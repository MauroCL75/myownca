# myownca
A python script to generate CA, servers and clients certificates. It needs python>=3.12, you can use virtual env to install this or the make install target.

# Scripts
At the moment we have:
* runme.py:  a script that generates your own CA key and certificate. A set of servers and clients keys and certificate signed by the CA authority you just made
* sign.py: a script that generates a key and certificate by using an already exisiting CA key and certificate
  
# runme.py
Help:

    usage: runme.py [-h] [--caname CANAME] [--servers SERVERS] [--clients CLIENTS]

    I generate a CA key and certificate then a set of clients and server keys and certificate by using the CA just created.

    options:
    -h, --help         show this help message and exit
    --caname CANAME    the CA name , default is dances.tango
    --servers SERVERS  server separated by commas with no domain. dances.tango will be added
    --clients CLIENTS  clients separated by commas with no domain. dances.tango will be added

# sign.py
Help:

    usage: sign.py [-h] [--cacert CACERT] [--cakey CAKEY] [--host HOST]

    I create a set of certificate and key by using an existing CA key and certificate.

    options:
    -h, --help       show this help message and exit
    --cacert CACERT  the CA certificate , default is dances.tango_ca_cert.pem
    --cakey CAKEY    the CA certificate , default is dances.tango_ca_key.pem
    --host HOST      New host to generate. newhost1.dances.tango will be added