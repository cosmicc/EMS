cd /opt
git clone https://github.com/cosmicc/EMS.git
read -n 1 -s -p "Press any key to continue"
timedatectl set-timezone America/New_York
apt update
read -n 1 -s -p "Press any key to continue"
apt upgrade
read -n 1 -s -p "Press any key to continue"
apt install python python-pip mysql-server python-dev libmysqlclient-dev mysql-client ntp ntpdate rrdtool python-rrdtool lighttpd i2c-tools python-smbus iw build-essential linux-headers-generic dkms -f
read -n 1 -s -p "Press any key to continue"
pip install --upgrade pip
read -n 1 -s -p "Press any key to continue"
pip install MySQL-python python-daemon RPi.GPIO config 
apt-get autoremove
read -n 1 -s -p "Press any key to continue"
service mysql restart
read -n 1 -s -p "Press any key to continue"
cp /opt/EMS/setup/ntp.conf /etc/ntp.conf
service ntp restart
read -n 1 -s -p "Press any key to continue"
mkdir /opt/rrddata
cp /opt/EMS/setup/modules /etc/modules
cp /opt/EMS/setup/ems_server.service  /lib/systemd/system/ems_server.service
cp /opt/EMS/setup/statusbar.service  /lib/systemd/system/statusbar.service
cp /opt/EMS/setup/emsreboot.service  /lib/systemd/system/emsreboot.service
cp /opt/EMS/setup/emsshutdown.service  /lib/systemd/system/emsshutdown.service
systemctl enable /lib/systemd/system/ems_server.service
systemctl enable /lib/systemd/system/statusbar.service
systemctl enable /lib/systemd/system/emsreboot.service
systemctl enable /lib/systemd/system/emsshutdown.service
rm /var/www/html/* -f
cp /opt/EMS/setup/index.html /var/www/html/index.html
read -n 1 -s -p "Press any key to continue"
mysql_secure_installation
read -n 1 -s -p "Press any key to continue"
mysql -u root --password=EMS16 -e 'CREATE DATABASE EMS;'
mysql -u root --password=EMS16 EMS < /opt/EMS/setup/dbinit.sql
read -n 1 -s -p "Press any key to continue"
cd /opt/EMS/setup/rt8192cu
make dkms
read -n 1 -s -p "Press any key to continue"
cd /opt/EMS/setup/RTL8188-hostapd/hostapd
make install
