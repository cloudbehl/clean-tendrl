# clean-tendrl

If your tendrl import cluster is failed and you are not able to import your cluster again then fix the problem mentioned by tendrl and clean the system using this script.

## What Clean-Tendrl  will do?
The clean-tendrl will Stop all the services on the storage and the tendrl server node, clean the required database files and will start the all the services. The tendrl-api password will also be generated after the clean up.

## Steps to clean
- Edit clean_tendrl.py
- Add the ip of server_node by replacing 0.0.0.0 
- Add the ip's of Storage nodes in the list 
- python clean_tendrl.py
