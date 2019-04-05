import logging
import socket

# initialize
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# set address, port.
sv_addr = socket.gethostbyname(socket.gethostname())
sv_port = 45001


def split_rcvmsg(data: str) -> object:
    """
    get Opposing access point info from datagram.
    :param data: <datagram> received datagram from server
    :return: < > ip address/port
    """

    addr, port = data.decode('utf-8').strip().split(':')
    return addr, int(port)


def sndmsg(message: str) -> bytes:
    """
    remake address and port string.
    :param message: <str> user input message
    :return: <bytes> message body
    """

    return message.encode("UTF-8")


# Internet, UPD.
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto(sndmsg(socket.gethostname()), (sv_addr, sv_port))
logger.info("connection to: {} {}".format(sv_addr, sv_port))

# wait until server message.
# buffer size is 1024 bytes.
data, server = client.recvfrom(1024)
logger.info("connection from: {}".format(server))

# split received message from server.
cl_addr, cl_port = split_rcvmsg(data)
client.sendto(sndmsg("> This is dummy."), (cl_addr, cl_port))
while True:
    message = input("> ")
    # send UDP packet to Opposing client
    client.sendto(sndmsg(message), (cl_addr, cl_port))
    logger.info('connection to: {} {}'.format(cl_addr, cl_port))
