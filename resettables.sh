echo "Deleting table data..."
mysql -u root --password=EMS16 EMS -e "DELETE FROM d1data; ALTER TABLE d1data AUTO_INCREMENT = 1; DELETE FROM d2data; ALTER TABLE d2data AUTO_INCREMENT = 1; DELETE FROM d3data; ALTER TABLE d3data AUTO_INCREMENT = 1; DELETE FROM d4data; ALTER TABLE d4data AUTO_INCREMENT = 1;"
echo "Complete."
