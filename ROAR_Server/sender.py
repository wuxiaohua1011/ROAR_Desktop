import socket
import time
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)

    host = "192.168.42.7"
    port = 8000

    while True:
        msg = f"{time.time()}"
        print(msg)
        s.sendto(msg.encode(), (host, port))

if __name__ == "__main__":
    main()

# import socket
# import time
# def main():
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     host = "192.168.42.7"
#     port = 8000
#
#     while True:
#         msg = f"{time.time()}"
#         print(msg)
#         s.sendto(msg.encode(), (host, port))
#
# if __name__ == "__main__":
#     main()