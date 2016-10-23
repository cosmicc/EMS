cd /opt
git clone https://github.com/cosmicc/EMS.git
apt update
apt upgrade
apt install python python-pip mysql-server python-dev libmysqlclient-dev mysql-client ntp ntpdate rrdtool python-rrdtool lighttpd i2c-tools python-smbus -f
pip install --upgrade pip
pip install MySQL-python python-daemon 
apt-get autoremove
service mysql restart
cp /opt/EMS/setup/ntp.conf /etc/ntp.conf
service ntp restart
mkdir /opt/rrddata
cp /opt/EMS/setup/modules /etc/modules
cp /opt/EMS/setup/ems_server.service  /lib/systemd/system/ems_server.service
cp /opt/EMS/setup/lcdreboot /etc/init.d/lcdreboot
cp /opt/EMS/setup/lcdshutdown /etc/init.d/lcdshutdown
ln -s ../init.d/lcdreboot K00lcdreboot
ln -s ../init.d/lcdreboot K00lcdshutdown
ln -s /lib/systemd/system/ems_server.service /etc/systemd/system/ems_server.service
rm /var/www/html/* -f
cp /opt/EMS/setup/index.html /var/www/html/index.html
mysql_secure_installation
mysql -u root --password=EMS16 -e 'CREATE DATABASE EMS;'
mysql -u root --password=EMS16 EMS < /opt/EMS/setup/dbinit.sql
