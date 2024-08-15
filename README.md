# Knappespillet

Games for the Kantega wall project.

# Local development setup

## Prerequesist
- python3 
- python3 virtualenv

## Installing dependencies

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.emulate.txt
```

## Emulate

```sh
python3 src/emulate.py
```

# Development/Setup on RPi

## Connecting to RPi with SSH

```sh
ssh makerspace@knappespillet.local  
```
Password: raspberry


## Initial setup of Raspberry Pi

```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```sh
sudo venv/bin/python src/run.py
```




### TODO

- Command line arguments
- Sound effects
