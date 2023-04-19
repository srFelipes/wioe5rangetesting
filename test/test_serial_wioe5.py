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
    Wioe5(serial_port.port)

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

