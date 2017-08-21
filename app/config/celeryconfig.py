# List of modules to import when the Celery worker starts.
ENV = 'lsm'
# ENV = 'test'
# ENV = 'pro_test'

if ENV == 'lsm':
    broker_url = 'redis://:1q2w3e4r%T@@192.168.2.201:6379/11'
    result_backend = 'redis://:1q2w3e4r%T@@192.168.2.201:6379/12'

    timezone = 'Etc/GMT+8'
    enable_utc = True
elif ENV == 'test':
    broker_url = 'redis://:1q2w3e4r%T@@127.0.0.1:6379/1'
    result_backend = 'redis://:1q2w3e4r%T@@127.0.0.1:6379/2'

    timezone = 'Etc/GMT+8'
    enable_utc = True
elif ENV == 'pro':
    broker_url = 'redis://:1q2w3e4r%T@@127.0.0.1:6379/1'
    result_backend = 'redis://:1q2w3e4r%T@@127.0.0.1:6379/2'

    timezone = 'Etc/GMT+8'
    enable_utc = True
elif ENV == 'pro_test':
    broker_url = 'redis://:1q2w3e4r%T@@192.168.2.201:6379/9'
    result_backend = 'redis://:1q2w3e4r%T@@192.168.2.201:6379/10'

    timezone = 'Etc/GMT+8'
    enable_utc = True

