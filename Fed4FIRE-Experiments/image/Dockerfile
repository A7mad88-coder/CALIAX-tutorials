FROM ubuntu:18.04
RUN apt-get update && \
	apt-get install -y python3.8 python3-pip
RUN pip3 install urllib3 influxdb
ADD asvincurl.py /app/curl.py
ENTRYPOINT ["/usr/bin/python3","-u", "/app/curl.py"]