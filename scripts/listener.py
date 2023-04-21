import argparse
from src.serial_wioe5 import Wioe5
from src.config.logging import logging

logger = logging.get_logger(logging.MAIN_LOGGER)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description="Script to operate WIO-e5 in coninouos TX form",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f','--frequency', help='lora frequency of operation in Mhz', metavar='')
    parser.add_argument('-sf','--spreading', help='lora spreading factor', metavar='')
    parser.add_argument('-b', '--bandwidth', help='lora bandwidht', metavar='')
    parser.add_argument('-tpr','--txpreamble', help = 'lora number of tx preamble bytes', metavar='')
    parser.add_argument('-rpr','--rxpreamble', help = 'lora number of rx preamble bytes', metavar='')
    parser.add_argument('-p','--power', help = 'lora output power in db', metavar='')
    parser.add_argument('-P', '--port', help='string of the port to open', metavar='')
    args = parser.parse_args()

    if args.port:
        wio = Wioe5(args.port)
    else:
        wio = Wioe5('/dev/ttyUSB0')

    wio.set_mode('TEST')
    argument_list = ['915', 
                    'SF12',
                    '125',
                    '12',
                    '15',
                    '14',
                    'ON',
                    'OFF',
                    'OFF']
    if args.frequency:
        argument_list[0] = args.frequency
    if args.spreading:
        argument_list[1] = args.spreading
    if args.bandwidth:
        argument_list[2] = args.bandwidth
    if args.txpreamble:
        argument_list[3] = args.txpreamble
    if args.rxpreamble:
        argument_list[4] = args.rxpreamble
    if args.power:
        argument_list[5] = args.power
    wio.config_test(*tuple(argument_list))
    wio.set_test_crx()
    while True:
        wio.wait_for_packet_in_test()