# Knappespillet Service 
System service for autostarting menu loop


## First time setup on Rpi 
Install dependencies through venv as seen in `knappespill/README.md`


## Initiate game-service
!Must be done if changes to `game.service` has been done!

```sh
cd service
sudo cp game.service /lib/systemd/system/game.service
sudo systemctl enable game.service  
```
