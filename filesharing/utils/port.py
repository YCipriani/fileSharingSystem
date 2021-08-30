import socket
import sys
from contextlib import closing

port_file_path = sys.path[0].replace("utils", "").replace("/base_library.zip", "") + "port.txt"

def read_port_from_file():
    file = open(
        port_file_path,
        "r",
    )
    lines = file.read().splitlines()
    return lines[-1]


def read_all_ports_from_file():
    file = open(
        port_file_path,
        "r",
    )
    return file.read().splitlines()


def write_port_to_file(port):
    file = open(
        port_file_path,
        "a",
    )
    file.write("\n" + str(port))


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
