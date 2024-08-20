# Knappespillet Service 
System service for autostarting menu loop and run other scripts whenever it chrashes or restarts


# Helpfull commands

```sh
sudo systemctl status game.service # Check status
sudo systemctl restart game.service # Restarts autorun script. Also runs ExecStop.py

sudo systemctl disable game.service # Disables the service. It will not start by itself
```

## First time setup on Rpi 
Install dependencies through venv as seen in `knappespill/README.md`


## Initiate game-service
!Must be done if changes to `game.service` has been done!


```sh
cd service
sudo cp game.service /lib/systemd/system/game.service
sudo systemctl enable game.service  
```

it is also possible to setup symlink to the game.service file.

```sh
cd service
sudo systemctl link ./game.service 
sudo systemctl enable game.service  
```
