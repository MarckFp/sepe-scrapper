import time
import os
import requests

#TELEGRAM
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

#SEPE
ID_CLIENTE = os.getenv('ID_CLIENTE')
COD_ENTIDAD = os.getenv('COD_ENTIDAD')
COD_IDIOMA = os.getenv('COD_IDIOMA')
ID_GRUPO_SERVICIO = os.getenv('ID_GRUPO_SERVICIO')
ZIPCODE = os.getenv('ZIPCODE')
LAT_ORIGEN = os.getenv('LAT_ORIGEN')
LNG_ORIGEN = os.getenv('LNG_ORIGEN')
TRAMITE_RELACIONADO = os.getenv('TRAMITE_RELACIONADO')
IDS_JERARQUIA_TRAMITES = os.getenv('IDS_JERARQUIA_TRAMITES')
SEPE_URL = f'https://citaprevia-sede.sepe.gob.es/citapreviasepe/cita/cargaTiposAtencionMapa?idCliente={ID_CLIENTE}&idGrupoServicio={ID_GRUPO_SERVICIO}&codigoPostal={ZIPCODE}&latOrigen={LAT_ORIGEN}&lngOrigen={LNG_ORIGEN}&tieneTramiteRelacionado={TRAMITE_RELACIONADO}&idsJerarquiaTramites={IDS_JERARQUIA_TRAMITES}&codIdioma={COD_IDIOMA}&codigoEntidad={COD_ENTIDAD}'
def handler(_event, _context):
    POPUP_MESSAGE = "¡Cita disponible!"
    NO_APPOINTMENTS_MESSAGE = "No hay citas"
    ERROR_MESSAGE = "Ha ocurrido un error"

    res = requests.post(SEPE_URL, timeout=20)
    if res.status_code == 200:
        local_time = time.localtime()
        current_time = time.strftime("%H:%M:%S", local_time)
        if res.json()['listaOficina'][0]['primerHuecoDisponible'] != '':
            data = {"text": POPUP_MESSAGE.encode("utf8"), "chat_id": TELEGRAM_CHAT_ID}
            requests.post(TELEGRAM_URL, data, timeout=10)
            print(res.json()['listaOficina'][0]['primerHuecoDisponible'])
        else:
            print(current_time + " - " + NO_APPOINTMENTS_MESSAGE)
    else:
        print(ERROR_MESSAGE)
