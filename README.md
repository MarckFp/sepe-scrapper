# Sepe Scrapper
This tool is done to be able to find appointments in your location in a Spanish SEPE Office near you. I know this procedure can be done through internet but some people want to do it physically at the office.

# Requirements

- Python 3.11 or above

# Configuration

This script needs some basic data including the zipcode where you live, the procedure you want the appointment, etc To be able to fulfill this data you can visit the [SEPE website](https://sede.sepe.gob.es/portalSede/procedimientos-y-servicios/personas/proteccion-por-desempleo/cita-previa/cita-previa-solicitud.html) and try requesting an appointment with the desired procedure. In the network tool using the Browser Developer Tools you will find a request with the url `citaprevia-sede.sepe.gob.es/citapreviasepe/cita/cargaTiposAtencionMapa` the payload sent is the data you need to change in the script.

Also take in mind that if you modify the frequency it can generate issues. For example lowering the value can be detected as an DDOS attack and your IP will be blocked, for that reason choose a value that will not block you and it's frequent enough to detect appointments in time.

# Usage

Just run:
```
python3 sepe_scrapper.py
```
This will execute for every frequency you specified and with the data you have configured
