#!/bin/bash -eu
<< commentout
sudo su
yum -y install gcc gcc-c++ make git openssl-devel bzip2-devel zlib-devel readline-devel sqlite-devel
cd /home/ec2-user/
mkdir github
git clone https://github.com/umihico/aws.git
cd /home/ec2-user/github/aws/setup_scripts/
chmod +x ./*.sh
commentout
yum -y update
yum -y install tmux
<< commentout
source ./setup_font.sh
source ./setup_timezone.sh
source ./setup_git_service.sh
source ./setup_python.sh
source ./setup_selenium.sh
commentout
