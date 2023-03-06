import os, paramiko, time, requests, json, ipfsApi
import config
#from ipfsInteraction import *

# Set details to log into machine using ssh
#print("Log into machine")
#machine_usr = input("Enter machine user: ")
#machine_pass = input("Enter machine password: ")
#machine_name = input("Enter the device name: ")
#host = "192.168.0.118"
#BASE_URL = "http://127.0.0.1:8510/v2/"

new_machine = {
        "description": "Machine Create by Manufacturer",
        "endpoint": config.DEVICE_IP + ":8530",
        "hostname": "pi",
        "protocol": "A10HTTPREST",
        "type": [
            "tpm2.0"
        ],
    }

ipfs_hash = "5h4ghJEkg83gneugHEI"

def registerMachine(userName, password, deviceName):

    new_machine["name"] = deviceName

    print("Creating Initial Session")
    ek_pub, ak_pub = initialSession(userName, password)

    tpm0 = {
        "akhandle": "0x810100aa",
        "akname": "empty",
        "akpem": ak_pub,
        "ekhandle": "0x810100ee",
        "ekname": "empty",
        "ekpem": ek_pub
    }

    print("Adding Element to A10")
    item_id = addNewElement(tpm0)

    print("Adding Item to IPFS")
    #ipfs_hash = storeInIPFS(deviceName, ek_pub, ak_pub)

    print("Storing in NVRAM")
    storeDataNVRAM(userName, password, item_id, ipfs_hash)

    print("Updating Element in A10")
    updateElement(item_id, ipfs_hash)

    print("End")

session = paramiko.SSHClient()

# inital connection to device which creates ek/ak keys and gets
# an initial quote from the device
def initialSession(userName, password):

    tpm_quote = "sudo tpm2_quote -c 0x81010003 -l sha256:0,1,2,3,4 -m quote.msg -s quote.sig -g sha256 -q 123456 -o pcrs.out"

    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    session.connect(
        hostname=config.DEVICE_IP,
        username=userName,
        password=password
    )

    stdin, stdout, stderr = session.exec_command('bash david/provisionDevice')

    print(stdout.read().decode())

    # read ek and ak public keys
    session.exec_command("sudo tpm2_readpublic -c 0x810100EE -o ek.pem -f pem")
    session.exec_command("sudo tpm2_readpublic -c 0x810100AA -o ak.pem -f pem")

    ekpem_in, ekpem_out, ekpem_err = session.exec_command("sudo cat ek.pem")
    akpem_in, akpem_out, akepm_err = session. exec_command("sudo cat ek.pem")

    ek_pem = ekpem_out.read().decode()
    ak_pem = akpem_out.read().decode()

    print("In Initial Session")
    print(ek_pem)
    print(ak_pem)


    # q_out -> initial quote after device is first created
    q_in, q_out, q_err = session.exec_command(tpm_quote)

    print(q_out.read().decode())

    time.sleep(0.5)

    session.close()

    return ek_pem, ak_pem

# Creates PUT request to store the device as an element in A10
def addNewElement(tpm0):

    #new_machine["ek ak pub"] = ek + ak

    json_object = json.loads("{ek + ak}")

    new_machine["tpm2"] = {"tpm0": tpm0}

    # Put new element to a10rest
    new_machine["ek"] = "0x810100EE"
    new_machine["ak"] = "0x810100AA"

    post_r = requests.post(config.BASE_URL + "element", json=new_machine)

    item_id = post_r.json()['itemid']

    new_machine["itemid"] =  item_id

    return item_id


def storeInIPFS(machine_name, ek_pub, ak_pub):

    print(ek_pub)

    new_machine["ekPub"] = ek_pub
    new_machine["akPub"] = ak_pub

    api = ipfsApi.Client("127.0.0.1", 5001)
    # Create a directory to store json file (should probable use /tmp)

    home_dir = os.path.expanduser('~')

    if os.path.exists(home_dir + "/machineFiles"):
        print("Directory Already Exists")
    else:
        os.mkdir(home_dir + "/machineFiles")


    machine_file = open(home_dir + "/machineFiles/" + machine_name + ".json", "w")

    json.dump(new_machine, machine_file)

    res = api.add(home_dir + "/machineFiles/" + machine_name + ".json")
    ipfs_hash = str(res[0]["Hash"])

    #ipfs_hash = store_file(home_dir + "/machineFiles/" + machine_name + ".json")

    print(ipfs_hash)
    print(new_machine)

    new_machine["ipfs"] = ipfs_hash

    return ipfs_hash

# connects to device and stores itemID and IPFS hash in NVRAM
def storeDataNVRAM(userName, password, itemId, ipfsHash):

    session.connect(
        hostname=config.DEVICE_IP,
        username=userName,
        password=password
    )

    # Storing item_id in nvram
    session.exec_command('tpm2_nvdefine 0x15000a1 -C o -s 64')
    itemin, itemout, itemderr = session.exec_command('echo ' + itemId  + ' > itemID')
    itemin, itemout, itemerr = session.exec_command('tpm2_nvwrite 0x15000a1 -C o -i itemID')

    # Storing ipfs_hash in nvram
    session.exec_command('tpm2_nvdefine 0x15000a2 -C o -s 64')
    ipfsin, ipfsout, ipfserr = session.exec_command('echo ' + ipfsHash + ' > ipfsID')
    ipfsin, ipfsout, ipfserr = session.exec_command('tpm2_nvwrite 0x15000a2 -C o -i ipfsID')

    itemin, itemout, itemerr = session.exec_command('tpm2_nvread 0x15000a1 -C o')
    ipfssin, ipfsout, ipfserr = session.exec_command('tpm2_nvread 0x15000a2 -C o')

    print(itemout.read().decode())
    print(ipfsout.read().decode())


    time.sleep(0.5)

    session.close()


def updateElement(itemId, ipfsHash):
    new_machine["ipfs"] = ipfsHash
    put_r = requests.put(config.BASE_URL + "element/" + itemId, json=new_machine)


#registerMachine(machine_usr, machine_pass, machine_name)