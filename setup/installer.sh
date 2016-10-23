cd /opt
git clone https://github.com/cosmicc/EMS.git
apt update
apt install python python-pip mysql-server python-dev libmysqlclient-dev mysql-client ntp ntpdate rrdtool python-rrdtool lighttpd i2c-tools python-smbus -f
pip install --upgrade pip
pip install MySQL-python 
apt-get autoremove
service mysql restart
cp /opt/EMS/setup/ntp.conf /etc/ntp.conf
service ntp restart
mkdir /opt/rrddata
cp /opt/EMS/setup/modules /etc/modules
rm /var/www/html/* -f
cp /opt/EMS/setup/index.html /var/www/html/index.html
mysql_secure_installation
mysql -u root --password=EMS16 -e 'CREATE DATABASE EMS;'
mysql -u root --password=EMS16 EMS < /opt/EMS/setup/dbinit.sql
