import logging
import socket
import sys

from socket import gethostname

logger = logging.getLogger()


def ex_communication(sv_addr: str, sv_port: int):
    """
    client gets opposite client address from the server.
    :param sv_addr: <str> server address
    :param sv_port: <int> server port
    """

    # send UDP packet to server.
    upd_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    upd_sock.sendto(gethostname(), (sv_addr, sv_port))
    logger.info('connection to: {} {}'.format(sv_addr, sv_port))

    while True:
        # wait until server response
        data, sv_addr = upd_sock.recvfrom(1024)
        logger.info('connection from: %s', sv_addr)

        # get opposing client
        cl_addr, cl_port = opposite_access_point(data)
        # send UDP packet to Opposing client
        upd_sock.sendto(gethostname(), (cl_addr, cl_port))
        logger.info('connection to: {} {}'.format(cl_addr, cl_port))

        # wait until opposing client response
        data, addr = upd_sock.recvfrom(1024)
        logger.info('connection from: %s', addr)


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


def opposite_access_point(data):
    """
    get Opposing access point info from datagram.
    :param data: <datagram> received datagram from server
    :return: < > ip address/port
    """

    addr, port = data.decode('utf-8').strip().split(':')
    return addr, int(port)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    ex_communication(*access_point(sys.argv))
