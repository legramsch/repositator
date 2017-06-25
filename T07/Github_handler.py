import requests
import json
from random import choice
import re
colors = ['6014ED', 'A84A4A', '51D126']
user = 'legramsch'
pswd = '2530027cb73d08d85a1f2ea1f74391f5366f9f2d'
ses = requests.Session()
ses.auth = (user, pswd)

def request_handler(orden):
    print(orden)
    if orden['orden'] == 'GET':
        numero = orden['numero']
        respuesta = requests.get('https://api.github.com/repos/legramsch/repositator/issues/{}'.format(str(numero)))
        if respuesta:
            data = json.loads(respuesta.text)
            print(data)
            url = data['url']
            m3n = data['comments']
            numero = data['number']
            autor = data['user']['login']
            titulo = data['title']
            texto = data['body']
            resp = '{}\n\nIssue #{} - {}\n\n{}\n\nComentarios: {}\n'.format(autor, numero, titulo, texto, m3n)
            comentarios = ses.get('https://api.github.com/repos/legramsch/repositator/issues/{}/comments'.format(numero))
            if comentarios:
                for x in json.loads(comentarios.text):
                    de = x['user']['login']
                    msj = x['body']
                    resp += '\n{}: {}'.format(de, msj)
            else:
                resp += 'Problema al cargar los comentarios'
            resp += '{}'.format(url)
            return resp
        else:
            return 'Hubo un problema al obtener el Issue (Seguro que puso el numero correcto?)'
    elif orden['orden'] == 'POST':
        numero = orden['numero']
        mensaje = orden['mensaje']
        comm = json.dumps({"body":mensaje})
        respuesta = ses.post('https://api.github.com/repos/legramsch/repositator/issues/{}/comments'.format(numero),comm)
        if respuesta:
            return 'Comentario hecho con exito!'
        else:
            return 'Hubo un problema al publicar el comentario ((Seguro que puso el numero correcto?))'
    elif orden['orden'] == 'LABEL':
        label = orden['label']
        numero = orden['numero']
        labels = ses.get('https://api.github.com/repos/legramsch/repositator/labels')
        if not labels:
            return 'Hubo un problema al obtener los labels ((Seguro que puso el numero correcto?))'
        else:
            lbs = json.loads(labels.text)
            if hay_label(lbs, label):
                color = choice(colors)
                labl = json.dumps([label])
                respuesta = ses.post('https://api.github.com/repos/legramsch/repositator/issues/{}/labels'.format(numero),labl)
                if respuesta:
                    return 'Issue etiquetado exitosamente!'
                else:
                    return 'Hubo un problema al etiquetar el Issue'
            else:
                DIC = json.dumps({"name":label, "color":choice(colors)})
                crear = ses.post('https://api.github.com/repos/legramsch/repositator/labels',DIC)
                if crear:
                    labl = json.dumps([label])
                    respuesta = ses.post('https://api.github.com/repos/legramsch/repositator/issues/{}/labels'.format(numero),labl)
                    if respuesta:
                        return 'Label creado, y Issue etiqueado con exito!'
                    else:
                        return 'Hubo un problema al agregar el Label'
                else:
                    return 'Problema al crear la etiquta'
    elif orden['orden'] == 'CLOSE':
        numero = orden['numero']
        orden = json.dumps({'state':'closed'})
        issue = ses.patch('https://api.github.com/repos/legramsch/repositator/issues/{}'.format(numero), orden)
        if issue:
            return 'Issue cerrado exitosamente!'
        else:
            return 'hubo un problema al cerrar la Issue'

def hay_label(labels, label):
    for x in labels:
        if x['name'] == label:
            return True
    return False

def check_errors(numero):
    data = requests.get('https://api.github.com/repos/legramsch/repositator/issues/{}'.format(str(numero)))
    if data:
        data = json.loads(data.text)
        issue = data['body']
        codigos = re.findall('`(.*?)`', issue, re.DOTALL)
        print(codigos)
        for x in codigos:
            lineas = x.split('\n')
            last = lineas.pop()
            if last == '':
                if lineas:
                    tru = lineas.pop()
                    busca = re.match('(.*?)(Error: )(.*?)', tru)
                    if busca:
                        busqueda = requests.get('https://www.googleapis.com/customsearch/v1?cx=008675764795148742003:pq6exbpjatg&key=AIzaSyBnByY_7A7p6E1nsLZKzq3DpWRl6--NRv0&q={}'.format(tru)).json()
                        if busqueda:
                            URL = busqueda['items'][0]['link']
                            respuesta = 'Hola amigo, LeGramschBot aqui, tal ves este link te pueda servir:\n{}'.format(URL)
                            return respuesta
                        else:
                            return 'Hola amigo, LeGramschBot aqui, Veo que tienes un error, pero no encontre nada :('
            else:
                busca = re.match('(.*?)Error: [\w\s.]+', last)
                if busca:
                    busqueda = requests.get('https://www.googleapis.com/customsearch/v1?cx=008675764795148742003:pq6exbpjatg&key=AIzaSyBnByY_7A7p6E1nsLZKzq3DpWRl6--NRv0&q={}'.format(last)).json()
                    if busqueda:
                        URL = busqueda['items'][0]['link']
                        respuesta = 'Hola amigo, LeGramschBot aqui, tal ves este link te pueda servir:\n{}'.format(URL)
                        return respuesta
                    else:
                        return 'Hola amigo, LeGramschBot aqui, Veo que tienes un error, pero no encontre nada :('
        return None

def check_closed(numero):
    comentarios = ses.get('https://api.github.com/repos/legramsch/repositator/issues/{}/comments'.format(numero))
    issue = requests.get('https://api.github.com/repos/legramsch/repositator/issues/{}'.format(str(numero)))
    if issue:
        autor = issue.json()['user']['login']
    if comentarios:
        data = comentarios.json()
        for x in data:
            if x['user']['login'] != 'legramsch' and x['user']['login'] != autor:
                return False
        return True
