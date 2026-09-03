def get_banner():
    return """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██╗    ██╗██╗███╗   ██╗██████╗  █████╗ ██╗██████╗ ███████╗ ║
║   ██║    ██║██║████╗  ██║██╔══██╗██╔══██╗██║██╔══██╗██╔════╝ ║
║   ██║ █╗ ██║██║██╔██╗ ██║██████╔╝███████║██║██║  ██║█████╗   ║
║   ██║███╗██║██║██║╚██╗██║██╔══██╗██╔══██║██║██║  ██║██╔══╝   ║
║   ╚███╔███╔╝██║██║ ╚████║██║  ██║██║  ██║██║██████╔╝███████╗ ║
║    ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝ ║
║                                                               ║
║              Windows Auto-Hack Tool v1.0                      ║
║              Author: Nullit                                     ║
╚═══════════════════════════════════════════════════════════════╝
    """

def get_epilog():
    return """
[+] Examples:
    python -m winraider.main -t 192.168.0.0 -u nullit -p pass
    python -m winraider.main -t 192.168.0.0 -w passwords.txt --users usernames.txt
    python -m winraider.main -t 192.168.0.0 --msfpath "C:\\metasploit\\msfconsole"

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
    """