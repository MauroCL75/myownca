'''
lala
'''

from datetime import datetime, timedelta, UTC
import argparse

from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.x509.oid import NameOID

def ca(cn="dances.tango"):
    '''Generate a private key for the Certificate Authority (CA)'''
    ca_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Create a self-signed Certificate Authority (CA) certificate
    ca_cert = x509.CertificateBuilder().subject_name(
        x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, cn),
        ])
    ).issuer_name(
        x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, cn),
        ])
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now(UTC)
    ).not_valid_after(
        datetime.now(UTC) + timedelta(days=365)
    ).public_key(
        ca_key.public_key()
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None),
        critical=True,
    ).sign(ca_key, SHA256())
    
        # Save the private keys and certificates to files
    outpath = cn+"_ca_key.pem"
    with open(outpath, "wb") as f:
        f.write(ca_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    outpath = cn+"_ca_cert.pem"
    with open(outpath, "wb") as f:
        f.write(ca_cert.public_bytes(serialization.Encoding.PEM))
    return [ca_key, ca_cert]

def server(ca_key, cn="my_server.dances.tango"):
    '''Generate a private key for the server'''
    server_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Create a server certificate signed by the CA
    server_cert = x509.CertificateBuilder().subject_name(
        x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, cn),
        ])
    ).issuer_name(
        ca_cert.subject
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now(UTC)
    ).not_valid_after(
        datetime.now(UTC) + timedelta(days=365)
    ).public_key(
        server_key.public_key()
    ).add_extension(
        x509.BasicConstraints(ca=False, path_length=None),
        critical=True,
    ).sign(ca_key, SHA256())
    
    outpath = cn+"_key.pem"
    with open(outpath, "wb") as f:
        f.write(server_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    outpath = cn+"_cert.prm"
    with open(outpath, "wb") as f:
        f.write(server_cert.public_bytes(serialization.Encoding.PEM))

def mkstuff(ca_key, ca_cert, cn="myclient.dances.tango"):
    '''Generate a private key for the client'''
    client_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Create a client certificate signed by the CA
    client_cert = x509.CertificateBuilder().subject_name(
        x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, cn),
        ])
    ).issuer_name(
        ca_cert.subject
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now(UTC)
    ).not_valid_after(
        datetime.now(UTC) + timedelta(days=365)
    ).public_key(
        client_key.public_key()
    ).add_extension(
        x509.BasicConstraints(ca=False, path_length=None),
        critical=True,
    ).sign(ca_key, SHA256())

    outpath = cn+"_cert.pem"
    with open(outpath, "wb") as f:
        f.write(client_cert.public_bytes(serialization.Encoding.PEM))

    outpath = cn+"_key.pem"
    with open(outpath, "wb") as f:
        f.write(client_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

def parser():
    '''The parser'''
    domain = "dances.tango"
    srv="srv1"
    clt="clt1"
    prsr = argparse.ArgumentParser(description='Process some integers.')
    prsr.add_argument('--caname',
                    help=f"the CA name , default is {domain}", default=domain)
    prsr.add_argument('--servers', 
                    help=f'server separated by commas with no domain. {domain} will be added', default=srv)
    prsr.add_argument('--clients', 
                    help=f'clients separated by commas with no domain. {domain} will be added', default=clt)
    args = prsr.parse_args()
    return args

def main():
    '''main'''
    args = parser()
    servers = args.servers.split(",")
    clients = args.clients.split(",")
    print(f"Processing {args.caname}")
    data = ca(args.caname)
    for clt in clients:
        clt = f"{clt}.{args.caname}"
        print(f"processing {clt}")
        mkstuff(data[0], data[1], clt)
    for srv in servers:
        srv = f"{srv}.{args.caname}"
        print(f"processing {srv}")
        mkstuff(data[0], data[1], srv)

if __name__ == "__main__":
    main()
