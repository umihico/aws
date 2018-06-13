#!/bin/bash -eu
cd /home/ec2-user/downloads
wget https://chromedriver.storage.googleapis.com/2.38/chromedriver_linux64.zip
echo '[CentOS-base]
name=CentOS-6 - Base
mirrorlist=http://mirrorlist.centos.org/?release=6&arch=x86_64&repo=os
gpgcheck=1
gpgkey=http://mirror.centos.org/centos/RPM-GPG-KEY-CentOS-6

#released updates
[CentOS-updates]
name=CentOS-6 - Updates
mirrorlist=http://mirrorlist.centos.org/?release=6&arch=x86_64&repo=updates
gpgcheck=1
gpgkey=http://mirror.centos.org/centos/RPM-GPG-KEY-CentOS-6

#additional packages that may be useful
[CentOS-extras]
name=CentOS-6 - Extras
mirrorlist=http://mirrorlist.centos.org/?release=6&arch=x86_64&repo=extras
gpgcheck=1
gpgkey=http://mirror.centos.org/centos/RPM-GPG-KEY-CentOS-6' > /etc/yum.repos.d/centos.repo
rpm --import http://mirror.centos.org/centos/RPM-GPG-KEY-CentOS-6
yum -y install GConf2


pip install selenium
