#!/bin/bash

sudo systemctl stop firewalld
sed -i 's/GSSAPIAuthentication yes/GSSAPIAuthentication no/' /etc/ssh/sshd_config
sed -i 's/#UseDNS yes/UseDNS no/' /etc/ssh/sshd_config

sudo yum update -y
sudo yum install -y -q nano wget bridge-utils unzip curl

echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.conf.all.rp_filter=0" | sudo tee -a /etc/sysctl.conf
echo "net.ipv4.conf.default.rp_filter=0" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
