cd /home/ec2-user/github/aws/setup_scripts
unzip zip.zip
eval `ssh-agent`
ssh-add ./id_rsa
git config --global --unset user.email
git config --global --unset user.name
git config --global --add user.email umihico_dummy@users.noreply.github.com
git config --global --add user.name umihico
echo "ssh -T git@github.com"
ssh -T git@github.com
ssh -T git@bitbucket.org
