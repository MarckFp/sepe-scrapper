import requests
import time
import subprocess
import os

# You should change this data, if you are unsure visit https://sede.sepe.gob.es/portalSede/procedimientos-y-servicios/personas/proteccion-por-desempleo/cita-previa/cita-previa-solicitud.html
# and catch your own request data from the network tool at the Browser Developer Tools
idCliente = 0
codigoEntidad = ''
idGrupoServicio = 0
codigoPostal = '00000'
latOrigen = '00.000000'
lngOrigen = '-0.000000'
tieneTramiteRelacionado = 0
idsJerarquiaTramites = 0
url = f'https://citaprevia-sede.sepe.gob.es/citapreviasepe/cita/cargaTiposAtencionMapa?idCliente={idCliente}&codigoEntidad={codigoEntidad}&idGrupoServicio={idGrupoServicio}&codigoPostal={codigoPostal}&latOrigen={latOrigen}&lngOrigen={lngOrigen}&tieneTramiteRelacionado={tieneTramiteRelacionado}&idsJerarquiaTramites={idsJerarquiaTramites}'

start_time = time.monotonic()
popup_message = "¡Cita disponible!"
no_appointments_message = "No hay citas"
frequency = 300.0 #5 Minutes

while True:
    res = requests.get(url)
    if res.status_code == 200:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        if res.json()['listaOficina'][0]['primerHuecoDisponible'] != '':
            if os.name == 'posix':
                subprocess.Popen(['notify-send', popup_message])
            elif os.name == 'nt':
                subprocess.Popen(['(Get-WmiObject Win32_OperatingSystem).Version', '|', 'Show-Notification', '-ToastTitle', popup_message])
            print(res.json()['listaOficina'][0]['primerHuecoDisponible'])
        else:
            print(current_time + " - " + no_appointments_message)
    else:
        print("Ha ocurrido un error")
    time.sleep(frequency - ((time.monotonic() - start_time) % frequency))
