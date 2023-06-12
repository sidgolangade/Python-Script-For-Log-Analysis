import paramiko
from opensearchpy import OpenSearch
from getpass import getpass
import datetime
import time

# Connect to AWS EC2 instance using Paramiko library
print("To connect an AWS EC2 instance, please enter the below-requested details: \n")

ec2_hostname = input("Enter the hostname: ")
ec2_username = input("Enter the username: ")
ec2_private_key_path = input("Enter the private_key_path: ")

# Establish SSH connection
ec2_client = paramiko.SSHClient()
ec2_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Load the private key
private_key = paramiko.RSAKey.from_private_key_file(ec2_private_key_path)

# Connect to the EC2 instance
ec2_client.connect(hostname=ec2_hostname, username=ec2_username, pkey=private_key)

print("\nConnected to EC2 instance.")

# Connect to AWS OpenSearch using opensearchpy library
print("\nTo connect an AWS OpenSearch domain, please enter the below-requested details: \n")
opensearch_host = input("Enter the opensearch host: ")
opensearch_username = input("Enter the opensearch username: ")
opensearch_password = getpass("Enter the opensearch password: ")

opensearch_client = OpenSearch(hosts=[opensearch_host], http_auth=(opensearch_username, opensearch_password))

print("\nConnected to OpenSearch.")

# Generate high CPU load on EC2 instance
print("\nGenerating High CPU load on EC2 instance...")
#cpu_percentage = input("Enter CPU percentage (0-100): ")
command = f"stress-ng --cpu 1 --cpu-method all --cpu-load 50 --timeout 240"
stdin, stdout, stderr = ec2_client.exec_command(command)
print("\nDone! High CPU load generated.")

def get_cpu_usage():
    command = "top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'"
    stdin, stdout, stderr = ec2_client.exec_command(command)
    cpu_usage = float(stdout.read().decode().strip())
    return cpu_usage

# Monitor CPU usage on OpenSearch and generate an alert
print("\nMonitoring CPU usage and generating alerts...")

while True:
    cpu_usage = get_cpu_usage()
    print(f"\nCurrent CPU usage: {cpu_usage}%")

    if cpu_usage > 20:
        # Generate alert in OpenSearch
        alert = {
            "timestamp": int(time.time() * 1000),
            "message": f"High CPU usage detected: {cpu_usage}%",
            "severity": "high"
        }
        opensearch_client.index(index="alerts", body=alert)

        # Break the loop when cpu_usage exceeds 20
        break
    time.sleep(30)

# Generate an Alert Report file
print("\nGenerating Alert Report file...")

alerts = opensearch_client.search(index="alerts", size=1000)

report_file = open("alert_report.txt", "w")
for hit in alerts["hits"]["hits"]:
    timestamp = hit["_source"]["timestamp"]
    formatted_timestamp = datetime.datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S")
    message = hit["_source"]["message"]
    report_file.write(f"Timestamp: {formatted_timestamp}\nMessage: {message}\n\n")
report_file.close()

print("\nDone! Alert report file generated.")

