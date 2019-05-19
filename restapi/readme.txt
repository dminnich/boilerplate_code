##Sample Python Falcon REST API

#install needed things
apt-get install python-pip virtualenv

#create a project in IDE

#create a virtualenv and start using it
virtualenv --no-site-packages restapi
source restapi/bin/activate
cd restapi
mkdir restapi


#install packages in the virtualenv
pip install falcon gunicorn

#start writing the code
touch restapi/__init__.py
touch restapi/app.py
touch restapi/users.py

#test the code
gunicorn --reload restapi.app


