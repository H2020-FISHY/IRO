#!/bin/bash -e
#IFACES="eth0 eth1"
for i in $INTERFACES_UP
do
echo "bringing up interface $i..."
if ip link set $i up; then
echo "brought $i up successfully"
else
echo "unable to bring up interface $i"
fi
done
echo "Interfaces:"
ip link sh
python /iro/main.py
