#!/bin/bash

wget --quiet https://releases.hashicorp.com/consul/0.6.4/consul_0.6.4_linux_amd64.zip
unzip consul_0.6.4_linux_amd64.zip

cat <<EOF > consul.service
[Unit]
Description=consul agent
Requires=network-online.target
After=network-online.target

[Service]
Restart=on-failure
ExecStart=/usr/local/bin/consul agent -server -bootstrap-expect=1 -data-dir=/var/lib/consul -config-dir=/etc/consul.d -node=micro -advertise=10.102.1.20 -client=0.0.0.0 -ui
ExecReload=/bin/kill -HUP $MAINPID
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target
EOF

chmod a+x consul
sudo install -o root -g root consul /usr/local/bin/consul
sudo install -o root -g root -d /etc/consul.d
sudo install -o root -g root -d /var/lib/consul
sudo install -o root -g root consul.service /etc/systemd/system/consul.service

echo '{"service": {"name": "marathon", "tags": ["marathon"], "port": 8080, "check": {"script": "curl localhost:8080 >/dev/null 2>&1", "interval": "10s"}}}' | sudo tee /etc/consul.d/marathon.json
echo '{"service": {"name": "zookeeper", "tags": ["zookeeper"], "port": 2181}}' | sudo tee /etc/consul.d/zookeeper.json

sudo systemctl start consul
sudo systemctl enable consul
