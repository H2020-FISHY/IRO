import requests

# Send mail to localoperator@vendor.com
def send_to_local_operator( subject, message):
    r = requests.post("https://10.15.126.21:5000/actions/report_local_operator", data={'subject':subject, 'message': message})
    print(r.status_code)

# Send mail to owner
def send_to_owner(vin, subject, message):
    r = requests.post("https://192.168.0.103:5000/actions/send_mail", data={'vin':vin,'subject':subject, 'message': message})
    print(r.status_code)

# Deactivate car
def deactivate_car(vin):
    r = requests.delete('https://192.168.0.103:5000/actions/vehicles', data ={'vin':vin})
    print(r.status_code)

# Deactivate car
def deactivate_car_2(vin): # 10.15.126.21:5000
    r = requests.delete('https://192.168.0.103:5000/actions/vehicles/{'+vin+'}')
    print(r.status_code)


 


### TEST 
vin = '22580003-4144-4085-bc3d-6cef407d6706'

print('sending to local operator ..')
send_to_local_operator( '', '')

print('sending to lowner ..')
send_to_owner(vin, '', '')

print('deactivating car ..')
deactivate_car(vin)