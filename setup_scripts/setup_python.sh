
git clone https://github.com/yyuu/pyenv.git /usr/bin/.pyenv
cd /usr/bin/.pyenv
mkdir shims
mkdir versions
chown -R ec2-user:ec2-user /usr/bin/.pyenv
echo 'export PYENV_ROOT="/usr/bin/.pyenv"
if [ -d "${PYENV_ROOT}" ]; then
export PATH=${PYENV_ROOT}/bin:$PATH
eval "$(pyenv init -)"
fi' >> /root/.bashrc
source /root/.bashrc
pyenv install --list
pyenv install 3.6.5
python -V
pyenv global 3.6.5
python -V
cd /home/ec2-user/github/aws
pip install -r aws_requirements.txt
export PYTHONPATH="/home/ec2-user/github"
