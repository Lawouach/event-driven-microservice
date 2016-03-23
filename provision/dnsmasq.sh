#!/bin/bash

echo server=/consul/127.0.0.1#8600 | sudo tee /etc/dnsmasq.d/10-consul
sudo systemctl restart dnsmasq
