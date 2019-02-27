import os
import subprocess
import xml.etree.ElementTree as ET

if not os.path.exists("Discovery/nmap"):
	os.makedirs("Discovery/nmap")

with open('Subnets.txt', 'r') as subnets:
	for subnet in subnets:
		subnet = subnet.replace('\n', '')
		subprocess.call(
			"nmap -sn -n -PE -PS -T5 --disable-arp-ping -vvv --reason -oA Discovery/nmap/"
			+ subnet.replace('/', '_') + " " + subnet
		)

if not os.path.exists("Discovery/AliveIPs"):
	os.makedirs("Discovery/AliveIPs")

for file in os.listdir("Discovery/nmap/"):
	if file.endswith(".xml"):
		xfile = "Discovery/nmap/" + file
		tfile = "Discovery/AliveIPs/" + file.replace("xml", "txt")
		f = open(tfile, "w+")
		tree = ET.parse(xfile)
		root = tree.getroot()
		i = 0
		for host in root.iter('host'):
			a = host.find('status')
			if a.get('state') == 'up':
				b = host.find('address')
				f.write(b.get('addr'))
				f.write("\n")
				i += 1
		print("No. of ips in " + file + " : " + str(i))
		f.close()
