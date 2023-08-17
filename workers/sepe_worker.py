from os import environ
from requests import get, post
from json import load

#TELEGRAM
TELEGRAM_TOKEN = environ('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = environ('TELEGRAM_CHAT_ID')
TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

#SEPE
ID_CLIENTE = environ('ID_CLIENTE')
CODIGO_ENTIDAD = ""
LAT_ORIGEN = environ('LAT_ORIGEN')
LNG_ORIGEN = environ('LNG_ORIGEN')
IDS_JERARQUIA_TRAMITES = environ('IDS_JERARQUIA_TRAMITES')

#RESPONSES
POPUP_MESSAGE = "¡Cita disponible!"
NO_APPOINTMENTS_MESSAGE = "No hay citas"
ERROR_MESSAGE = "Ha ocurrido un error"

def handler(event, _context):
    for message in event["Records"]:
        message = load(message["body"])
        USER = message["user"]
        APPOINTMENT = message["appointment"]

        SEPE_URL = f'https://citaprevia-sede.sepe.gob.es/citapreviasepe/cita/cargaTiposAtencionMapa?idCliente={ID_CLIENTE}&codigoEntidad={CODIGO_ENTIDAD}&idGrupoServicio={APPOINTMENT["idGrupoServicio"]}&codigoPostal={USER["zipcode"]}&latOrigen={LAT_ORIGEN}&lngOrigen={LNG_ORIGEN}&tieneTramiteRelacionado={APPOINTMENT["tieneTramiteRelacionado"]}&idsJerarquiaTramites={IDS_JERARQUIA_TRAMITES}'

        response = get(SEPE_URL, timeout=20)
        if response.status_code == 200:
            if response.json()['listaOficina'][0]['primerHuecoDisponible'] != '':
                if USER["preference"] == "telegram":
                    data = {"text": POPUP_MESSAGE.encode("utf8"), "chat_id": USER["chat_id"]}
                    post(TELEGRAM_URL, data, timeout=10)
                if USER["preference"] == "email":
                    print("Send Email")
                print(response.json()['listaOficina'][0]['primerHuecoDisponible'])
            else:
                print(NO_APPOINTMENTS_MESSAGE)
        else:
            print(ERROR_MESSAGE)
