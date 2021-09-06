FROM centos:latest
RUN yum install net-tools -y
RUN yum install httpd -y
RUN yum install python3 -y
RUN pip3 install colorama
RUN pip3 install validate_email
RUN pip3 install bcrypt
RUN pip3 install pymongo[srv]
RUN pip3 install pytz
RUN pip3 install flask
COPY WEB_APP Mail_App
WORKDIR Mail_App
ENTRYPOINT ["python3", "app.py"]
EXPOSE 3000 5050

