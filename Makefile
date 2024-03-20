.PHONY: verify run clean
run:
	python3 ./runme.py
install:
	virtualenv venv
	source venv/bin/activate
	pip install -r requirements.txt
clean:
	rm -fr *.pem
help:
	python3 ./runme.py --help
verify:
	openssl verify -CAfile dances.tango_ca_cert.pem clt1.dances.tango_cert.pem
	openssl verify -CAfile dances.tango_ca_cert.pem srv1.dances.tango_cert.pem

