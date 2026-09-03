# ⚡ WinRaider

```text
██╗    ██╗██╗███╗   ██╗██████╗  █████╗ ██╗██████╗ ███████╗██████╗
██║    ██║██║████╗  ██║██╔══██╗██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
██║ █╗ ██║██║██╔██╗ ██║██████╔╝███████║██║██║  ██║█████╗  ██████╔╝
██║███╗██║██║██║╚██╗██║██╔══██╗██╔══██║██║██║  ██║██╔══╝  ██╔══██╗
╚███╔███╔╝██║██║ ╚████║██║  ██║██║  ██║██║██████╔╝███████╗██║  ██║
 ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝

          Windows Security Assessment & Penetration Testing Toolkit
```

> **WinRaider** is a Python-based Windows penetration-testing and security-assessment toolkit designed for authorized security testing, research, and educational lab environments.

---

## 🚀 Features

WinRaider provides a unified CLI for assessing commonly exposed Windows services.

### 🔎 Network & Service Scanning

Scans seven commonly targeted Windows/network services:

* **445 — SMB**
* **3389 — RDP**
* **5985 — WinRM HTTP**
* **5986 — WinRM HTTPS**
* **139 — NetBIOS**
* **135 — MSRPC**
* **22 — SSH**

### 🔐 Authenticated Testing

When authorized credentials are supplied, WinRaider can test:

* SMB authenticated file access
* RDP authenticated GUI access
* WinRM authenticated shell access
* SSH authenticated shell access

### 🛡️ Unauthenticated Vulnerability Assessment

WinRaider includes checks for security issues associated with:

* EternalBlue / MS17-010
* BlueKeep / CVE-2019-0708
* SMBGhost / CVE-2020-0796
* WinRM authentication/configuration weaknesses
* NetBIOS information disclosure
* SSH-related vulnerabilities

### 🔑 Credential Testing

Supports username and password wordlists for authorized credential-security assessments.

### 💥 Metasploit Integration

If `msfconsole` is available, WinRaider can integrate with Metasploit for supported security-testing workflows.

The Metasploit executable can be supplied explicitly with:

```text
--msfpath
```

### 🖥️ Professional CLI

Includes:

* Startup banner
* Quiet mode
* Verbose mode
* Command-line argument parsing
* Target-oriented scanning
* Optional authentication parameters
* Optional wordlists
* Optional Metasploit configuration

---

# 📦 Installation

## Requirements

* Windows
* Python 3.x
* Network access to an **authorized** test environment
* Optional: Metasploit Framework for Metasploit integration

Clone the repository:

```bash
git clone https://github.com/Nullit13/winraider.git
cd winraider
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Verify the installation:

```bash
python winraider.py --help
```

---

# 🛠️ Usage

After building the project, WinRaider can be run directly using the compiled executable:

```powershell
.\winraider.exe -t <TARGET>
```

For example, against a machine in an isolated authorized lab:

```powershell
.\winraider.exe -t 192.0.2.10
```

> `192.0.2.0/24` is reserved for documentation and examples. Replace it with an IP address belonging to a system you are explicitly authorized to test.

## Verbose Mode

Display additional diagnostic information:

```powershell
.\winraider.exe -t 192.0.2.10 -v
```

## Quiet Mode

Suppress non-essential output:

```powershell
.\winraider.exe -t 192.0.2.10 -q
```

## Authenticated Assessment

Provide credentials for authorized authenticated testing:

```powershell
.\winraider.exe -t 192.0.2.10 -u administrator -p "<PASSWORD>"
```

## Password Wordlist

Specify a password wordlist for authorized credential testing:

```powershell
.\winraider.exe -t 192.0.2.10 -w passwords.txt
```

## Username + Password Wordlists

```powershell
.\winraider.exe -t 192.0.2.10 --users users.txt -w passwords.txt
```

Only use credential-testing functionality against systems and accounts for which you have explicit authorization.

## Metasploit Configuration

Specify the location of `msfconsole`:

```powershell
.\winraider.exe -t 192.0.2.10 --msfpath "C:\path\to\msfconsole.exe"
```

A local host can be supplied for authorized reverse-shell testing:

```powershell
.\winraider.exe -t 192.0.2.10 --msfpath "C:\path\to\msfconsole.exe" --lhost 192.0.2.20
```

---

# 📋 Command-Line Arguments

| Argument           | Description                                         |
| ------------------ | --------------------------------------------------- |
| `-t`, `--target`   | **Required.** Target IP address                     |
| `-u`, `--username` | Username for authentication                         |
| `-p`, `--password` | Password for authentication                         |
| `-w`, `--wordlist` | Password wordlist for authorized credential testing |
| `--users`          | Username wordlist for authorized credential testing |
| `--msfpath`        | Path to Metasploit `msfconsole`                     |
| `--lhost`          | Local host IP for supported Metasploit workflows    |
| `-v`, `--verbose`  | Verbose output                                      |
| `-q`, `--quiet`    | Quiet mode                                          |

---

# 🔌 Supported Ports & Assessment Types

|     Port | Service     | Assessment Types                                                                                    |
| -------: | ----------- | --------------------------------------------------------------------------------------------------- |
|  **445** | SMB         | Service discovery, authenticated SMB access, SMB vulnerability checks, credential testing           |
| **3389** | RDP         | Service discovery, authenticated RDP testing, BlueKeep assessment, credential testing               |
| **5985** | WinRM HTTP  | Service discovery, authentication testing, WinRM configuration/security checks                      |
| **5986** | WinRM HTTPS | Service discovery, authenticated WinRM testing, configuration/security checks                       |
|  **139** | NetBIOS     | Service discovery, information-disclosure assessment, credential testing                            |
|  **135** | MSRPC       | Service discovery and RPC-related security assessment                                               |
|   **22** | SSH         | Service discovery, authenticated SSH testing, SSH security/vulnerability checks, credential testing |

---

# 📄 Wordlist Format

WinRaider accepts plain-text wordlists.

Each entry should occupy a separate line.

### Password wordlist

```text
password123
Password123!
Winter2026!
ExamplePassword
```

### Username wordlist

```text
administrator
admin
guest
test
user
```

Blank lines should generally be avoided.

For example:

```text
users.txt
├── administrator
├── admin
├── test
└── user
```

```text
passwords.txt
├── password123
├── Password123!
├── ExamplePassword
└── Winter2026!
```

When using wordlists, keep testing constrained to accounts and systems explicitly included within your authorization.

---

# 🧪 Recommended Lab Environment

For safe testing and development, use WinRaider against machines specifically configured as security-testing targets.

A suitable lab can contain:

```text
┌───────────────────────┐
│    WinRaider Host     │
│       Windows         │
└───────────┬───────────┘
            │
            │ Isolated Lab Network
            │
┌───────────▼───────────┐
│   Windows Test VM     │
│  SMB / RDP / WinRM    │
│  NetBIOS / MSRPC      │
└───────────────────────┘
```

Avoid running intrusive testing against systems that you do not own or have explicit permission to assess.

---

# ⚖️ Legal Disclaimer

**WinRaider is intended strictly for authorized security testing, education, research, and defensive security assessment.**

You are solely responsible for ensuring that your use of this software complies with all applicable laws, regulations, contracts, and organizational policies.

Do **not** use WinRaider to:

* Access systems without authorization
* Attack third-party infrastructure
* Attempt to obtain unauthorized credentials
* Disrupt or damage systems or networks
* Deploy exploits against systems without explicit permission
* Circumvent security controls without authorization

The author and contributors are **not responsible for misuse, damage, data loss, unauthorized access, or any other consequences resulting from use of this software**.

By using WinRaider, you acknowledge that you are responsible for obtaining appropriate authorization before conducting any security assessment.

---

# 👤 Author

**Adam Abed**

* GitHub: `@nullit13`
* Project: `WinRaider`
* Language: Python

---

# 📜 License

WinRaider is released under the **MIT License**.

```text
MIT License

Copyright (c) 2026 Adam Abed

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the
Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```

See [`LICENSE`](LICENSE) for the complete license text.

---

## ⭐ Project Goals

WinRaider aims to provide security researchers, students, and penetration testers with a single Python-based interface for assessing common Windows network services in controlled environments.

**Use it responsibly. Test only systems you are authorized to test.**