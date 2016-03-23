# -*- mode: ruby -*-
# # vi: set ft=ruby :
require 'fileutils'
Vagrant.require_version ">= 1.6.0"

Vagrant.configure("2") do |config|
  config.vm.box = "bento/centos-7.1"
  
  config.vm.define vm_name = "microservices-demo" do |master|
    master.vm.network "private_network", ip: "10.102.1.20"
    master.vm.network "forwarded_port", guest: 5050, host: 5050  # mesos
    master.vm.network "forwarded_port", guest: 8079, host: 8079  # marathon
    master.vm.network "forwarded_port", guest: 8500, host: 8500  # consul
    master.vm.network "forwarded_port", guest: 8080, host: 8080  # bookshelf gateway
  
    master.vm.provision :shell, inline: <<-SHELL
      hostnamectl set-hostname #{vm_name}
      echo 10.102.1.20 #{vm_name} >> /etc/hosts
      echo export MYIP=10.102.1.20 >> /etc/profile.d/vagrant.sh
    SHELL
    
    master.vm.provider :virtualbox do |vb|
      vb.gui = true
      vb.memory = 3072
      vb.cpus = 1
      vb.customize ["modifyvm", :id, "--ioapic", "on"]
      vb.customize ["modifyvm", :id, "--vram", "24"]
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    end
    
    master.vm.provision "shell", path: "provision/sys.sh"
    master.vm.provision "shell", path: "provision/docker.sh"
    master.vm.provision "shell", path: "provision/mesos.sh"
    master.vm.provision "shell", path: "provision/consul.sh"
    master.vm.provision "shell", path: "provision/dnsmasq.sh"
  end
end
