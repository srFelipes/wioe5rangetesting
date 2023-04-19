import pytest
import mock_serial
from src.serial_wioe5 import Wioe5
from src.wio_errors import *

@pytest.fixture
def serial_port()->mock_serial.MockSerial:
    device = mock_serial.MockSerial()
    device.open()
    device.stub(name = 'AT',
                receive_bytes = b'AT\n',
                send_bytes=b'+AT: OK\n')
    return device

@pytest.fixture
def wioe5(serial_port)->Wioe5:
    return Wioe5(serial_port.port) 

def test_at_called(serial_port):
    wioe = Wioe5(serial_port.port)
    assert serial_port.stubs['AT'].called

def test_at_not_ok(serial_port: mock_serial.MockSerial,wioe5):
    serial_port.stub(name = 'AT',receive_bytes = b'AT\n',
                     send_bytes=b'+AT: ERROR(-11)\n')
    try:
        wio = Wioe5(serial_port=serial_port.port)
        assert False
    except Wioe5WrongFormatError:
        assert True
    assert serial_port.stubs['AT'].called

def test_get_mode(serial_port,wioe5):
    serial_port.stub(name='MODE',
                     receive_bytes= b'AT+MODE\n',
                     send_bytes=b'+MODE: LWABP\n')
    assert 'LWABP'==wioe5.get_mode()

def test_get_mode_is_test(serial_port,wioe5):
    serial_port.stub(name='MODE_test',
                     receive_bytes= b'AT+MODE\n',
                     send_bytes=b'+MODE: TEST\n')
    assert 'TEST'==wioe5.get_mode()

def test_get_mode_rn(serial_port,wioe5):
    serial_port.stub(name='MODE',
                     receive_bytes= b'AT+MODE\n',
                     send_bytes=b'+MODE: LWABP\r\n')
    assert 'LWABP'==wioe5.get_mode()

def test_get_mode_as_param(serial_port,wioe5):
    serial_port.stub(name='MODE',
                     receive_bytes= b'AT+MODE\n',
                     send_bytes=b'+MODE: LWABP\n')
    wioe5.get_mode()
    assert 'LWABP'==wioe5.mode

def test_set_mode(serial_port,wioe5):
    serial_port.stub(name='set_mode',
                     receive_bytes= b'AT+MODE=TEST\n',
                     send_bytes=b'+MODE: TEST\n')
    wioe5.set_mode('TEST')
    assert serial_port.stubs['set_mode'].called
    serial_port.stub(name='MODE_test',
                     receive_bytes= b'AT+MODE\n',
                     send_bytes=b'+MODE: TEST\n')
    assert 'TEST'== wioe5.get_mode()

def test_set_mode_returns_1_if_answer_ok(serial_port,wioe5):
    serial_port.stub(name='set_mode',
                     receive_bytes= b'AT+MODE=TEST\n',
                     send_bytes=b'+MODE: TEST\n')
    assert wioe5.set_mode('TEST')
    assert serial_port.stubs['set_mode'].called
    serial_port.stub(name='MODE_test',
                     receive_bytes= b'AT+MODE\n',
                     send_bytes=b'+MODE: TEST\n')
    assert 'TEST'== wioe5.get_mode()

def test_set_mode_returns_0_if_answer_notok(serial_port,wioe5):
    serial_port.stub(name='set_mode',
                     receive_bytes= b'AT+MODE=TEST\n',
                     send_bytes=b'+MODE: LWABP\n')
    assert not wioe5.set_mode('TEST')

def test_set_mode_lwotaa(serial_port,wioe5):
    serial_port.stub(name='set_mode',
                     receive_bytes= b'AT+MODE=LWOTAA\n',
                     send_bytes=b'+MODE: LWOTAA\n')
    
    assert wioe5.set_mode('LWOTAA')
    assert serial_port.stubs['set_mode'].called

def test_invalid_mode(serial_port,wioe5):
    serial_port.stub(name='set_mode',
                     receive_bytes= b'AT+MODE=DEFENSA\n',
                     send_bytes=b'+MODE: ERROR(-1)\n')
    
    try:
        wioe5.set_mode('DEFENSA')
    except Exception as e:
        assert type(e)==Wioe5InvalidParameterError
    assert serial_port.stubs['set_mode'].called

def test_sleep(serial_port,wioe5):
    serial_port.stub(name='set_sleep',
                     receive_bytes= b'AT+LOWPOWER\n',
                     send_bytes=b'+LOWPOWER: SLEEP\n')
    
    wioe5.set_sleep()
    assert serial_port.stubs['set_sleep'].called
    assert 'SLEEP' == wioe5.state

def test_wakeup(serial_port,wioe5):
    serial_port.stub(name='set_sleep',
                     receive_bytes= b'AT+LOWPOWER\n',
                     send_bytes=b'+LOWPOWER: SLEEP\n')
    

    serial_port.stub(name='AT',
                     receive_bytes= b'AT\n',
                     send_bytes=b'+LOWPOWER: WAKEUP\n')
    
    wioe5.set_sleep()
    assert serial_port.stubs['set_sleep'].called
    assert 'SLEEP' == wioe5.state
    wioe5.wakeup()
    assert 'OK' == wioe5.state

def test_config_test_mode(serial_port,wioe5:Wioe5):
    serial_port.stub(name='set_mode',
                     receive_bytes= b'AT+MODE=TEST\n',
                     send_bytes=b'+MODE: TEST\n')
    serial_port.stub(name='set_config',
                     receive_bytes= b'AT+TEST=RFCFG,915,SF12,125,12,15,14,ON,OFF,OFF\n',
                     send_bytes=b'+TEST: RFCFG F:915000000, SF12, BW125K, TXPR:12, RXPR:15, POW:14dBm, CRC:ON, IQ:OFF, NET:OFF\n')
    wioe5.config_test()
    assert 'TEST' == wioe5.mode
    assert serial_port.stubs['set_config'].called

def test_config_test_mode_uses_parameters(serial_port,wioe5:Wioe5):
    serial_port.stub(name='set_mode',
                     receive_bytes= b'AT+MODE=TEST\n',
                     send_bytes=b'+MODE: TEST\n')
    serial_port.stub(name='set_config',
                     receive_bytes= b'AT+TEST=RFCFG,900,SF11,250,13,16,15,OFF,ON,ON\n',
                     send_bytes=b'+TEST: RFCFG F:900000000, SF11, BW250K, TXPR:13, RXPR:16, POW:15dBm, CRC:OFF, IQ:ON, NET:ON\n')
    wioe5.config_test(frequency = '900',
                      sf='SF11',
                      bandwidth = '250',
                      tx_preamble= '13',
                      rx_preamble= '16',
                      tx_power='15',
                      crc='OFF',
                      iq='ON',
                      net='ON')
    assert 'TEST' == wioe5.mode
    assert serial_port.stubs['set_config'].called
    assert {'frequency' : '900000000',
            'sf':'SF11',
            'bandwidth' : 'BW250K',
            'tx_preamble': '13',
            'rx_preamble': '16',
            'tx_power':'15dBm',
            'crc':'OFF',
            'iq':'ON',
            'net':'ON'} == wioe5.test_config_dict

def test_set_crx(serial_port,wioe5:Wioe5):
    serial_port.stub(name='set_mode',
                     receive_bytes= b'AT+MODE=TEST\n',
                     send_bytes=b'+MODE: TEST\n')
    serial_port.stub(name='set_config',
                     receive_bytes= b'AT+TEST=RFCFG,915,SF12,125,12,15,14,ON,OFF,OFF\n',
                     send_bytes=b'+TEST: RFCFG F:915000000, SF12, BW125K, TXPR:12, RXPR:15, POW:14dBm, CRC:ON, IQ:OFF, NET:OFF\n')
    serial_port.stub(name='crx',
                     receive_bytes= b'AT+TEST=RXLRPKT\n',
                     send_bytes=b'+TEST: RXLRPKT\n')
    wioe5.config_test()
    wioe5.set_test_crx()
    assert serial_port.stubs['crx'].called
    assert 'RXLRPKT'==wioe5.test_status

def test_send_a_packet_test(serial_port,wioe5:Wioe5):
    serial_port.stub(name='set_mode',
                     receive_bytes= b'AT+MODE=TEST\n',
                     send_bytes=b'+MODE: TEST\n')
    serial_port.stub(name='set_config',
                     receive_bytes= b'AT+TEST=RFCFG,915,SF12,125,12,15,14,ON,OFF,OFF\n',
                     send_bytes=b'+TEST: RFCFG F:915000000, SF12, BW125K, TXPR:12, RXPR:15, POW:14dBm, CRC:ON, IQ:OFF, NET:OFF\n')
    serial_port.stub(name='send_a_packet',
                     receive_bytes= b'AT+TEST=TXLRPKT, \"00 AA 11 BB 22 CC\"\n',
                     send_bytes=b'+TEST: TXLRPKT \"00AA11BB22CC\"\n'+b'+TEST: TX DONE\n')
    wioe5.config_test()
    wioe5.send_packet_in_test([0x00,0xAA,0x11,0xBB,0x22,0xCC])
    assert serial_port.stubs['send_a_packet'].called