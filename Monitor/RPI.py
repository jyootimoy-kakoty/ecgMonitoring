import requests  
import json
import pytz
import datetime
import random
from time import sleep
from datetime import timedelta

sampleRate =250
url = "http://192.168.43.133:8000/Monitor/RPIPush"
#IST = pytz.timezone('Asia/Kolkata')
time = datetime.datetime.now()#(IST)
#print(IST, time, type(time))
data = {
    'ECGData':
        []
}
#{'sensorID':'HTZ12S001', 'patientID':'PTZ202102270001', 'time': datetime.datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S.%f"), 'data': '633.9791791021592'}
def myconverter(o):
    if isinstance(o, datetime.datetime):
        #print(datetime.datetime)
        return o.__str__()#{}-{}-{}".format(o.year, o.month, o.day)

for i in range(0, sampleRate, 1):
    time += datetime.timedelta(milliseconds = 4)
    sleep(0.004)
    #print(i, time)
    row = {'sensorID':'HTZ12S001', 'patientID':'PTZ202102270001', 'time': myconverter(time), 'data': random.uniform(0, 1023)}
    data['ECGData'].append(row)
r = requests.post(url, data = json.dumps(data))
print (r.text)