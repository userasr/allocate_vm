FROM python:3.7
ADD pyVms /opt/pyVms
RUN pip install -r /opt/pyVms/requirements.txt --user
WORKDIR /opt/pyVms
ENTRYPOINT ["python3", "app/app.py"]
