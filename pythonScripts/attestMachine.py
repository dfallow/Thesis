import requests, time, paramiko


# Set details to log into machine using ssh
print("Log into machine")
machine_usr = input("Enter machine user: ")
machine_pass = input("Enter machine password: ")
machine_name = input("Enter the device name: ")
host = "192.168.0.118"
BASE_URL = "http://127.0.0.1:8510/v2/"


# Policy ID's

medCRTM = "4b6a2a69-ce8e-4a0c-bc69-d798e5e7fa12"
medSRTM = "1746e0fd-984c-4fe6-bd50-983e4a5e7496"

tpm_quote = "sudo tpm2_quote -c 0x81010003 -l sha1:0,1,2,3,4,5,6,7,8,9 -m quote.msg -s quote.sig -g sha256 -q 123456 -o pcrs.out"

session = paramiko.SSHClient()

session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

session.connect(
    hostname=host,
    username=machine_usr,
    password=machine_pass
)

# Get element ID

itemin, itemout, itemerr = session.exec_command('tpm2_nvread 0x15000a1')

item_id = itemout.read().decode()
print(item_id)

time.sleep(0.5)

session.close()

post_session = requests.post(BASE_URL + "sessions/open")

session_id = post_session.json()['itemid']
print(post_session.json()['itemid'])

###

# Session is open hear
item_id = "d9bbc32b-feac-406f-b494-b4b3f3ffa396"
attest_json = {
    'eid': item_id,
    'pid': medCRTM,
    'cps': "",
    'sid': session_id
}

post_attest = requests.post(BASE_URL + "attest", json=attest_json)

print(post_attest)
#print(post_attest.json())


###

close_session = requests.delete(BASE_URL + "session/" + session_id) 

print(close_session.json())
