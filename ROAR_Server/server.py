import socket


def main():
    # Set up socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except AttributeError:
        pass  # Some systems don't support SO_REUSEPORT
    s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 20)
    s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)

    port = 8000
    # Bind to the port
    s.bind(('', port))
    intf = socket.gethostbyname(socket.gethostname())
    s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(intf))
    # s.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton(intf))
    counter = 0
    while True:
        data, sender_addr = s.recvfrom(1024)
        s.sendto(f"hello {counter}".encode(), sender_addr)
        counter+=1


if __name__ == "__main__":
    main()