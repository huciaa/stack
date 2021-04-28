sudo yum install python37
sudo yum install git
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user

pip install requests
pip install datetime
pip install bs4
pip install wget
pip install pandas
pip install py7zr

curl https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

git clone https://github.com/huciaa/stack.git

aws s3 ls s3://stackdev1csv --recursive >> csv_files
aws s3 ls s3://stackdev1 --recursive >> xml_files

#!/bin/sh
aws s3 mv /home/ec2-user/unpack s3://stackdev2 --recursive
 
