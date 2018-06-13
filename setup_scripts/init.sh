#!/bin/bash -eu
<< commentout
sudo su
mkdir github
cd github
git clone git@github.com:umihico/aws.git
cd /home/ec2-user/github/aws/setup_scripts/
chmod +x ./*.sh
commentout
yum -y update
yum -y install tmux
yum -y install gcc gcc-c++ make git openssl-devel bzip2-devel zlib-devel readline-devel sqlite-devel
<< commentout
./setup_font.sh
./setup_timezone.sh
./setup_git_service.sh
./setup_python.sh
./setup_selenium.sh
commentout
