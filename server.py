import logging
import socket
import sys

logger = logging.getLogger()
cl_address = []


def ex_communication(sv_addr: str, sv_port: int):
    """
    Exchange each other client info .
    :param sv_addr: <str> server address
    :param sv_port: <int> server port
    """

    # socket bind a port.
    upd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    upd_sock.bind((sv_addr, sv_port))

    while True:
        # buffer size is 1024 bytes
        data, cl_addr = upd_sock.recvfrom(1024)
        logger.info('connection from: %s', cl_addr)
        upd_sock.sendto(remake_access_point(cl_addr), cl_addr)
        logger.info('connection to: %s', cl_addr)

        cl_address.append(cl_addr)
        if len(cl_address) >= 2:
            # client A ⇔ client B
            logger.info("server - send client info to: %s", cl_address[0])
            upd_sock.sendto(remake_access_point(cl_address[1]), cl_address[0])
            logger.info("server - send client info to: %s", cl_address[0])
            upd_sock.sendto(remake_access_point(cl_address[0]), cl_address[1])

            # delete client info
            cl_address.pop(1)
            cl_address.pop(0)


def access_point(args: object, addr: str = '127.0.0.1', port: int = 9999) -> object:
    """
    get access point info from arguments.
    :param addr: <str> server address
    :param port: <int> server port
    :return: < > ip address/port
    """

    if len(args) >= 3:
        addr, port = args[1], int(args[2])
    elif len(args) == 2:
        addr, port = addr, int(args[1])
    else:
        addr, port = addr, port
    return addr, int(port)


def remake_access_point(data: object) -> bytes:
    """
    remake address and port string.
    :param data: <datagram> address and port
    :return: < > ip address:port
    """

    addr, port = data
    return ':'.join([addr, str(port)]).encode("UTF-8")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    ex_communication(*access_point(sys.argv))
