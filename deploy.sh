SSH_ENDPOINT=makerspace@knappespillet.local
PROJECT=knappespillet

ssh $SSH_ENDPOINT /bin/bash << EOF
cd ~/$PROJECT
git pull
sudo systemctl restart game.service