import os
import csv
import shutil
import logging
from flask import Flask, jsonify, render_template, send_from_directory
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "VM allocator"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

home = os.path.expanduser('~')
header = ['ip', 'occupied', 'formatted', 'owner', 'key', 'memory', 'storage']
fileName = home + '/vm_reservation.csv'
tmpFileName = home + '/vm_reservation_tmp.csv'
logFile = home + '/vm_reservation.log'

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler(logFile), logging.StreamHandler()],
    format='%(levelname)s:%(asctime)s:%(message)s')


class virtualMac:
    def __init__(self, ip):
        self.ip = ip

    def get(self):
        read = open(fileName, 'r')
        data = csv.DictReader(read)
        for row in data:
            if row['ip'] == self.ip:
                return {'ip': self.ip, 'owner': row['owner'], 'key': row['key'], 'memory': row['memory'],
                        'storage': row['storage']}
        return 'No VM found with given IP.'


@app.route("/")
def spec():
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "VM Allocation"
    return jsonify(swag)


@app.route('/coverage')
def coverage():
    return render_template('templates/index.html', title="Dashboard")


@app.route('/static/<path:path>')
def send_report(path):
    return send_from_directory('static', path)


@app.route('/init')
def init_vms():
    file = open(fileName, 'w')
    writer = csv.writer(file)
    writer.writerow(header)
    for cnt in range(100):
        row = ['10.10.10.' + str(cnt + 1), False, True, '', '', '16GB', '100GB']
        logging.debug(row)
        writer.writerow(row)
    file.close()
    logging.info('Data initialized.')
    return {'message': 'Data initialized.'}


def get_free_vm():
    read = open(fileName, 'r')
    data = csv.DictReader(read)
    for row in data:
        if row['occupied'] == 'False':
            logging.info("Found free VM: " + row['ip'])
            return row['ip']
        else:
            continue
    logging.info("No free VM in the pool. Please try again after sometime.")
    # sys.exit()
    read.close()
    return "No free VM in the pool. Please try again after sometime."


def format_vm(ip):
    '''
    Many possiblities here. for example for windows instance do x else y for linux etc.
    '''
    return {'message': 'Released VM ' + ip + ' and added into the pool.'}


def allocate_vm(uname):
    read = open(fileName, 'r')
    write = open(tmpFileName, 'w')
    writer = csv.writer(write)
    writer.writerow(header)
    writer = csv.DictWriter(write, header)
    data = csv.DictReader(read)
    ip = get_free_vm()
    if ip is None:
        return "No free VM in the pool. Please try again after sometime."
    for row in data:
        if row['ip'] == ip:
            writer.writerow(
                {'ip': row['ip'], 'occupied': True, 'formatted': False, 'owner': uname, 'key': uname, 'memory': '16GB',
                 'storage': '100GB'})
        else:
            writer.writerow(row)
    write.close()
    read.close()
    shutil.move(tmpFileName, fileName)
    if ip != '':
        vm = virtualMac(ip)
        vm_info = vm.get()
        logging.info(vm_info)
        return vm_info


@app.route('/checkin/<uname>/<ip>', methods=['POST'])
def checkin_vm(uname, ip):
    # uname = request.form['uname']
    # ip = request.form['ip']
    flag = True
    # logging.info('Releasing the vm and adding into the pool.')
    read = open(fileName, 'r')
    write = open(tmpFileName, 'w')
    writer = csv.writer(write)
    writer.writerow(header)
    writer = csv.DictWriter(write, header)
    data = csv.DictReader(read)
    for row in data:
        if row['ip'] == ip and row['owner'] == uname:
            writer.writerow(
                {'ip': row['ip'], 'occupied': False, 'formatted': True, 'owner': '', 'key': '', 'memory': '16GB',
                 'storage': '100GB'})
            flag = False

        else:
            writer.writerow(row)
    write.close()
    read.close()
    shutil.move(tmpFileName, fileName)
    if flag:
        return {'message': 'No VM is occupied by user ' + uname + ' with IP ' + ip}
    else:
        return format_vm(ip)


@app.route('/checkout/<uname>', methods=['POST'])
def checkout_vm(uname):
    # uname = request.form['uname']
    logging.info('Checking if there are free VMs in the pool.')
    return {'message': allocate_vm(uname)}


@app.route('/list/<occupied>', methods=['POST'])
def list_vms(occupied):
    # occupied = request.form['occupied']
    file = open(fileName, 'r')
    data = csv.DictReader(file)
    response = {}
    ips = []
    for row in data:
        if row['occupied'] == occupied:
            ips.append(row['ip'])
    file.close()
    response['count'] = len(ips)
    response['ips'] = ips
    return jsonify(response)


@app.route('/occupied/<uname>', methods=['POST'])
def occupied_vms(uname):
    # uname = request.form['uname']
    file = open(fileName, 'r')
    data = csv.DictReader(file)
    response = {}
    ips = []
    for row in data:
        if row['occupied'] == 'True' and row['owner'] == uname:
            ips.append(row['ip'])
    file.close()
    response['count'] = len(ips)
    response['ips'] = ips
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # checkOut_vms('anrathore')
    # checkIn_vms('anrathore', '10.10.10.1')
    # init_vms()
