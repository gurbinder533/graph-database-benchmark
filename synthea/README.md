This article documents the details on how to reproduce the graph database benchmark result on TigerGraph Enterprise Edtion v2.5.3

Hardware & Major enviroment
================================
TigerGraph Machines : Dell C6525 
JMeter Machine : Dell R6525
OS Ubuntu Server 18.04 LTS
Java build 1.8.0_144-b01 (follow http://www.webupd8.org/2012/09/install-oracle-java-8-in-ubuntu-via-ppa.html)
JMeter version : 5.2.1 (https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.2.1.tgz)

You need to install the following modules
$ sudo apt-get update
$ sudo apt-get install python-pip python-dev build-essential 
$ sudo pip install --upgrade pip 
$ sudo pip install --upgrade virtualenv 
$ sudo pip install tornado
$ sudo pip install neo4j-driver
$ sudo pip install requests
$ sudo apt-get install libcurl4-openssl-dev
$ sudo apt-get install libssl-dev
$ sudo pip install pycurl

Machine size specifications
==============================
C6525 :
128 CPU 
1TB Mem
1TB disk

R6525:
128 CPU
2TB Mem
1TB disk

Data set
=========
Sample data set is provided under /synthea/data/ directory

If generating synthetic data using synthea, you will need to do the following:
git clone https://github.com/synthetichealth/synthea.git
download https://github.com/synthetichealth/synthea/releases/download/master-branch-latest/synthea-with-dependencies.jar

Utilize the provided scripts (find here : /synthea/synthea-data-generation/) to automate the data generation process. 

bash generate1_data.sh - this will generate 1 TB data per entry
python copyall.py - this will move all the generated files into one location on the disk. You can bypass this step by using the sample data files we have provided.
NOTE: You may want to edit the file locations within the python script.


TigerGraph Version
===================
- TigerGraph Enterprise Editon v.2.5.3

Install TigerGraph 
===================
- installation video reference here https://www.youtube.com/watch?v=q-vAioBUwkI&t=3s
- make sure all ports are open to commmunication between each machine in the cluster

Open READ and WRITE permission for TigerGraph User
==================================================
If you installed TigerGraph with the default user, it's tigergraph.

Grant Read and Write permission to the tigergraph user on 
- raw data folder.
- the script folder. 

- use the following command to check TigerGraph service 
gadmin status 



Schema Setup
==============
As TigerGraph user, cd to the directory containing schema.gsql
Run this command to set up the graph schema: gsql schema.gsql

Note: This step may take a minute or two.

Load Data
==========
In the file distributed_loading.gsql, you will need to change the directory of each file to their respective file locations (lines 5-19).  
e.g. "ALL:/nvme1/synthea/output/Final/allergies.csv" -> “/home/tigergraph/datafiles/allergies.csv”

Once you have provided the correct data file locations, use this command to create the loading job and begin loading: 
gsql distributed_loading.gsql

Install Queries
================
Run this command to create and install all the included queries:
gsql queries.gsql



JMeter Machine Setup
=======================
JMeter is installed and run from a machine outside the cluster, but in the same region. 
This allows the TigerGraph machines to operate all full capacity and minimize latency for query calls.

After preparing the machine, download JMeter.
For our test, we used JMeter v5.2.1. Download here : https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-5.2.1.tgz

JMeter Testing
===============
We have provided the file DistributedTPm8.jmx for testing. You can create other tests you may want to run through a local instance of JMeter using the JMeter UI.
Get started here : https://www.blazemeter.com/blog/getting-started-jmeter-basic-tutorial

You will need to create a pool of data entried to query for, we simply need the patient IDs from the generated data.
awk -F "\"*,\"*" '{print $1}' patients.csv >> patients_sample.csv

In the DistributedTPm8.jmx file, replace the follwing :
MACHINE_IP_HERE = The public IP address of each machine in the cluster. We want to hit each machine to ensure maximum concurrency.
FILE_LOCATION = the absolute file path to your patients_sample.csv

Using the provided JMeter test file, run the command to begin the test in the /jmeter/bin/ folder:
./jmeter.sh -n -t ~/DistributedTPm8.jmx

