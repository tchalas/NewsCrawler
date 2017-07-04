
[![Build Status](https://travis-ci.org/tchalas/NewsCrawler.svg?branch=master)](https://travis-ci.org/tchalas/NewsCrawler)

# NewsCrawler
Crawler for python subreddit, exposed with a Rest api

# Use case  
This app can be used for extracting and exploring useful data from a web page, in our case the python subreddit. The app is composed by two major modules.  
The crawler is the program that reads the data from the webpage and stores them in a database after extracting the info we need. The API provides access to the stored data by querying the database to serve the received request.  


# Specifications  
Environment: Linux  
Language: Python3        - There was no reason not to use the last python version  
Database: Postgresql     - The schema was clearly relational and I prefer postgres for that type of dbs as it scales quite well  
API: Flask               - Library really useful for simple APIs  
Servers: flask, gunicorn - Gunicorn workers can help flask scale  
Parsing: BeautifulSoup   - Never used it before but really helpful, no second thoughts  
Asynchronous: Celery     - Easy configuration and good performance, really hesps web parsing  
Celery queue: RabbitMq   - Tested redis as well and rabbit had a bit better performance  
Profiling: Flower        - Helped me debug a low performance issue  

# Installing with ansible  
The app is using ansible to provide a cross-platform configuration and to avoid complications on db management.  

First you need to install ansible:  
sudo apt-get install software-properties-common  
sudo apt-add-repository ppa:ansible/ansible  
sudo apt-get update  
sudo apt-get install ansible  

For local installation you need to add the following two lines to /etc/ansible/hosts  
[local]  
localhost ansible_connection=local  

Now you are ready to deploy with ansible using  
ansible-playbook app-playbook.yml --ask-become   

Before exiting ansible will call the install-script to set up your environment on a byobu session. Execute byobu and you will be ready to play with the app using the manager or by directly starting the gunicorn server (see below)  

# Run commands with application Manager  
The app is coming with a manager that should be used to invoke the different modules. The available commands are:

manager.py crawl <max_page> - Runs the crawler asking him to parse the first <max_page> pages  
manager.py createdb - Creates the db tables
manager.py serve - Starts the api server
manager.py test - invokes the tests  

# Execute tests  
The unitests  can be invoked by executing the following command. The sed command will just set the environment to test  
sed -i.bak 's/^\(env =\).*/\1 test/' config.cfg | python manage.py test   

# Craw  
The crawler works by starting a celery task that will continuously create child tasks. Reddit page splits the posts to odd and even so it was a good chance for parallel processing. The tasks craw_post and craw_comments fill the database with the parsed info, using BeautifulSoup parser.


# Serve with gunicorn  
Just execute the gunicorn.sh script. A pool of six copies of the Api will be created  

# How crawler manually  

# Starting the API  

# Monioring   

You can monitor 1) the celery worker and 2) the flask api requests

API monitoring with flask_profiler
Credentials: admin/admin  
Port: http://127.0.0.1:8002/flask-profiler/  

Celery monitoring with flower  
Start server with:  celery -A crawler.crawler_tasks flower   
Port: http://localhost:5555/dashboard  
