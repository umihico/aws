#!/bin/bash -eu
cp /home/ec2-user/github/aws/setup_scripts/zip.zip /root/.ssh/
cd /root/.ssh/
unzip zip.zip
chmod 400 ./id_rsa
chmod 400 ./id_rsa.pub
eval `ssh-agent`
ssh-add ./id_rsa
git config --global --unset user.email
git config --global --unset user.name
git config --global --add user.email umihico_dummy@users.noreply.github.com
git config --global --add user.name umihico
ssh -T git@github.com
ssh -T git@bitbucket.org
cd /home/ec2-user/github/aws
git remote set-url origin git@github.com:umihico/aws.git
cd /home/ec2-user/github
git clone git@github.com:umihico/ipo_autoapplier.git
git clone git@github.com:umihico/passpacker.git
git clone git@github.com:umihico/umihico_commons.git
git clone git@github.com:umihico/stenizer.git
git clone git@github.com:umihico/xpath_detecter.git
git clone git@github.com:umihico/blog.git
git clone git@bitbucket.org:umihico/trading.git
