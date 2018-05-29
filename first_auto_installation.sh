#!/bin/bash -eu
read -p "input your gmail:" gmail
sudo su -
yum update
yum -y install gcc gcc-c++ make git openssl-devel bzip2-devel zlib-devel readline-devel sqlite-devel
git clone https://github.com/yyuu/pyenv.git /usr/bin/.pyenv
cd /usr/bin/.pyenv
mkdir shims
mkdir versions
chown -R ec2-user:ec2-user /usr/bin/.pyenv
echo 'export PYENV_ROOT="/usr/bin/.pyenv"
if [ -d "${PYENV_ROOT}" ]; then
export PATH=${PYENV_ROOT}/bin:$PATH
eval "$(pyenv init -)"
fi' >> ~/.bashrc
source ~/.bashrc
pyenv install --list
pyenv install 3.6.5
python -V
pyenv global 3.6.5
python -V
yum -y install tmux
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
cd /home/ec2-user/
mkdir downloads
cd downloads/
wget https://chromedriver.storage.googleapis.com/2.38/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
mkdir fonts
cd fonts/
wget https://noto-website-2.storage.googleapis.com/pkgs/Noto-hinted.zip
unzip Noto-hinted.zip
mkdir -p /usr/share/fonts/opentype/noto
cp *otf *ttf /usr/share/fonts/opentype/noto
fc-cache -f -v # optional
sudo su -
pip install selenium
pip install --upgrade pip
cd /home/ec2-user/
mkdir github
cd github/
git clone https://github.com/umihico/aws.git
cd /home/ec2-user/github/aws
git remote set-url origin git@github.com:umihico/aws.git
pip install r- req.txt
ssh-keygen -t rsa -C $gmail
eval `ssh-agent`
ssh-add /root/.ssh/id_rsa
cat /root/.ssh/id_rsa.pub
read -p "press enter after above key is added on github..."
ssh -T git@github.com
