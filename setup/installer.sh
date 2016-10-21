cd /opt
git clone https://github.com/cosmicc/EMS.git
apt update
apt install python python-pip mysql-server python-dev libmysqlclient-dev mysql-client ntp ntpdate -f
pip install --upgrade pip
pip install MySQL-python
apt-get autoremove
service mysql restart
cp /opt/EMS/setup/ntp.conf /etc/ntp.conf
service ntp restart
mysql_secure_installation
mysql -u root --password=EMS16 -e 'CREATE DATABASE EMS;'
mysql -u root --password=EMS16 EMS < /opt/EMS/setup/dbinit.sql
