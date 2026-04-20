import pytest
from pathlib import Path


from magic_numbers.main import next_magic_num
from drop_test.main import min_num_of_drops
from ipconfig_parser.main import parse_ipconfig
from parking_calculator.main import calculate_fee

def test_next_magic_num():
    assert next_magic_num("808") == "818"
    assert next_magic_num("999") == "1001"
    assert next_magic_num("2133") == "2222"
    assert next_magic_num("1321") == "1331"
    assert next_magic_num("9") == "11"
    
def test_min_num_of_drops():
    assert min_num_of_drops(1, 100) == 100
    assert min_num_of_drops(2, 100) == 14
    assert min_num_of_drops(3, 100) == 9

def test_parking_fee():

    assert calculate_fee("2026-03-30 08:00:00", "2026-03-30 08:20:00") == 0

    assert calculate_fee("2026-03-30 08:00:00", "2026-03-30 10:00:00") == 600

    assert calculate_fee("2026-03-30 08:00:00", "2026-03-30 12:00:00") == 1400

    assert calculate_fee("2026-03-30 08:00:00", "2026-03-31 08:00:00") == 10000

def test_ipconfig_parser():
    sample = """
Ethernet adapter Ethernet 2:

   Connection-specific DNS Suffix  . : 
   Description . . . . . . . . . . . : Intel(R) Ethernet Connection (16) I219-LM
   Physical Address. . . . . . . . . : E1-17-17-17-17-E1
   DHCP Enabled. . . . . . . . . . . : Yes
   IPv4 Address. . . . . . . . . . . : 192.168.0.10(Preferred)
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.0.1
   DNS Servers . . . . . . . . . . . : 8.8.8.8
                                       8.8.4.4
"""
    result = parse_ipconfig(sample)
    assert len(result) == 1
    adapter = result[0]
    assert adapter["adapter_name"] == "Ethernet adapter Ethernet 2"
    assert adapter["ipv4_address"] == "192.168.0.10"
    assert adapter["dhcp_enabled"] == "Yes"
    assert adapter["default_gateway"] == "192.168.0.1"
    assert "8.8.8.8" in adapter["dns_servers"]
    assert "8.8.4.4" in adapter["dns_servers"]
