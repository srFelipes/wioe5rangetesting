"""
serial_wioe5.py is a python module used to communicate via serial with the wio e5,
based on the information at https://files.seeedstudio.com/products/317990687/res/LoRa-E5%20AT%20Command%20Specification_V1.0%20.pdf
"""
import serial
import serial.tools.list_ports
from src.wio_errors import *
baudrate = 9600
timeout = 1

def ports():
    """
    returns a list of available ports to be opened
    """
    ports = serial.tools.list_ports.comports()
    list = []
    for port, _, _ in sorted(ports):
        list.append(port)
    return list

class Wioe5:
    def __init__(self,serial_port: serial.Serial= None):
        """
        initialization method, a port can be given to it, otherwise it will try
        to open /dev/ttyUSB1
        """
        if not serial_port:
            serial_port = serial.Serial('/dev/ttyUSB0', baudrate)
        self.connection = serial.Serial(port =serial_port.port,timeout=timeout)
        self.write('AT')
        self.mode = None
        self.error = None
    def write(self,command : str):
        """
        Write method, it checks if there is an error in the answer before returning it
        """
        if not b'\n' == command[-1]:
            command += '\n'
        self.connection.write(command.encode('UTF-8'))
        self.connection.flush()
        answer = self.connection.readline()
        wioError(answer)
        return answer