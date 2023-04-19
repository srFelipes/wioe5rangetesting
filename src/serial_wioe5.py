"""
serial_wioe5.py is a python module used to communicate via serial with the wio e5,
based on the information at https://files.seeedstudio.com/products/317990687/res/LoRa-E5%20AT%20Command%20Specification_V1.0%20.pdf
"""
import logging
import serial
import serial.tools.list_ports
from src.wio_errors import *
baudrate = 9600
timeout = 1

logger = logging.getLogger(__name__)

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
        if serial_port:
            if serial.Serial==type(serial_port):
                self.connection = serial.Serial(port=serial_port.port,
                                                timeout=timeout)
            elif str==type(serial_port):
                self.connection = serial.Serial(port=serial_port,
                                                baudrate=baudrate,
                                                timeout=timeout)
            
        else:
            self.connection = serial.Serial('/dev/ttyUSB0', baudrate)
        
        self.write('AT')
        self.mode = None
        self.state = None
        self.error = None
        self.test_config_dict = {}
        self.is_test_config = False
        self.test_status = 'NO'

    def write(self,command : str):
        """
        Write method, it checks if there is an error in the answer before returning it
        """
        logger.debug('command %s',command)
        if not '\n' == command[-1]:
            command += '\n'
        self.connection.write(command.encode('UTF-8'))
        self.connection.flush()
        answer = self.connection.readline()
        newlinepos = answer.find(b'\n') 
        if not newlinepos == -1:
            if answer.find(b'\r') == -1:
                answer = answer[:newlinepos]
            else:
                answer = answer[:newlinepos-1]
        try:
            wioError(answer)
        except Exception as e:
            logger.error('answer \"%s\" is an error',answer,exc_info=e)
            raise e
        logger.debug('answer was %s',answer)
        return answer.decode()
    
    def get_mode(self):
        """
        Ask the mode to the radio
        """
        query = 'AT+MODE\n'
        answer = self.write(query)
        self.mode = answer[7:]
        return self.mode
    
    def set_mode(self,new_mode : str):
        """
        set the mode of the radio
        """
        query = 'AT+MODE='+new_mode
        answer = self.write(query)[7:]
        if answer == new_mode:
            self.mode = new_mode
            if self.mode == 'TEST':
                self.is_test_config=False
            return 1
        else:
            return 0
    
    def set_sleep(self):
        """
        put the radio to sleep, it will wake up after any command is given
        """
        query =  'AT+LOWPOWER'
        answer =  self.write(query)
        if answer[11:]=='SLEEP':
            self.state='SLEEP'
    
    def wakeup(self):
        """
        wakes up the radio after sleeping
        """
        if not 'SLEEP' == self.state:
            return 
        query = 'AT'
        answer = self.write(query)
        if 'WAKEUP' == answer[11:]:
            self.state='OK'
    
    def config_test(self,
                    frequency = '915', 
                    sf='SF12',
                    bandwidth = '125',
                    tx_preamble= '12',
                    rx_preamble= '15',
                    tx_power='14',
                    crc='ON',
                    iq='OFF',
                    net='OFF'):
        """
        Checks if the radio is in test mode and then send the given configuration
        """
        if not self.mode == 'TEST':
            self.set_mode('TEST')
        query = 'AT+TEST=RFCFG,'+frequency+','+ \
                sf+','+\
                bandwidth+','+\
                tx_preamble+','+\
                rx_preamble+','+\
                tx_power+','+\
                crc+','+\
                iq+','+\
                net+'\n'
        answer = self.write(query)
        positions = [i for i, letter in enumerate(answer) if letter == ',']
        self.test_config_dict={
            'frequency' : answer[15:positions[0]],
            'sf':answer[positions[0]+2:positions[1]],
            'bandwidth' : answer[positions[1]+2:positions[2]],
            'tx_preamble': answer[positions[2]+7:positions[3]],
            'rx_preamble': answer[positions[3]+7:positions[4]],
            'tx_power': answer[positions[4]+6:positions[5]],
            'crc':answer[positions[5]+6:positions[6]],
            'iq':answer[positions[6]+5:positions[7]],
            'net':answer[positions[7]+6:]}
        self.is_test_config=True
    
    def set_test_crx(self):
        """
        If the radio is in test mode and it has been configured,
        sets it in continuous RX mode
        """
        if self.mode=='TEST' and self.is_test_config:
            query = 'AT+TEST=RXLRPKT'
            answer = self.write(query)
            self.test_status = answer[7:]

    def wait_for_packet_in_test(self):
        """
        if the test_status is RXLRPKT then it blocks until a new message is received
        UNTESTED
        """
        if self.test_status=='RXLRPKT':
            while True:
                rawpacket = self.connection.readline()
                if rawpacket:
                    return rawpacket[rawpacket.find('\"')-1]
    
    def send_packet_in_test(self,packet):
        """
        makes sure the test mode is configured and sends a packet
        """
        if self.mode=='TEST' and self.is_test_config:
            query = 'AT+TEST=TXLRPKT, \"00 AA 11 BB 22 CC\"\n'
            answer = self.write(query)
            