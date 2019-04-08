import requests
import os
import time


if not os.path.exists("Reports/Nexpose/"):
	os.makedirs("Reports/Nexpose/")

Project_name = "projectname"
Nexpose_url = 'https://nexposehost:3780'
credentials = {'nexposeccusername': 'nexposeuser', 'nexposeccpassword': 'nexposepassword'}
s = requests.session()
session = s.post(Nexpose_url + "/data/user/login", credentials, verify=False).content.split('"')[5]
headers = {"nexposeCCSessionID": session, "Content-Type": "application/json", "charset": "UTF-8"}

for file in os.listdir("Discovery/AliveIPs/"):
	scan_name = Project_name + "-" + file.replace('.txt', '')
	targets = []
	data = open("Discovery/AliveIPs/" + file)
	for ip in data:
		targets.append(ip)
	if targets != '':
		Create_Site = {
			"name": scan_name, "templateID": "pci-internal-audit", "engineID": "3",
			"includedTargets": {"addresses": targets}
		}
		site_id = s.put(Nexpose_url + "/data/scan/config", json=Create_Site, headers=headers)
		scan_id = s.post(Nexpose_url + "/data/site/" + site_id.content + "/scan", headers=headers)
		print("scan in progress for " + scan_name)
		status = s.get(
			Nexpose_url + "/data/scan/statistics/dyntable?printDocType=0&tableID=scanStatisticsTable&scanid=" +
			scan_id.content)
		scan_status = status.content.split("<td>")[-1].split("</td>")[0]
		while scan_status == "In progress":
			time.sleep(60)
			status = s.get(
				Nexpose_url + "/data/scan/statistics/dyntable?printDocType=0&tableID=scanStatisticsTable&scanid=" +
				scan_id.content)
			scan_status = status.content.split("<td>")[-1].split("</td>")[0]
		print("Scan completed for " + scan_name)
		time.sleep(60)
		generate = s.post(Nexpose_url + "/data/report/configs?generate=true", json={
			"name": scan_name, "owner": "1", "reportTemplateID": "audit-report", "exporterConfig": {"format": "raw-xml"},
			"sites": [int(site_id.content)]}, headers=headers)
		print("Report generated for " + scan_name)
		time.sleep(60)
		Download = s.get(Nexpose_url + "/data/report/configs?sEcho=1&searchPhrase=" + scan_name).content.split('"')
		time.sleep(60)
		report_name = open("Reports/Nexpose/" + scan_name + ".xml", "w+")
		report_name.write(s.get(Nexpose_url + Download[57]).content)
		report_name.close()
		print("Report Downloaded for " + scan_name)
		s.post(Nexpose_url + "/data/site/delete?siteid=" + site_id.content, headers=headers)

s.get(Nexpose_url + "/logout.html", verify=False)
