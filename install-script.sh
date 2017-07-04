#!/bin/bash
rm -rf venv
virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
python db/setup.py
rabbitmqctl add_user myuser mypassword
rabbitmqctl add_vhost myvhost
rabbitmqctl set_user_tags myuser mytag
rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"

SESSION='Crawler'

# -2: forces 256 colors,
byobu-tmux -2 new-session -d -s $SESSION

byobu-tmux rename-window -t $SESSION:0 'Manage'
byobu-tmux send-keys "source venv/bin/activate" C-m
byobu-tmux send-keys "python manage.py createdb" C-m
byobu-tmux send-keys "echo hola" C-m

byobu-tmux new-window -t $SESSION:1 -n 'Celery'
byobu-tmux send-keys "source venv/bin/activate" C-m
byobu-tmux send-keys "celery  -A crawler.crawler_tasks worker --loglevel=info" C-m

byobu-tmux new-window -t $SESSION:2 -n 'Flower'
byobu-tmux send-keys "source venv/bin/activate" C-m
byobu-tmux send-keys "celery -A crawler.crawler_tasks flower" C-m

# Set default window as the dev split plane
byobu-tmux select-window -t $SESSION:0
