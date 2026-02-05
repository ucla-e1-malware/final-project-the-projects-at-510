from ..commands import Command # Required
import socket 
import shlex
import argparse

def scan_ip(target: str, port_range: tuple[int, int]) -> list[int]:
    open_ports = []

    for port in range(port_range[0], port_range[1] + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        s.close()
    return open_ports

def pretty_print_scan(open_ports: list[int]) -> None:
    """Takes in a list of ports (like from the output of scan_ip), and outputs a user-friendly table to read"""

    format_string = "{:<5} {:<5}" 
    print(format_string.format("Port", "Service"))
    
    for port in open_ports:
        print(format_string.format(port, socket.getservbyport(port, 'tcp')))

class Scan(Command): 
    """
    Scan ports on a target host.
    """

    # When this command is called, do_command() is executed. 
    def do_command(self, lines: str):
        parser = argparse.ArgumentParser(description="Scan ports on a target host.")
        parser.add_argument("target", help="The target IP address to scan.")
        parser.add_argument("start_port", type=int, help="The starting port number to scan.")
        parser.add_argument("end_port", type=int, help="The ending port number to scan.")
        parser.add_argument("--service-id", action="store_true", help="Show what service is running on each open port (if possible).")


        arguments = shlex.split(lines)
        args = parser.parse_args(arguments)

        target_ip = args.target
        open_ports = scan_ip(target_ip, (args.start_port, args.end_port))
        print(f"Open ports on {target_ip}: {", ".join(map(str, open_ports))}")
        pretty_print_scan(open_ports)
        

command = Scan # Assign the class you created to the variable called command for the system to find the command!
