import nmap
import json
from utils import color_text, Colors

def nmap_scan(target):
    scanner = nmap.PortScanner()
    ports = '445,3389,5985,5986,139,135,22'
    print(color_text(f"Scanning machine({target}) ...", Colors.BLUE))
    scanner.scan(target, ports)

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
    return json.dumps(hosts_data)

def filter_open_ports(json_data):
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data
    
    result = []
    
    for host_entry in data:
        open_ports = []
        for protocol in host_entry.get("protocols", []):
            for port_info in protocol.get("ports", []):
                if port_info.get("state") == "open":
                    open_ports.append(port_info.get("port"))
        if open_ports:
            result = open_ports
        else:
            print(color_text("No open ports found!", Colors.YELLOW))
    return result

def scan_only(open_ports):
    print(color_text("\n[+] Scan completed. Open ports found:", Colors.GREEN))
    for port in open_ports:
        print(f"    - {port}")