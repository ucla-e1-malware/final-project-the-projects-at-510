from ..commands import Command # Required
import socket 
import shlex

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
        arguments = shlex.split(lines)
        target_ip = arguments[0]
        open_ports = scan_ip(target_ip, (int(arguments[1]), int(arguments[2])))
        print(f"Open ports on {target_ip}: {", ".join(map(str, open_ports))}")
        print()
        pretty_print_scan(open_ports)
        

command = Scan # Assign the class you created to the variable called command for the system to find the command!
