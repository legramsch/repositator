import requests
import re



def handlemessage(message):
    if re.match('^(/start)', message):
        respuesta = 'Salut, je suis Le Gramsch bot, et je vais vous aider avec\
votre dépôt github. Dans ce cas, le dépôt est https://github.com/legramsch/repositator. \n \
para interactuar con el bot, usa los siguientes comandos:\n - /get #numero_issue --> ver un issue en especifico\n \
- /post #numero_issue *respuesta --> publicar respuesta en una issue \n- /label #numero_issue label --> asignar etiqueta a un issue \n\
- /close #numero_issue --> Cerrar una issue'
        return respuesta, 'NEW'
    elif re.match('^(/get) ', message):
        num = re.search(' #[1-9]+', message)
        if num:
            poses = num.span()
            respuesta = 'Hubo un problema tal ves?'
            numero = int(message[poses[0]+2:poses[1]])
            return respuesta, {'orden':'GET', 'numero':numero}
        else:
            respuesta = 'Numero ingresado es invalido, debe ser del formato "#[numero de Issue]"'
            return respuesta, None
    elif re.match('^(/post) ', message):
        num = re.search(' #[1-9]+ ', message)
        if num:
            poses = num.span()
            numero = int(message[poses[0]+2:poses[1]])
            mes = re.search(' (\*[\w\s.]+)', message)
            if mes:
                poses = mes.span()
                msj = message[poses[0]+2:poses[1]]
                respuesta = 'Hubo un problema tal vez?'
                return respuesta, {'orden':'POST', 'numero':numero, 'mensaje':msj}
            else:
                respuesta = 'Comentario invalido, debe ser del formato "*[Comentario]"'
                return respuesta, None
        else:
            respuesta = 'Numero ingresado es invalido, debe ser del formato "#[numero de Issue]"'
            return respuesta, None

    elif re.match('^(/label) ', message):
        num = re.search(' #[1-9]+ ', message)
        if num:
            poses = num.span()
            numero = int(message[poses[0]+2:poses[1]])
            mes = re.search(' [\w\s.]+', message)
            if mes:
                poses = mes.span()
                msj = message[poses[0]+1:poses[1]]
                respuesta = 'Hubo un problema tal vez?'
                return respuesta, {'orden':'LABEL', 'numero':numero, 'label':msj}
            else:
                respuesta = 'No escribiste ningun label!'
                return respuesta, None
        else:
            respuesta = 'Numero ingresado es invalido, debe ser del formato "#[numero de Issue]"'
            return respusta, None
    elif re.match('^(/close) ', message):
        num = re.search(' #[1-9]+', message)
        if num:
            poses = num.span()
            numero = int(message[poses[0]+2:poses[1]])
            respuesta = 'Hubo un problema tal ves?'
            return respuesta, {'orden':'CLOSE', 'numero':numero}
        else:
            respuesta = 'Numero ingresado es invalido, debe ser del formato "#[numero de Issue]"'
            return respuesta, None

    else:
        return 'No se que quiere caballero', None

def SendMessage(mensaje, sender):
    a = requests.post('https://api.telegram.org/bot438437858:AAE_vFeTXCUmXtU8Ax3PSczDBQGvBBrhLc8/sendMessage',params={'chat_id':sender, 'text': mensaje})
