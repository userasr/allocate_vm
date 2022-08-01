# VM Allocator

This is an API based tool which helps users reserve/release VMs from/to a pool of VMs.

### Prerequisites:

1. python3. recommended: 3.7.3
2. Install the python required libraries using command: `pip install -r requirements.txt`
3. Docker if you are using docker image to run the tool.

### Run on CLI: 
Execute the following command within `pyVms` project directory.

    nohup python3 app/app.py &


### Run on Docker:
To create the docker image run the following command:

    docker build -t dockerasr/vms:1.0.0 .

To create the container run the following command:

    docker run -d --name vms -p 5000:5000 dockerasr/vms:1.0.0

### Usage:
To interact with the API, you can use swagger UI : http://localhost:5000/swagger/

To run the tests and generate code coverage please execute the following command within `pyVms` project directory:

    python3 -m pytest --cov=app --cov-report html:app/static/templates tests/

If you are running on Docker then get inside the docker container using following command and run the above command within `pyVms` project directory:

    docker exec -it vms /bin/bash

To see the coverage report. Go to browser and hit this URL : http://localhost:5000/static/templates/index.html
