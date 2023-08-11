"""
This test are meant to be ran on real hardware, it needs 2 lora e5 modules with
factory program in order to use the libraries in this python proyect and one custom
firmware and the aloha protocol.
"""
import pytest
import serial
import src.tpr_gateway.tpr_gateway as tpr_gateway
import src.serial_wioe5 as e5

@pytest.fixture
def gateway()->e5.Wioe5:
    for s_port in e5.ports():
        try:
            return tpr_gateway.Tpr_gateway(s_port,'slow').wio
        except:
            pass
    raise Exception("no e5 connected")

@pytest.fixture
def aloha()->serial.Serial:
    for s_port in e5.ports():
        try:
            e5.Wioe5(serial_port=s_port)
        except:
            return  serial.Serial(port=s_port,
                                  baudrate=9600,
                                  timeout= 5)
    raise Exception("no aloha connected")

def test_gateway_successfull(gateway):
    assert True

def test_aloha_present(aloha):
    assert True

def test_aloha_timeout_ack(gateway,aloha):
    gateway.set_test_crx()
    aloha.write(b'GO\n')
    answer = gateway.wait_for_packet_in_test(timeout=10)
    assert 'aloha\n'==answer
    ack = aloha.readline()
    assert ack == 'ACK TIMEOUT\n'

