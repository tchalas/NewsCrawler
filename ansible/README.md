# Install ansible with PIP
sudo pip3 install ansible  

# Link to the ansible installation   
sudo ln -s /usr/local/bin/ansible-galaxy /usr/bin/ansible-galaxy  
sudo ln -s /usr/local/bin/ansible-playbook /usr/bin/ansible-playbook  

# For local installation add the following line to /etc/ansible/hosts  
[local]  
localhost ansible_connection=local   

