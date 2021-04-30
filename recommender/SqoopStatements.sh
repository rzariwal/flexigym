#!/usr/bin/env bash

echo "1.Importing customer data into HBase"
sqoop import --hbase-create-table \
	--hbase-table customer_data \
	--column-family customer \
	--hbase-row-key customer_id \
	--connect jdbc:mysql://localhost:3306/flexigm \
	--table customers \
	-m 1

echo "2.Importing Packages list data into HBase"

sqoop import --hbase-create-table \
	--hbase-table packages_data \
	--column-family package \
	--hbase-row-key package_id \
	--connect jdbc:mysql://localhost:3306/flexigm \
	--table packages \
	-m 1

echo "3.Importing ratings data into HBase"
sqoop import --hbase-create-table \
	--hbase-table ratings_data \
	--column-family rating \
	--hbase-row-key epoch_ms \
	--connect jdbc:mysql://localhost:3306/flexigm \
	--table ratings \
	-m 1

