import argparse
import subprocess
import sys
import os
from utils import get_banner, get_epilog, setup_logging, color_text, Colors
from scanner import nmap_scan, filter_open_ports, scan_only
from exploit import attack_with_credentials, attack_zero_day
from brute import brute_force

def discover_windows():
    import socket
    import re
    import subprocess
    import ipaddress
    import threading
    from queue import Queue
    
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        result = subprocess.run(['ipconfig'], capture_output=True, text=True)
        match = re.search(r'Subnet Mask[ .]+: (\d+\.\d+\.\d+\.\d+)', result.stdout)
        if not match:
            print(color_text("[-] Could not find subnet mask", Colors.RED))
            return
        subnet_mask = match.group(1)
        ip_parts = local_ip.split('.')
        mask_parts = subnet_mask.split('.')
        network_parts = []
        for i in range(4):
            network_parts.append(str(int(ip_parts[i]) & int(mask_parts[i])))
        network = '.'.join(network_parts)
        cidr = sum(bin(int(x)).count('1') for x in mask_parts)
        subnet = f"{network}/{cidr}"
        print(color_text(f"[+] Local IP: {local_ip}", Colors.BLUE))
        print(color_text(f"[+] Subnet: {subnet}", Colors.BLUE))
        print(color_text(f"[+] Scanning for Windows devices...", Colors.BLUE))
        
        network_range = ipaddress.ip_network(subnet, strict=False)
        windows_ips = []
        lock = threading.Lock()
        
        def check_host(ip_str):
            if ip_str == local_ip:
                return
            try:
                result = subprocess.run(
                    ['ping', '-n', '1', '-w', '500', ip_str],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                if "TTL" in result.stdout or "Reply from" in result.stdout:
                    for port in [445, 135, 139]:
                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            sock.settimeout(0.5)
                            if sock.connect_ex((ip_str, port)) == 0:
                                with lock:
                                    windows_ips.append(ip_str)
                                sock.close()
                                break
                            sock.close()
                        except:
                            pass
            except:
                pass
        
        threads = []
        for ip in network_range.hosts():
            ip_str = str(ip)
            t = threading.Thread(target=check_host, args=(ip_str,))
            t.daemon = True
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join(timeout=0.5)
        
        if windows_ips:
            print(color_text(f"\n[+] Found {len(windows_ips)} Windows device(s):", Colors.GREEN))
            for ip in sorted(windows_ips):
                print(f"    - {ip}")
        else:
            print(color_text("[-] No Windows devices found.", Colors.YELLOW))
            
    except Exception as e:
        print(color_text(f"[-] Discovery failed: {e}", Colors.RED))

def main():
    parser = argparse.ArgumentParser(
        prog="WinRaider",
        description=get_banner(),
        epilog=get_epilog(),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-t', '--target', required=False, help='Target IP address')
    parser.add_argument('--discover', action='store_true', help='Discover Windows devices on the local network')
    parser.add_argument('-u', '--username', help='Username for authentication')
    parser.add_argument('-p', '--password', help='Password for authentication')
    parser.add_argument('-w', '--wordlist', default='wordlists/passwords.txt', help='Password wordlist for brute force')
    parser.add_argument('--users', default='wordlists/users.txt', help='Username wordlist for brute force')
    parser.add_argument('--threads', type=int, default=10, help='Number of threads for brute force (default: 10)')
    parser.add_argument('--msfpath', help='Path to Metasploit msfconsole')
    parser.add_argument('--lhost', help='Local host IP for Metasploit reverse shells')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-q', '--quiet', action='store_true', help='Quiet mode (minimal output)')
    parser.add_argument('--log', action='store_true', help='Log all activity to winraider.log')
    parser.add_argument('--report', help='Save report to a file (e.g., report.txt)')
    
    attack_group = parser.add_mutually_exclusive_group(required=False)
    attack_group.add_argument('--scan', action='store_true', help='Port scan only (no attack)')
    attack_group.add_argument('--zero', action='store_true', help='Zero-day vulnerability check (no credentials)')
    attack_group.add_argument('--creds', action='store_true', help='Attack using provided credentials')
    attack_group.add_argument('--brute', action='store_true', help='Brute force credentials')
    
    args = parser.parse_args()

    if args.discover:
        discover_windows()
        return
    
    if args.log:
        logger = setup_logging()
    else:
        logger = None
    
    if not args.quiet:
        print(get_banner())
    
    print(color_text(f"\n[+] Target: {args.target}", Colors.WHITE))
    if args.username and args.creds:
        print(color_text(f"[+] Username: {args.username}", Colors.WHITE))
    if args.verbose:
        print(color_text("[+] Verbose mode enabled", Colors.BLUE))
    
    json_data = nmap_scan(args.target)
    open_ports = filter_open_ports(json_data)
    print(color_text(f"\n[+] Open ports: {open_ports}", Colors.WHITE))
    
    if args.log and logger:
        logger.info(f"Target: {args.target}, Open ports: {open_ports}")
    
    report_data = {}
    report_data['target'] = args.target
    report_data['open_ports'] = open_ports
    
    if args.scan:
        scan_only(open_ports)
        report_data['mode'] = 'scan'
        report_data['result'] = 'scan completed'
    
    elif args.zero:
        print(color_text("\n[!] Starting zero-day vulnerability check...", Colors.YELLOW))
        msf_path = None
        if args.msfpath:
            msf_path = args.msfpath
        else:
            check = subprocess.run(['where', 'msfconsole'], capture_output=True, text=True)
            if check.returncode == 0:
                msf_path = check.stdout.strip().split('\n')[0]
        
        attack_zero_day(args.target, open_ports, msf_path)
        report_data['mode'] = 'zero-day'
        report_data['result'] = 'vulnerability check completed'
    
    elif args.creds:
        if not args.username or not args.password:
            print(color_text("[-] --creds requires -u (username) and -p (password)", Colors.RED))
            sys.exit(1)
        print(color_text("\n[+] Credentials provided. Attempting authenticated attack...", Colors.GREEN))
        attack_with_credentials(args.target, args.username, args.password, open_ports)
        report_data['mode'] = 'credentials'
        report_data['username'] = args.username
        report_data['password'] = args.password
        report_data['result'] = 'attack completed'
    
    elif args.brute:
        print(color_text("\n[+] Starting brute force attack...", Colors.GREEN))
        username, password = brute_force(args.target, args.users, args.wordlist, args.threads)
        if username and password:
            print(color_text(f"\n[+] Credentials found: {username}:{password}", Colors.GREEN))
            attack_with_credentials(args.target, username, password, open_ports)
            report_data['mode'] = 'brute'
            report_data['found_username'] = username
            report_data['found_password'] = password
            report_data['result'] = 'credentials found and attack completed'
        else:
            print(color_text("\n[-] Brute force failed. No credentials found.", Colors.RED))
            report_data['mode'] = 'brute'
            report_data['result'] = 'no credentials found'
    
    if args.report:
        try:
            with open(args.report, 'w') as f:
                f.write("WinRaider Report\n")
                f.write("================\n\n")
                for key, value in report_data.items():
                    f.write(f"{key}: {value}\n")
                f.write(f"\nReport generated: {__import__('datetime').datetime.now()}\n")
            print(color_text(f"\n[+] Report saved to: {args.report}", Colors.GREEN))
            if args.log and logger:
                logger.info(f"Report saved to {args.report}")
        except Exception as e:
            print(color_text(f"[-] Failed to save report: {e}", Colors.RED))
    
    print(color_text("\n[+] WinRaider finished.", Colors.GREEN))

if __name__ == "__main__":
    main()