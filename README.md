# WinRaider

```text
██╗    ██╗██╗███╗   ██╗██████╗  █████╗ ██╗██████╗ ███████╗██████╗
██║    ██║██║████╗  ██║██╔══██╗██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
██║ █╗ ██║██║██╔██╗ ██║██████╔╝███████║██║██║  ██║█████╗  ██████╔╝
██║███╗██║██║██║╚██╗██║██╔══██╗██╔══██║██║██║  ██║██╔══╝  ██╔══██╗
╚███╔███╔╝██║██║ ╚████║██║  ██║██║  ██║██║██████╔╝███████╗██║  ██║
 ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝

                     Windows Security Testing Toolkit
                              Version 2.0
```

WinRaider is a Windows security testing tool written in Python. It brings network scanning, Windows device discovery, vulnerability checks, credential testing, brute-force testing, logging, reporting, and Metasploit integration into one CLI tool.

> **For authorized security testing and lab environments only.**

---

## Features

* Port scanning for common Windows services
* Windows device discovery on the local network
* Checks for common Windows vulnerabilities
* SMB, RDP, WinRM, and SSH assessment
* Credential-based testing
* Username and password wordlist testing
* Multi-threaded brute-force support
* Progress bar for long-running tasks
* Activity logging
* Report generation
* Colored terminal output
* Quiet and verbose modes
* Metasploit integration

---

## Supported Ports

| Port   | Service | Description                          |
| ------ | ------- | ------------------------------------ |
| `445`  | SMB     | Primary Windows file-sharing service |
| `3389` | RDP     | Remote Desktop Protocol              |
| `5985` | WinRM   | Windows Remote Management over HTTP  |
| `5986` | WinRM   | Windows Remote Management over HTTPS |
| `139`  | NetBIOS | Legacy Windows networking            |
| `135`  | MSRPC   | Microsoft RPC                        |
| `22`   | SSH     | Secure Shell                         |

---

## Requirements

* Python 3.6+
* Nmap
* `python-nmap`
* `tqdm`

Install the Python dependencies with:

```powershell
pip install -r requirements.txt
```

Nmap must also be installed and available on your system for scanning features.

---

## Installation

Clone the repository:

```powershell
git clone https://github.com/Nullit13/winraider.git
cd winraider
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

You can run WinRaider directly from the source:

```powershell
python main.py --help
```

---

## Building the EXE

WinRaider can be packaged as a standalone Windows executable with PyInstaller.

Install PyInstaller:

```powershell
pip install pyinstaller
```

Build the executable:

```powershell
pyinstaller --onefile --console --name winraider --add-data "wordlists;wordlists" --hidden-import=nmap main.py
```

The executable will be created inside the `dist` directory.

Example:

```powershell
.\dist\winraider.exe --help
```

---

## Usage

### Discover Windows Devices

Scan the local network for Windows devices:

```powershell
python main.py --discover
```

---

### Port Scan

Scan the target for supported Windows services:

```powershell
python main.py -t 192.168.0.101 --scan
```

---

### Vulnerability Check

Run the available vulnerability checks without providing credentials:

```powershell
python main.py -t 192.168.0.101 --zero
```

---

### Credential Testing

Test a target using provided credentials:

```powershell
python main.py -t 192.168.0.101 --creds -u Abed -p password
```

---

### Brute Force

Run a username and password wordlist test:

```powershell
python main.py -t 192.168.0.101 --brute -w wordlists/passwords.txt --users wordlists/users.txt --threads 20
```

The number of threads can be changed with `--threads`.

---

### Logging

Save activity to `winraider.log`:

```powershell
python main.py -t 192.168.0.101 --scan --log
```

---

### Generate a Report

Save the scan results to a report file:

```powershell
python main.py -t 192.168.0.101 --scan --report report.txt
```

---

### Verbose Mode

Show additional information while WinRaider is running:

```powershell
python main.py -t 192.168.0.101 --scan -v
```

---

### Quiet Mode

Run with minimal terminal output:

```powershell
python main.py -t 192.168.0.101 --scan -q
```

---

## Command-Line Arguments

| Argument           | Description                                                   |
| ------------------ | ------------------------------------------------------------- |
| `-t`, `--target`   | Target IP address. Required for target-based operations.      |
| `--discover`       | Discover Windows devices on the local network.                |
| `-u`, `--username` | Username used for authentication.                             |
| `-p`, `--password` | Password used for authentication.                             |
| `-w`, `--wordlist` | Password wordlist. Default: `wordlists/passwords.txt`         |
| `--users`          | Username wordlist. Default: `wordlists/users.txt`             |
| `--threads`        | Number of threads used for brute-force testing. Default: `10` |
| `--msfpath`        | Path to the Metasploit `msfconsole` executable.               |
| `--lhost`          | Local host IP used for Metasploit operations.                 |
| `-v`, `--verbose`  | Enable verbose output.                                        |
| `-q`, `--quiet`    | Enable quiet mode.                                            |
| `--log`            | Save activity to `winraider.log`.                             |
| `--report`         | Save results to a report file.                                |
| `--scan`           | Run a port scan only.                                         |
| `--zero`           | Run vulnerability checks without credentials.                 |
| `--creds`          | Run testing using supplied credentials.                       |
| `--brute`          | Run username/password wordlist testing.                       |

---

## Wordlists

WinRaider supports separate username and password wordlists.

### Username List

```text
administrator
admin
user
guest
```

### Password List

```text
password
Password123
admin123
```

Put one entry on each line.

Avoid unnecessary spaces or empty lines in the wordlists.

---

## Included Wordlists

The repository includes:

```text
wordlists/
├── users.txt
└── passwords.txt
```

* `wordlists/users.txt` — Username list
* `wordlists/passwords.txt` — Password list

---

## Project Structure

```text
WinRaider/
├── main.py
├── requirements.txt
├── README.md
├── wordlists/
│   ├── users.txt
│   └── passwords.txt
└── ...
```

---

## Logging & Reports

WinRaider can save activity and scan results to files.

Enable logging:

```powershell
python main.py -t 192.168.0.101 --scan --log
```

Generate a report:

```powershell
python main.py -t 192.168.0.101 --scan --report report.txt
```

This makes it easier to keep records of authorized security assessments.

---

## Metasploit Integration

WinRaider supports integration with Metasploit through `msfconsole`.

Specify the path to your Metasploit installation:

```powershell
python main.py -t 192.168.0.101 --msfpath "C:\path\to\msfconsole.exe"
```

A local host address can also be supplied when required:

```powershell
python main.py -t 192.168.0.101 --msfpath "C:\path\to\msfconsole.exe" --lhost 192.168.0.102
```

Use Metasploit functionality only against systems where you have explicit authorization.

---

## Recommended Lab Setup

For testing and development, use an isolated environment such as:

```text
┌──────────────────────┐
│    Windows Target    │
│     Test Machine     │
└──────────┬───────────┘
           │
        Isolated
        Network
           │
┌──────────▼───────────┐
│     WinRaider        │
│    Testing Machine   │
└──────────────────────┘
```

A virtualized lab is recommended so testing does not affect systems or networks that are not part of the assessment.

---

## Version 2.0

Version 2.0 adds several improvements over the previous version, including:

* Windows device discovery
* Logging support
* Report generation
* Multi-threaded brute-force testing
* Configurable thread count
* Dedicated scan, vulnerability, credential, and brute-force modes
* Improved CLI output
* Metasploit configuration options

---

## Legal Disclaimer

WinRaider is provided for **educational purposes, security research, authorized penetration testing, and controlled lab environments**.

You may only use WinRaider against systems that you own or have explicit permission to test.

Unauthorized access, credential attacks, vulnerability testing, or other activity against systems without permission may be illegal.

The author is not responsible for any misuse, damage, unauthorized access, data loss, or other consequences resulting from the use of this software.

**Use responsibly and only with proper authorization.**

---

## Author

**Adam (Nullit13)**

GitHub: https://github.com/Nullit13

Project: https://github.com/Nullit13/winraider

---

## License

WinRaider is released under the MIT License.

See the `LICENSE` file for details.

---

## Project Goals

WinRaider is intended to make Windows security testing easier to perform from a single command-line interface while keeping the tool useful for security research, testing, and lab environments.