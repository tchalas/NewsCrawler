# Build
[![Build Status](https://travis-ci.org/tchalas/NewsCrawler.svg?branch=master)](https://travis-ci.org/tchalas/NewsCrawler)

# NewsCrawler
Crawler for python subreddit, exposed with a Rest api

# Installing with ansible

# Starting celery worker

# application Manager  

The app is coming with a manager that should be used to invoke the different modules. The available commands are:

manager.py crawl <max_page>  
manager.py createdb  
manager.py serve  
manager.py test  

# Execute tests

# Run the crawler manually

# Starting the API

# Monitoring  

You can monitor 1) the celery worker and 2) the flask api requests

API monitoring with flask_profiler
Credentials: admin/admin  
Port: http://127.0.0.1:8002/flask-profiler/  

Celery monitoring with flowler  
Start server with:  celery -A crawler.crawler_tasks flower   
Port: http://localhost:5555/dashboard  
