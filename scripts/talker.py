import argparse
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
    parser = argparse.ArgumentParser(description="Script to operate WIO-e5 in coninouos TX form",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f','--frequency', help='lora frequency of operation in Mhz', metavar='')
    parser.add_argument('-sf','--spreading', help='lora spreading factor', metavar='')
    parser.add_argument('-b', '--bandwidth', help='lora bandwidht', metavar='')
    parser.add_argument('-tpr','--txpreamble', help = 'lora number of tx preamble bytes', metavar='')
    parser.add_argument('-rpr','--rxpreamble', help = 'lora number of rx preamble bytes', metavar='')
    parser.add_argument('-p','--power', help = 'lora output power in db', metavar='')
    parser.add_argument('-i','--id', help = 'device id', metavar='')
    parser.add_argument('-t','--time', help = 'period, time between transmisions in seconds', metavar='')
    parser.add_argument('-P', '--port', help='string of the port to open', metavar='')
    parser.add_argument('-s', '--start_num', help='first number to send, it will increase from there', metavar='')
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
    if args.start_num:
        num = int(args.start_num)
    else:
        num = 0
    if args.id:
        id = int(args.id)
    to_send = [id]
    if args.time:
        period = float(args.time)
    else: 
        period = 1
    while True:
        
        wio.send_packet_in_test(to_send+splitter(num))
        num+=1
        time.sleep(period)