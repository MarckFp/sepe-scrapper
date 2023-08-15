import time
import subprocess
import os
import requests

# You should change this data, if you are unsure visit https://sede.sepe.gob.es/portalSede/procedimientos-y-servicios/personas/proteccion-por-desempleo/cita-previa/cita-previa-solicitud.html
# and catch your own request data from the network tool at the Browser Developer Tools
ID_CLIENTE = 0
CODIGO_ENTIDAD = ''
ID_GRUPO_SERVICIO = 0
CODIGO_POSTAL = '00000'
LAT_ORIGEN = '00.000000'
LNG_ORIGEN = '-0.000000'
TRAMITE_RELACIONADO = 0
IDS_JERARQUIA_TRAMITES = 0
URL = f'https://citaprevia-sede.sepe.gob.es/citapreviasepe/cita/cargaTiposAtencionMapa?idCliente={ID_CLIENTE}&codigoEntidad={CODIGO_ENTIDAD}&idGrupoServicio={ID_GRUPO_SERVICIO}&codigoPostal={CODIGO_POSTAL}&latOrigen={LAT_ORIGEN}&lngOrigen={LNG_ORIGEN}&tieneTramiteRelacionado={TRAMITE_RELACIONADO}&idsJerarquiaTramites={IDS_JERARQUIA_TRAMITES}'

POPUP_MESSAGE = "¡Cita disponible!"
NO_APPOINTMENTS_MESSAGE = "No hay citas"
ERROR_MESSAGE = "Ha ocurrido un error"
FREQUENCY = 300.0 #5 Minutes

start_time = time.monotonic()

while True:
    res = requests.get(URL, timeout=30)
    if res.status_code == 200:
        local_time = time.localtime()
        current_time = time.strftime("%H:%M:%S", local_time)
        if res.json()['listaOficina'][0]['primerHuecoDisponible'] != '':
            if os.name == 'posix':
                subprocess.Popen(['notify-send', POPUP_MESSAGE])
            elif os.name == 'nt':
                print(POPUP_MESSAGE) #Making pop-us on windows is hard man
            print(res.json()['listaOficina'][0]['primerHuecoDisponible'])
        else:
            print(current_time + " - " + NO_APPOINTMENTS_MESSAGE)
    else:
        print(ERROR_MESSAGE)
    time.sleep(FREQUENCY - ((time.monotonic() - start_time) % FREQUENCY))
