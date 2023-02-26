import os, paramiko, time, requests, json
from ipfsInteraction import *

# Set details to log into machine using ssh
print("Log into machine")
machine_usr = input("Enter machine user: ")
machine_pass = input("Enter machine password: ")
machine_name = input("Enter the device name: ")
host = "192.168.0.118"
BASE_URL = "http://127.0.0.1:8510/v2/"


new_machine = {
    "description": "Machine Create by Manufacturer",
    "endpoint": "http://127.0.0.1:8530",
    "name": machine_name,
    "protocol": "A10HTTPREST",
    "type": [
        "tpm2.0"
    ],
}

tpm_quote = "sudo tpm2_quote -c 0x81010003 -l sha1:0,1,2,3,4,5,6,7,8,9 -m quote.msg -s quote.sig -g sha256 -q 123456 -o pcrs.out"

session = paramiko.SSHClient()

session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

session.connect(
    hostname=host,
    username=machine_usr,
    password=machine_pass
)

stdin, stdout, stderr = session.exec_command('./AttestationEngine/apps/enroller/minimalclient/provisionMinimal')

print(stdout.read().decode())

# read ek and ak public keys
ek_in, ek_out, ek_err = session.exec_command("sudo tpm2_readpublic -c 0x810100EE -o ek.pem -f pem")
ak_in, ak_out, ak_err = session.exec_command("sudo tpm2_readpublic -c 0x810100EE -o ek.pem -f pem")

print(ek_out.read().decode())
print(ak_out.read().decode())

# q_out -> initial quote after device is first created
q_in, q_out, q_err = session.exec_command(tpm_quote)

print(q_out.read().decode())

time.sleep(0.5)

session.close()

# Put new element to a10rest
new_machine["ek"] = "0x810100EE"
new_machine["ak"] = "0x810100AA"

post_r = requests.post(BASE_URL + "element", json=new_machine)


item_id = post_r.json()['itemid']

new_machine["itemid"] =  item_id

# Add new_machine to IPFS

#machine_json = json.dumps(new_machine)

home_dir = os.path.expanduser('~')

if os.path.exists(home_dir + "/machineFiles"):
    print("Directory Already Exists")
else:
    os.mkdir(home_dir + "/machineFiles")



machine_file = open(home_dir + "/machineFiles/" + machine_name + ".json", "w")

json.dump(new_machine, machine_file)

ipfs_hash = store_file(home_dir + "/machineFiles/" + machine_name + ".json")

print(ipfs_hash)
print(new_machine)

new_machine["ipfs"] = ipfs_hash


session.connect(
    hostname=host,
    username=machine_usr,
    password=machine_pass
)

print(item_id)

# Storing item_id in nvram
session.exec_command('tpm2_nvdefine 0x15000a1 -C o -s 64')
itemin, itemout, itemderr = session.exec_command('echo ' + item_id  + ' > itemID')
itemin, itemout, itemerr = session.exec_command('tpm2_nvwrite 0x15000a1 -C o -i itemID')

# Storing ipfs_hash in nvram
session.exec_command('tpm2_nvdefine 0x15000a2 -C o -s 64')
ipfsin, ipfsout, ipfserr = session.exec_command('echo ' + ipfs_hash + ' > ipfsID')
ipfsin, ipfsout, ipfserr = session.exec_command('tpm2_nvwrite 0x15000a2 -C o -i ipfsID')

print(stdout.read().decode())

itemin, itemout, itemerr = session.exec_command('tpm2_nvread 0x15000a1 -C o')
ipfssin, ipfsout, ipfserr = session.exec_command('tpm2_nvread 0x15000a2 -C o')

print(itemout.read().decode())
print(ipfsout.read().decode())


time.sleep(0.5)

session.close()



put_r = requests.put(BASE_URL + "element/" + item_id, json=new_machine)

