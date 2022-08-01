import json
import pytest
import logging
import ipaddress
from app.app import get_free_vm, allocate_vm, format_vm



# Test GET /init. This call initializes the csv file with unoccupied VMs.
def test_init(app, client):
    del app
    res = client.get('/init')
    assert res.status_code == 200
    expected = {'message': 'Data initialized.'}
    assert expected == json.loads(res.get_data(as_text=True))


# Test POST /list/<occupied>. This call lists count and IP of occupied/unoccupied VMs.
@pytest.mark.parametrize("occupied", ["False"])
def test_list(app, client, occupied):
    del app
    res = client.post(f'/list/{occupied}')
    logging.info(res.json)
    assert res.status_code == 200
    assert "count" in res.json


# Test POST /occupied/<uname>. This call lists count and IPs of occupied VMs by provided user name.
@pytest.mark.parametrize("uname", ["ankit"])
def test_occupied(app, client, uname):
    del app
    res = client.post(f'/occupied/{uname}')
    logging.info(res.json)
    assert res.status_code == 200
    assert "count" in res.json


# Test POST /checkout/<uname>. This call reserves a VM for provided user.
@pytest.mark.parametrize("uname", ["ankit"])
def test_checkout(app, client, uname):
    del app
    res = client.post(f'/checkout/{uname}')
    assert res.status_code == 200
    #logging.info(res.json['message'])
    if "ip" in res.json['message']:
        assert ipaddress.ip_address(res.json["message"]["ip"])
    else:
        assert "No free VM in the pool. Please try again after sometime." in res.json["message"] or "No VM found with given IP." in res.json["message"]


# Test POST /checkin/<uname>/<ip>. This call releases a VM based on provided from provided user.
@pytest.mark.parametrize("uname,ip", [("ankit", "10.10.10.2")])
def test_checkin(app, client, uname, ip):
    del app
    res = client.post(f'/checkin/{uname}/{ip}')
    logging.info(res.json['message'])
    assert res.status_code == 200
    assert "Released VM" in res.json["message"] or "No VM is occupied by user" in res.json["message"]


# Test: Get a free VM's IP.
def test_get_free_vm(app, client):
    res = get_free_vm()
    print(res)
    assert "No free VM in the pool. Please try again after sometime." in res or ipaddress.ip_address(res)


# Test: Returns an IP if found an unoccupied VM else notifies user about unavailability of free VMs.
@pytest.mark.parametrize("uname", ["ankit"])
def test_allocate_vm(app, client, uname):
    res = allocate_vm(uname)
    #assert res == "No free VM in the pool. Please try again after sometime." or ipaddress.ip_address(res)
    if "ip" in str(res):
        assert ipaddress.ip_address(res["ip"])
    else:
        assert "No free VM in the pool. Please try again after sometime." in res or "No VM found with given IP." in res


# Test: Formats a VM based on provided IP
@pytest.mark.parametrize("ip", ["10.10.10.1"])
def test_format_vm(app, client, ip):
    res = format_vm(ip)
    assert "Released VM" in res["message"]
