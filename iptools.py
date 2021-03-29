from ip2geotools.databases.noncommercial import DbIpCity
from pyfiglet import Figlet
from tqdm import tqdm
import socket
import time
f = Figlet(font = 'slant') #you can also use '3-d'
print (f.renderText('Ip2tools'))
url = str(input('enter a url: '))
ip = socket.gethostbyname(url)
response = DbIpCity.get(ip,api_key='free')
for i in tqdm(range(100)):
    time.sleep(0.1)
print ('ip: ',ip)
time.sleep(0.1)
print ('city:',response.city)
time.sleep(0.1)
print ('region:',response.region)
time.sleep(0.1)
print ('country:',response.country)

