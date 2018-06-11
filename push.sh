eval `ssh-agent`
ssh-add /c/Users/umi/.ssh/github
ssh -T git@github.com
git push
read -p "Hit enter: "
