import sys, os
import paramiko


server_node = "0.0.0.0" #ip of tendrl server node
storage_node = ["1.1.1.1"] #ip's of storage node

server_node_services = ["etcd", "tendrl-monitoring-integration", "tendrl-api",
                        "tendrl-notifier", "carbon-cache", "grafana-server",
                        "tendrl-node-agent"]
storage_node_services = ["tendrl-node-agent", "collectd"]

server_files = ["/var/lib/etcd/*", "/var/lib/carbon/whisper/*", "/var/lib/grafana/grafana.db"]

def workon(host, host_type):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username='root')
    if (host_type == "storage"):
	storage_commands(ssh, host)
    elif(host_type == "server"):
	server_commands(ssh, host)
    elif(host_type == "startStorage"):
        start_storage_service(ssh, host)
    elif(host_type == "startServer"):
        start_server_service(ssh, host)

def server_commands(ssh, host):
    #Stopping all the services on server node
    print("\n################# Stopping Tendrl Server(%s) Node Services ###############" %host)
    for node_service in server_node_services:
        cmd = "service %s stop" %node_service
        stdin, stdout, stderr = ssh.exec_command(cmd)
        if(node_service == "grafana-server"):
            print(stdout.readlines())
        else:
            print(stderr.readlines())

    print("\n################# Removing Database Files from Tendrl Server(%s) ###############" %host)
    #Removing the files
    for files in server_files:
       cmd = "rm -rf %s" %files
       stdin, stdout, stderr = ssh.exec_command(cmd)
       print("%s is removed" % files)

def start_server_service(ssh, host):
    print("\n################# Starting Tendrl Server(%s) Node Services ###############" %host)
    #Starting all the services on server node
    for node_service in server_node_services:
        cmd = "service %s start" %node_service
        stdin, stdout, stderr = ssh.exec_command(cmd)
        if(node_service == "grafana-server"):
            print(stdout.readlines())
        else:
            print(stderr.readlines())
    stdin, stdout, stderr = ssh.exec_command("cd /usr/share/tendrl-api; RACK_ENV=production rake etcd:load_admin")
    print("Tendrl Api password is generated", stderr.readlines());

def storage_commands(ssh, host):
    print("\n################# Stopping Storage(%s) Node Services ###############" %host)
    stdin, stdout, stderr = ssh.exec_command("yum remove tendrl-gluster-integration -y --nogpgcheck")
    print(stderr.readlines())
    #Stopping all the services on storage node
    for node_service in storage_node_services:
        cmd = "service %s stop" %node_service
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stderr.readlines())

def start_storage_service(ssh, host):
    print("\n################# Starting Storage(%s) Node Services ###############" %host)
    #Starting all the services on storage node
    for node_service in storage_node_services:
        cmd = "service %s start" %node_service
        stdin, stdout, stderr = ssh.exec_command(cmd)
        print(stderr.readlines())
 
def main():
    #stopping the service
    for storage in storage_node:
        workon(storage, "storage")
    workon(server_node, "server")
    #Starting the service
    for storage in storage_node:
        workon(storage, "startStorage")
    workon(server_node, "startServer")

main()
