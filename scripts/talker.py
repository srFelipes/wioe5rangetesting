from src.serial_wioe5 import Wioe5
from src.config.logging import logging
import time

logger = logging.get_logger(logging.MAIN_LOGGER)
id = 0

def splitter(num:int)->list:
    internal =  num
    return_list = []
    if internal == 0:
        return [0]
    else:
        while (internal > 0):
            return_list.append(internal&0xff)
            internal=internal>>8
        return return_list

if __name__=='__main__':
    wio = Wioe5('/dev/ttyUSB0')
    wio.set_mode('TEST')
    wio.config_test()
    num = 0
    to_send = [id]
    while True:
        
        wio.send_packet_in_test(to_send+splitter(num))
        num+=1
        time.sleep(1)