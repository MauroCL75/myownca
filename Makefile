.PHONY: verify run clean info sign help
run:
	python3 ./runme.py
info:
	openssl x509 -in clt1.dances.tango_cert.pem  -text -noout
	openssl x509 -in srv1.dances.tango_cert.pem  -text -noout
install:
	virtualenv venv
	source venv/bin/activate
	pip install -r requirements.txt
sign:
	python3 ./sign.py
clean:
	rm -fr *.pem
help:
	python3 ./runme.py --help
verify:
	openssl verify -CAfile dances.tango_ca_cert.pem clt1.dances.tango_cert.pem
	openssl verify -CAfile dances.tango_ca_cert.pem srv1.dances.tango_cert.pem

