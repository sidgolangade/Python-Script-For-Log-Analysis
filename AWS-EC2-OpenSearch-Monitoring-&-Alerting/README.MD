## AWS EC2 High CPU Monitoring & Alerting with AWS OpenSearch using Python Script
This Python script allows you to monitor the CPU usage of an AWS EC2 instance and generate alerts in an AWS OpenSearch domain when the CPU usage exceeds a certain threshold. It utilizes the Paramiko and OpenSearchPy libraries to establish connections and interact with the EC2 instance and OpenSearch domain, respectively.

### Prerequisites
- Python 3.x installed on your machine.
- The Paramiko and OpenSearchPy libraries installed. You can install them using `pip install paramiko opensearchpy`
- An AWS EC2 instance running RHEL
- An AWS OpenSearch domain

## Usage
- The script will prompt you to enter the required details, such as the EC2 instance hostname, username, private key path, OpenSearch host, username, and password. Provide the requested information accordingly.

- The script will connect to the EC2 instance and OpenSearch domain, generate a high CPU load on the EC2 instance, monitor its CPU usage, and generate alerts in OpenSearch when the CPU usage exceeds the defined threshold.

- Once the CPU usage exceeds the threshold and an alert is generated, the script will stop monitoring and generate an alert report file named "alert_report.txt" in the same directory.

## Customization
Threshold: 
By default, the script generates an alert when the CPU usage exceeds 20%. You can modify this threshold by changing the value in the if cpu_usage > 20: condition inside the while loop.

CPU Load: 
The script uses the stress-ng command to generate a high CPU load. You can customize the CPU load by modifying the command variable in the "Generating High CPU load on EC2 instance" section. Adjust the --CPU-load option to the desired percentage (0-100).

Note: This script assumes that you have the necessary permissions and access credentials to connect to the AWS EC2 RHEL instance.
