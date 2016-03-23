#!/bin/bash

sudo rpm -i http://repos.mesosphere.io/el/7/noarch/RPMS/mesosphere-el-repo-7-3.noarch.rpm
sudo yum -y install mesos marathon mesosphere-zookeeper


# Zookeeper
export ZOOKEEPER_ID=1
echo $ZOOKEEPER_ID | sudo tee -a /var/lib/zookeeper/myid
echo "server.$ZOOKEEPER_ID=$MYIP:2888:3888" | sudo tee -a /etc/zookeeper/conf/zoo.cfg
sudo systemctl start zookeeper
sudo systemctl enable zookeeper


# Master
export MESOS_MASTER=$MYIP
echo zk://$MESOS_MASTER:2181/mesos | sudo tee /etc/mesos/zk
echo 1 | sudo tee /etc/mesos-master/quorum
sudo systemctl daemon-reload
sudo systemctl restart mesos-master


# Slave
echo '5mins' | sudo tee /etc/mesos-slave/executor_registration_timeout
cat <<EOF > mesos-slave-containerizers.conf
[Service]
Environment=MESOS_CONTAINERIZERS=docker,mesos
Environment=MESOS_DOCKER_SOCKET=/var/run/docker.sock
EOF
echo 'ports(*):[1025, 60000]' | sudo tee /etc/mesos-slave/resources

sudo install -o root -g root -d /etc/systemd/system/mesos-slave.service.d
sudo install -o root -g root mesos-slave-containerizers.conf /etc/systemd/system/mesos-slave.service.d

# let's change marathon's default port which
# conflicts with our gateway
sudo install -o root -g root -d /etc/marathon/conf
echo 8079 | sudo tee /etc/marathon/conf/http_port

echo zk://$MESOS_MASTER:2181/mesos | sudo tee /etc/mesos/zk
sudo systemctl daemon-reload
sudo systemctl restart mesos-slave marathon
