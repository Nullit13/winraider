import logging
from datetime import datetime

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def setup_logging(log_file="winraider.log"):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger()

def color_text(text, color):
    return f"{color}{text}{Colors.RESET}"

def get_banner():
    return f"""
{Colors.BLUE}╔═══════════════════════════════════════════════════════════════╗
║                                                                            ║
║    ██╗    ██╗██╗███╗   ██╗██████╗  █████╗ ██╗██████╗ ███████╗██████╗       ║
║    ██║    ██║██║████╗  ██║██╔══██╗██╔══██╗██║██╔══██╗██╔════╝██╔══██╗      ║
║    ██║ █╗ ██║██║██╔██╗ ██║██████╔╝███████║██║██║  ██║█████╗  ██████╔╝      ║
║    ██║███╗██║██║██║╚██╗██║██╔══██╗██╔══██║██║██║  ██║██╔══╝  ██╔══██╗      ║
║    ╚███╔███╔╝██║██║ ╚████║██║  ██║██║  ██║██║██████╔╝███████╗██║  ██║      ║
║    ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝       ║
║                                                                            ║
║              Windows Auto-Hack Tool v2.0                                   ║
║              Author: Nullit                                                ║ 
╚════════════════════════════════════════════════════════════════════════════╝{Colors.RESET}
    """

def get_epilog():
    return f"""
{Colors.YELLOW}[+] Examples:
    winraider -t 192.168.0.101 --scan
    winraider -t 192.168.0.101 --zero
    winraider -t 192.168.0.101 --creds -u Abed -p password
    winraider -t 192.168.0.101 --brute -w passwords.txt --users users.txt --threads 20

[+] Attack Modes:
    --scan   : Port scan only (no attack)
    --zero   : Zero-day vulnerability check (no credentials)
    --creds  : Use provided credentials to attack
    --brute  : Brute force credentials using wordlists

[+] Supported Ports:
    445  - SMB (Primary)
    3389 - RDP
    5985 - WinRM HTTP
    5986 - WinRM HTTPS
    139  - NetBIOS
    22   - SSH
{Colors.RESET}
    """