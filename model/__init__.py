from mongoengine import register_connection, connect

connect("air_ticket", host='139.196.96.160', port=27017)
