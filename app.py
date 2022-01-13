from pyzabbix import ZabbixAPI
import csv

zapi = ZabbixAPI("http://zabbix/zabbix")
zapi.login(user="Admin", password="zabbix")

arq = csv.reader(open('hosts.csv'))

# Print hostgroups
for h in zapi.hostgroup.get(output="extend"):
    print(h)

# Print template_ids + names
for h in zapi.template.get(output="extend"):
    print(h['templateid']+' - '+h['name'])

# Add hosts to zabbix
with open("hosts.csv", "r") as csvfile:
    csvreader = csv.DictReader(csvfile)
    for row in csvreader:
        try:
            hostcreation = zapi.host.create(
                host= row["hostname"],
                status= 1,
                interfaces=[{
                    "type": 1,
                    "main": "1",
                    "useip": 1,
                    "ip": row["ip"],
                    "dns": "",
                    "port": row["port"]
                }],
                groups=[{
                    "groupid": row["group_id"]
                }],
                templates=[{
                    "templateid": row["template_id"]
                }]
            )
            print(row["hostname"], 'added to zabbix')
        except:
            continue