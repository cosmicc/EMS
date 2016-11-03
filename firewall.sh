#!/bin/bash

iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
iptables --table nat --append POSTROUTING --out-interface wlan1 -j MASQUERADE
iptables --append FORWARD --in-interface wlan0 -j ACCEPT

sysctl -w net.ipv4.ip_forward=1
