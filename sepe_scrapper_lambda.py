import time
import os
import requests

#TELEGRAM
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

#SEPE
ID_CLIENTE = os.getenv('ID_CLIENTE')
CODIGO_ENTIDAD = ""
ID_GRUPO_SERVICIO = os.getenv('ID_GRUPO_SERVICIO')
ZIPCODE = os.getenv('ZIPCODE')
LAT_ORIGEN = os.getenv('LAT_ORIGEN')
LNG_ORIGEN = os.getenv('LNG_ORIGEN')
TRAMITE_RELACIONADO = os.getenv('TRAMITE_RELACIONADO')
IDS_JERARQUIA_TRAMITES = os.getenv('IDS_JERARQUIA_TRAMITES')
SEPE_URL = f'https://citaprevia-sede.sepe.gob.es/citapreviasepe/cita/cargaTiposAtencionMapa?idCliente={ID_CLIENTE}&codigoEntidad={CODIGO_ENTIDAD}&idGrupoServicio={ID_GRUPO_SERVICIO}&codigoPostal={ZIPCODE}&latOrigen={LAT_ORIGEN}&lngOrigen={LNG_ORIGEN}&tieneTramiteRelacionado={TRAMITE_RELACIONADO}&idsJerarquiaTramites={IDS_JERARQUIA_TRAMITES}'

def handler(_event, _context):
    popup_message = "¡Cita disponible!"
    no_appointments_message = "No hay citas"
    error_message = "Ha ocurrido un error"

    res = requests.get(SEPE_URL, timeout=45)
    if res.status_code == 200:
        local_time = time.localtime()
        current_time = time.strftime("%H:%M:%S", local_time)
        if res.json()['listaOficina'][0]['primerHuecoDisponible'] != '':
            data = {"text": popup_message.encode("utf8"), "chat_id": TELEGRAM_CHAT_ID}
            requests.post(TELEGRAM_URL, data, timeout=15)
            print(res.json()['listaOficina'][0]['primerHuecoDisponible'])
        else:
            print(current_time + " - " + no_appointments_message)
    else:
        print(error_message)
