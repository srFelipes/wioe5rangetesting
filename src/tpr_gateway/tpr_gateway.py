import src.serial_wioe5 as e5
import logging

ALOHA_FREQ = '915'
ALOHA_GATEWAY_POWER = '20'
ALOHA_BANDWIDTH = '500'
ALOHA_CRC = 'ON'
ALOHA_PREAMBLE = '16'
ALOHA_SLOW_DR = {'FREQ': ALOHA_FREQ,
                 'SF': 'SF12',
                 'BANDWIDTH':ALOHA_BANDWIDTH,
                 'TX_PREAMBLE': ALOHA_PREAMBLE,
                 'RX_PREAMBLE': ALOHA_PREAMBLE,
                 'POWER': ALOHA_GATEWAY_POWER,
                 'CRC':'ON',
                 'IQ': 'OFF',
                 'NET': 'OFF'}

class Tpr_gateway:
    def __init__(self, port : str, config: str) -> None:
        self.logger = logging.getLogger(__name__)
        self.wio = e5.Wioe5(port)
        self.configurate(config)
    
    def configurate(self,config:str):
        config_dict = None
        if config == 'slow':
            config_dict = ALOHA_SLOW_DR
        if config_dict:
            self.wio.config_test(frequency=config_dict['FREQ'],
                                 sf=config_dict['SF'],
                                 bandwidth=config_dict['BANDWIDTH'],
                                 tx_preamble=config_dict['TX_PREAMBLE'],
                                 rx_preamble=config_dict['RX_PREAMBLE'],
                                 tx_power=config_dict['POWER'],
                                 crc=config_dict['CRC'],
                                 iq=config_dict['IQ'],
                                 net=config_dict['NET'])