"""
This test are meant to be ran on real hardware, it needs 2 lora e5 modules with
factory program in order to use the libraries in this python proyect and one custom
firmware and the aloha protocol.
"""
import pytest
import serial
import src.serial_wioe5 as e5


def test_fails():
    assert False