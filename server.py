import logging
import socket


# initialize
con_clients = []

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# set address, port.
sv_addr = socket.gethostbyname(socket.gethostname())
sv_port = 51000


def sndmsg(address: object) -> bytes:
    """
    remake address and port string.
    :param address: <datagram> address and port
    :return: <bytes> message body
    """

    ip, port = address
    return ':'.join([ip, str(port)]).encode("UTF-8")


# Internet, UPD.
# socket bind a port.
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((sv_addr, sv_port))

while True:
    # wait until client message.
    # buffer size is 1024 bytes.
    data, client = server.recvfrom(1024)
    logger.info('connection from: {}', client)

    # duplicate check
    if client not in con_clients:
        con_clients.append(client)

    if len(con_clients) == 1:
        # server.sendto('waiting connection...', client)
        # logger.info('connection to: {}', client)
        pass

    elif len(con_clients) == 2:
        # exchange address each other.
        logger.info("server - send client info to: {}", con_clients[1])
        server.sendto(sndmsg(con_clients[1]), con_clients[0])
        logger.info("server - send client info to: {}", con_clients[0])
        server.sendto(sndmsg(con_clients[0]), con_clients[1])

        # clear client info
        con_clients.clear()

    else:
        pass
