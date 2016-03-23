#!/bin/bash

curl -sSL https://get.docker.com/ | sudo sh
sudo usermod -aG docker vagrant

sudo sed -i 's|ExecStart=/usr/bin/docker daemon -H fd://|EnvironmentFile=-/etc/sysconfig/docker\nExecStart=/usr/bin/docker daemon -H fd:// -H unix:///var/run/docker.sock \$OPTIONS|' /usr/lib/systemd/system/docker.service

echo OPTIONS=\"--dns $MYIP --dns-search service.consul\" | sudo tee -a /etc/sysconfig/docker
sudo systemctl enable docker
sudo systemctl start docker

# let's pull images right now so the
# first deployment is faster
docker pull ciscocloud/mesos-consul
docker pull wurstmeister/zookeeper
docker pull wurstmeister/kafka
docker pull lawouach/bookshelf:0.1
