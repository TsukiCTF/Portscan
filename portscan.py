#!/usr/bin/python3

from util import Parser
from util import FileManager
from core import port_scan
import sys


def print_banner():
    print(" ____               __                                      ")
    print("/\  _`\            /\ \__                                   ")
    print("\ \ \L\ \___   _ __\ \ ,_\   ____    ___     __      ___    ")
    print(" \ \ ,__/ __`\/\`'__\ \ \/  /',__\  /'___\ /'__`\  /' _ `\  ")
    print("  \ \ \/\ \L\ \ \ \/ \ \ \_/\__, `\/\ \__//\ \L\.\_/\ \/\ \ ")
    print("   \ \_\ \____/\ \_\  \ \__\/\____/\ \____\ \__/.\_\ \_\ \_\\")
    print("    \/_/\/___/  \/_/   \/__/\/___/  \/____/\/__/\/_/\/_/\/_/")


def print_version():
    print("+--")    
    print("Advanced Port Scanner (Staged Nmap Scans + Service Enumeration Tool)")
    print("Author   Tsuki CTF")
    print("Version  1.0 (beta)")
    print("+--")    
    print()


def main():
    parser = Parser()
    arguments = parser.run(sys.argv[1:])

    output_file = FileManager()

    if arguments.quiet is False:
        print_banner()
        print_version()

    if arguments.output:
        if output_file.create(arguments.output) is False:
            print(f"[!] File name already exists! ({arguments.output})")
            sys.exit(1)
        else:
            print(f"[*] Writing output to {arguments.output}")

    port_scan(arguments, output_file)


if __name__ == '__main__':
    main()
