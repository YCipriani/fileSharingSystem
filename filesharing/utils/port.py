def read_port_from_file():
    file = open(
        "/Users/yonatancipriani/PycharmProjects/fileSharing/filesharing/resources/port.txt",
        "r",
    )
    lines = file.read().splitlines()
    return lines[-1]


def read_all_ports_from_file():
    file = open(
        "/Users/yonatancipriani/PycharmProjects/fileSharing/filesharing/resources/port.txt",
        "r",
    )
    return file.read().splitlines()


def write_port_to_file(port):
    file = open(
        "/Users/yonatancipriani/PycharmProjects/fileSharing/filesharing/resources/port.txt",
        "a",
    )
    file.write("\n" + str(port) + "\n")
