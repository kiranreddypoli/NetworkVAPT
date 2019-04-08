import os
import time
from nessrest.ness6rest import Scanner


if not os.path.exists("Reports/Nessus/"):
	os.makedirs("Reports/Nessus/")

Project_name = "nessusscanfolder"
Policy_name = "nessuspolicyname"
scan = Scanner(url="https://nessushost:8834", login="nessususer", password="nessuspassword", insecure=True)
scan._scan_tag(Project_name)
scan.policy_exists(Policy_name)

for file in os.listdir("Discovery/AliveIPs/"):
	scan_name = file.replace('.txt', '')
	targets = ''
	data = open("Discovery/AliveIPs/" + file)
	for ip in data:
		targets = targets + ip
	if targets != '':
		print("Scan starting for " + scan_name)
		scan.scan_add(targets=targets, name=scan_name)
		scan.scan_run()
		scan._scan_status()
		print("Scan completed for the scan " + scan_name)
		time.sleep(30)
		report = "Reports/Nessus/" + file.replace(".txt", ".nessus")
		download = open(report, "w+")
		download.write(scan.download_scan(export_format="nessus"))
		download.close()
		print(scan_name + "report downloaded")
