from multiprocessing import Process
import socket
import subprocess


def staged_nmap(ip_address, output):
    """
    Stage 1: Open Port Scan For Common TCP Ports + Light Version Detection

    """
    print("[+] Starting quick nmap scan for %s" % ip_address)
    QUICKSCAN = "nmap -Pn -sV --version-light --min-rate=3000 %s" % (ip_address)
    quickresults = subprocess.check_output(QUICKSCAN, shell=True).decode("utf-8")

    # parse ports only
    ports = [_ for _ in quickresults.split() if '/tcp' in _]
    # parse ports and services
    quickresults = '\n| '.join( quickresults.split('\n')[4:-4] )
    quickresults = '\n%s\n\\%s...\n' % (quickresults, "_" * 16)

    print("[*] TCP quick scans completed for %s" % ip_address)
    print("[*] Total number of ports discovered for TCP: %d" % len(ports))
    print(quickresults)

    """
    Stage 2: Open Port Scan For All 65535 TCP Ports

    """
    print("[+] Starting full port scan for TCP (range: 1-65535)")
    FULLTCP = "nmap -Pn -p- -T4 --min-rate=3000 %s" % (ip_address)
    fulltcp_results = subprocess.check_output(FULLTCP, shell=True).decode("utf-8")

    # parse ports and append
    for _ in fulltcp_results.split():
        if '/tcp' in _:
            ports.append(_)
    ports = list(set(ports))
    portlist = ",".join([p.rstrip("/tcp") for p in ports])

    print("[*] TCP full port scan completed")
    print("[*] Total number of ports discovered for TCP: %d" % len(ports))
    
    """
    Stage 3: Run Default NSE Scripts + Version Detection Against Ports Found From Stage 2

    """
    output.append(f"TCP port scan result for {ip_address}:\n")
    if len(ports) > 0:
        print("[+] Starting service enumeration for TCP ports: %s" % portlist)
        ENUMTCP = "nmap -Pn -p '%s' -sC -sV --min-rate=1500 %s" % (portlist, ip_address)
        enumtcp_results = subprocess.check_output(ENUMTCP, shell=True).decode("utf-8")

        # parse nmap enum output
        enumtcp_results = '\n| '.join(
            [ _ for _ in enumtcp_results.split('\n')[4:-4] if " closed " not in _ ])
        enumtcp_results = '\n%s\n\\%s...\n' % (enumtcp_results, "_" * 64)

        print("[*] Enumeration for TCP ports finished")
        print(enumtcp_results)
        output.append(enumtcp_results)
        output.append("\n\n")
    else:
        print("[-] Skipping TCP service enumeration due to no open ports found")

    """
    Stage 4: Open Port Scan For All 65535 UDP Ports

    """
    print("[+] Starting full port scan for UDP (range: 1-65535)")
    FULLUDP = "nmap -Pn -p- -sU -T4 --min-rate=3000 %s" % (ip_address)
    fulludp_results = subprocess.check_output(FULLUDP, shell=True).decode("utf-8")

    # parse udp ports
    udp_ports = []
    for _ in fulludp_results.split():
        if '/udp' in _:
            udp_ports.append(_)
    udp_ports = list(set(udp_ports))
    udp_portlist = ",".join([p.rstrip("/udp") for p in udp_ports])

    print("[*] UDP full port scan completed")
    print("[*] Total number of ports discovered for UDP: %d" % len(udp_ports))

    """
    Stage 5: Run Default NSE Scripts + Version Detection Against Ports Found From Stage 5

    """
    output.append(f"UDP port scan result for {ip_address}:\n")
    if len(udp_ports) > 0:
        print("[+] Starting service enumeration for UDP ports: %s" % udp_portlist)
        ENUMUDP = "nmap -Pn -p '%s' -sU -sC -sV --min-rate=1000 %s" % (udp_portlist, ip_address)
        enumudp_results = subprocess.check_output(ENUMUDP, shell=True).decode("utf-8")

        # parse nmap enum output
        enumudp_results = '\n| '.join(
            [ _ for _ in enumudp_results.split('\n')[4:-3] if " closed " not in _ ])
        enumudp_results = '\n%s\n\\%s...\n' % (enumudp_results, "_" * 64)

        print("[*] Enumeration for UDP ports finished")
        print(enumudp_results)
        output.append(enumudp_results)
    else:
        print("[-] Skipping UDP service enumeration due to no open ports found")

    print()
    print("[*] Portscan finished.")



def port_scan(host, output_handle):
    # TODO: add more options that can be used as valid host
    # (currently only supporting IPv4 address for target)
    try:
        socket.inet_aton(host)
        print("[*] Loaded target address: %s" % host)
    except socket.error:
        print("[-] Invalid IPv4 address for host")
        sys.exit(1)

    # this list will come handy for managing multiple active scanners in future updates (alpha)
    jobs = []
    p = Process(target=staged_nmap, args=(host,output_handle,))
    jobs.append(p)
    p.start()
