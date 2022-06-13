FROM centos:latest
RUN yum install httpd -y
RUN yum install python3 -y
COPY requirements.txt /home
RUN pip3 install -r /home/requirements.txt
COPY WEB_APP Mail_App
WORKDIR Mail_App
ENTRYPOINT ["python3", "app.py"]
EXPOSE 3000 5050
                    
