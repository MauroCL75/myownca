
'''A script to sign from a working CA'''

from datetime import datetime, timedelta, UTC
import argparse

from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.x509.oid import NameOID

def parser():
    '''The parser'''
    domain = "dances.tango"
    cacert = f"{domain}_ca_cert.pem"
    cakey = f"{domain}_ca_key.pem"

    clt= f"newhost1.{domain}"
    prsr = argparse.ArgumentParser(description='Process some integers.')
    prsr.add_argument('--cacert',
                    help=f"the CA certificate , default is {cacert}", default=cacert)
    prsr.add_argument('--cakey',
                    help=f"the CA certificate , default is {cakey}", default=cakey)
    prsr.add_argument('--host', 
                    help=f'New host to generate. {clt} will be added', default=clt)
    args = prsr.parse_args()
    return args

def mkstuff(cakey, cacert, cn="myclient.dances.tango"):
    '''Generate a private key for the client'''
    
    with open(cakey, "rb") as key_file:
        ca_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
    )
    
    with open(cacert, 'rb') as cert_file:
        pem_data = cert_file.read()

        # Load the certificate
        ca_cert = x509.load_pem_x509_certificate(pem_data)
    
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


def main():
    '''The main'''
    args = parser()
    mkstuff(args.cakey, args.cacert, args.host)

if __name__ == "__main__":
    main()