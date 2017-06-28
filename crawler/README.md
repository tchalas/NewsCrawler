# Delete virtual env  
rm -rf venv  
  
# Create virtual env  
virtualenv -p python3 venv  

# Activate it  
source venv/bin/activate  

# Install requirments
pip3 install -r requirements.txt
