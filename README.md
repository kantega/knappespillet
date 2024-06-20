Knappespillet et MakerSpace/JavaZone prosjekt.

Kode til å drifte et fysisk knappe/arcade-spill som skal brukes på JavaZone og lignende arenaer. 

Koden skal kjøres direkte på en Raspberry Pi 4 Model B som styrer et rutenett med 5 X 7 knapper. 
Hver knapp skal ha en tilhørende adresserbar 12 RGB Ring fra Neopixel.

Koden kan utvikles lokalt på egen maskin eller tilkoblet til Raspberry Pien gjennom SSH tilkobling.

SSH til Raspberry Pi:

* Raspberry Pi må være tilkoblet strøm og du må være tilkoblet samme nettverk
* Visual Studio:
    1. Last ned plugin -> Remote-SSH
    2. Hurtigtast CMD + Shift + P -> Søk etter handlingen -> Connect to Host
    3. Host/Hostname: makerspace.local User: pi Password: raspberry
       
     
Kan gjøre kode lokalt og kopiere den over på pien gjennom scp -r pi@makerspac.local:/filepath

## Utvikling

### Nødvendige python pakker for å kjøre koden
- `pip install adafruit-circuitpython-neopixel`
- `pip install adafruit-circuitpython-busdevice`
- `pip install adafruit-circuitpython-mcp230xx`

### I2C Error?
Hvis koden klager på en feil med I2C så kan det være at I2C-bus på RaspberryPien har blitt disabled.
Slå det på igjen:
- `sudo raspi-config` -> Interfacing Options -> I2C -> Enable I2C