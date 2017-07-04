
[![Build Status](https://travis-ci.org/tchalas/NewsCrawler.svg?branch=master)](https://travis-ci.org/tchalas/NewsCrawler)

# NewsCrawler
Crawler for python subreddit, exposed with a Rest api

# Use case  
This app can be used for extracting and exploring useful data from a web page, in our case the python subreddit. The app is composed by two major modules. The crawler is the program that reads the data from the webpage and stores them in a database after extracting the info we need. The API provides access to the stored data by querying the database to serve the received request.  


# Specifications  
Environment: Linux Ubuntu
Language: Python3        - There was no reason not to use the last python version  
Database: Postgresql     - The schema was clearly relational and I prefer postgres for that type of dbs as it scales quite well  
API: Flask               - Library really useful for simple APIs  
Servers: flask, gunicorn - Gunicorn workers can help flask scale  
Parsing: BeautifulSoup   - Never used it before but really helpful, no second thoughts  
Asynchronous: Celery     - Easy configuration and good performance, really helps web parsing  
Celery queue: RabbitMq   - Tested redis as well and rabbit had a bit better performance  
Profiling: Flower        - Helped me debug a low performance issue  

# Architecture Overview  
There are four python packages in the initial directory. The idea behind the design is that there are two distinct modules, the crawler and the api, that share the database module. The api is built using flask blueprints in order to be easily expandable and client is used to collect the info from the db. The crawler is using celery tasks to parallelize the parsing.  Finally the db comes with a client module in order to allow it to be queried.  

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

# Setup database  
Passing the createdb argument to the manager will drop all the tables and recreate the database, by default called reddit-db.  The database schema is quite simple as there are 1-n user-post, post-comment, user-comment relationships. Postgres by default protects against foreign key violation. By default the credentials are craw/craw.

# Craw  
The crawler works by starting a celery task that will continuously create child tasks. Reddit page splits the posts to odd and even so it was a good chance for parallel processing. The tasks craw_post and craw_comments fill the database with the parsed info, using BeautifulSoup parser.  Only for the case of post the info about score and comment number is updated on the next round of crawling.  

# Serve with gunicorn  
Just execute the gunicorn.sh script. A pool of six copies of the Api will be created  

# API     
url_prefix='/crawl_api'  

Endpoints (all are GET methods)  
/top10points/<post_type>    - Returns top 10 posts by points. <post_type>  can be "discussion", "external", "all"   
/top10commented/<post_type> - Returns top 10 posts by comments. <post_type>  can be "discussion", "external", "all"      
/topsubmitter               - Returns user with the most posts  
/topcommenter               - Returns user with the most comments  
/mostactive                 - Returns user with the most comments+posts  
/posts_by_user/<username>   - Returns all posts by a username  
/posts_user_commented/<username> - Returns all posts a user commented by a username  
/update/<max_page>          - Starts crawling again updating the database  


# Monioring   

You can monitor 1) the celery worker and 2) the flask api requests  

API monitoring with flask_profiler  
Credentials: admin/admin   
Port: http://127.0.0.1:8002/flask-profiler/  

Celery monitoring with flower  
Start server with:  celery -A crawler.crawler_tasks flower   
Port: http://localhost:5555/dashboard  

# TOBEDONE  
Going over reddit comments it can be notices a case where the comment is deleted. The crawler currently ignores that type of comments, the parsing fails and the error is being catch but no info are inserted in the db. The crawler module directly inserts to the db while it should call the a method exposed by the db module. Also the app doesn't currently reacts to user wrong input.
