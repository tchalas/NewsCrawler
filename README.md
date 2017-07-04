
[![Build Status](https://travis-ci.org/tchalas/NewsCrawler.svg?branch=master)](https://travis-ci.org/tchalas/NewsCrawler)

# NewsCrawler
Crawler for python subreddit, exposed with a Rest api

# Use case  
This app can be used for extracting and exploring useful data from a web page, in our case the python subreddit. The app is composed by two major modules.  
The crawler is the program that reads the data from the webpage and stores them in a database after extracting the info we need. The API provides access to the  
stored data by querying the database to serve the received request.


# Specifications  
language: Python3               | There was no reason not to use the last python version  
Database: Postgresql            | The schema was clearly relational and I prefer postgres for that type of dbs as it scales quite well
API: Flask                      | Library really useful for simple APIs
Servers: flask, gunicorn        | Gunicorn workers can help flask scale
Parsing: BeautifulSoup          | Never used it before but really helpful, no second thoughts
Asynchonous: Celery             | Easy configuration and good performance, really hesps web parsing
Celery queu: RabbitMq           | Tested redis as well and rabbit had a bit better performance
Profiling: Flower               | Helped me debug a low performance issue

# Installing with ansible  
The app is using ansible to provide a cross-platform configuration and to avoid complications on db management.

First you need to install ansible:  
sudo easy_install pip  
sudo pip install ansible  
sudo ln -s /usr/local/bin/ansible-playbook /usr/bin/ansible-playbook  

For local installation you need to add the following two lines to /etc/ansible/hosts  
[local]
localhost ansible_connection=local

# Run with application Manager  

The app is coming with a manager that should be used to invoke the different modules. The available commands are:

manager.py crawl <max_page>  
manager.py createdb  
manager.py serve  
manager.py test  

# Execute tests

# Run the crawler manually

# Starting the API

# Monioring   

You can monitor 1) the celery worker and 2) the flask api requests

API monitoring with flask_profiler
Credentials: admin/admin  
Port: http://127.0.0.1:8002/flask-profiler/  

Celery monitoring with flower  
Start server with:  celery -A crawler.crawler_tasks flower   
Port: http://localhost:5555/dashboard  
