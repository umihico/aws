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
