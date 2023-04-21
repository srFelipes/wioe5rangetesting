from src.serial_wioe5 import Wioe5
from src.config.logging import logging

logger = logging.get_logger(logging.MAIN_LOGGER)

if __name__=='__main__':
    wio = Wioe5('/dev/ttyUSB1')
    wio.set_mode('TEST')
    wio.config_test()
    wio.set_test_crx()
    while True:
        wio.wait_for_packet_in_test()