#!/bin/bash
/usr/bin/mysqld_safe &
sleep 5
mysql -u root -e "source /initial/initial_values.sql"
