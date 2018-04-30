import flask
import Telegram_handler
import Github_handler
import json

mainapp = flask.Flask(__name__)
contactos = []

@mainapp.route('/legramschTelegramHandler',methods=['POST'])
def handletelegram():
    data = json.loads(flask.request.data)
    sender = data['message']['from']['id']
    message = data['message']['text']
    respuesta, ordenes = Telegram_handler.handlemessage(message)
    if ordenes:
        if ordenes == 'NEW':
            if sender not in contactos:
                contactos.append(sender)
                print('nuevo contacto!')
        else:
            respuesta = Github_handler.request_handler(ordenes)
    Telegram_handler.SendMessage(respuesta, sender)
    return 'Done'


@mainapp.route('/legramschGithubHandler', methods=['POST'])
def handlegithub():
    data = json.loads(flask.request.data)
    numero = data['issue']['number']
    if data['action'] == 'opened':
        print('oh may ga, se creo una Issue!')
        numero = data['issue']['number']
        error = Github_handler.check_errors(numero)
        if error:
            Github_handler.request_handler({'orden':'POST', 'numero':numero, 'mensaje':error})
        msj = Github_handler.request_handler({'orden':'GET', 'numero':numero})
        for x in contactos:
            Telegram_handler.SendMessage('nueva Issue!!!', x)
            Telegram_handler.SendMessage(msj, x)
    elif data['action'] == 'closed':
        if Github_handler.check_closed(numero):
            Github_handler.request_handler({'orden':'LABEL', 'numero':numero, 'label':'Googleable'})

    return 'Nice'

@mainapp.route('/apunteswaw',methods=['GET'])
def apunteswaw():
    return 'Done'

mainapp.run(port=8080)
