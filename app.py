from flask import Flask, request, render_template, make_response
import flask.views
import random
import xml.etree.ElementTree as ET
import sys
import json
import uuid

app = Flask(__name__)

tree = ET.parse('chemia.xml')
root = tree.getroot()
app = flask.Flask(__name__)
moja = []
ID = []
otazka = []
dic = {'od': 0, 'ot': 0, 'body': 0, 'sklonovanie':'ok', 'userID': None, 'listotazok':0, 'ypsilon': None}
uvod = 'Zvol spravne odpovede. Skontroluj svoje odpovede kliknutim na tlacitko kontrola.'

@app.route('/', methods=['GET'])
def get():
    dic['userID'] = ''
    if request.cookies.get('nameID') == None:
        randommeno = str(uuid.uuid4())
        dic['userID'] = randommeno
        dic['listotazok'] = list(range(1, 5 + 1))
        pole = (dic['userID'], dic['listotazok'])
        print('toto vypise pole v newUSER', pole)
        respond = make_response(
            render_template('layout.html', uvod=True, bdy=dic['body'], sklonovanie=dic['sklonovanie']).encode('utf-8'))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

    else:
        kokie = request.cookies.get('nameID')
        pole1 = json.loads(kokie)
        pole2 = pole1[:1]
        pole3 = str(pole2)
        pole4 = pole3[2:-2]
        print('cookie pola', pole4)
        dic['userID'] = pole4
        lstpole2 = pole1[1:3]
        lstpole3 = list(lstpole2)
        lstpole4 = random.choice(lstpole3)
        print('listicek', lstpole4)
        dic['listotazok'] = lstpole4
        pole = (dic['userID'], dic['listotazok'])
        print('toto vypise pole', pole)
        respond = make_response(
            render_template('layout.html', uvod=True, bdy=dic['body'], sklonovanie=dic['sklonovanie']).encode('utf-8'))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond




@app.route('/', methods=['POST'])
def post():
    if request.form['btn'] == 'Nova otazka':
        print('kookie', request.cookies.get('nameID', dic['listotazok']))
        print('list', dic['listotazok'])
        if len(list(dic['listotazok'])) == 0:
            return flask.render_template('layout.html', control='Nemame otazky', bdy=dic['body'],
                                         sklonovanie=dic['sklonovanie'])
        else:
            y = random.choice(dic['listotazok'])
            for otazky in root.findall('otazka'):
                number = otazky.attrib.get('number')
                if str(y) == number:
                    dic['ypsilon'] = int(y)
                    ot = otazky.find('ot').text
                    od = otazky.find('od').text
                    dic['od'] = od
                    dic['ot'] = ot
                    kookie = request.cookies.get('nameID')
                    print('meno', kookie)
                    print(dic['od'])
                    return flask.render_template('layout.html', otazka=dic['ot'],
                                                 control=('Spravna odpoved je', dic['od']), bdy=dic['body'],
                                                 sklonovanie=dic['sklonovanie'])

    if request.form['btn'] == 'Kontrola':
        def kont():
            print(request.cookies.get('nameID'))
            A = request.form.get('A')
            if A:
                moja.append('a')
            B = request.form.get('B')
            if B:
                moja.append('b')
            C = request.form.get('C')
            if C:
                moja.append('c')
            D = request.form.get('D')
            if D:
                moja.append('d')
            E = request.form.get('E')
            if E:
                moja.append('e')
            F = request.form.get('F')
            if F:
                moja.append('f')
            G = request.form.get('G')
            if G:
                moja.append('g')
            H = request.form.get('H')
            if H:
                moja.append('h')

        kont()
        a = dic['od']
        lst = str(a).split(',')
        print('moja', moja, 'od', lst)

        if list(moja) == lst:
            moja[:] = []
            kokie = request.cookies.get('nameID')
            try:
                dic['listotazok'].remove(dic['ypsilon'])
            except ValueError:
                pass
            pole = (dic['userID'], dic['listotazok'])
            print('toto vypise pole', pole)
            dic['body'] = 5 - len(dic['listotazok'])
            if dic['body'] == 1:
                dic['sklonovanie'] = 'ku'
            elif dic['body'] == 2 or dic['body'] == 3 or dic['body'] == 4:
                dic['sklonovanie'] = 'ky'
            elif dic['body'] >= 5:
                dic['sklonovanie'] = 'ok'
            respond = make_response(
                flask.render_template('layout.html', control='Vyborne, spravna odpoved!', bdy=dic['body'],
                                      sklonovanie=dic['sklonovanie']))
            respond.set_cookie('nameID', json.dumps(pole))
            return respond

        elif list(moja) != lst:
            moja[:] = []
            return flask.render_template('layout.html', control='Bohužiaľ nesprávne.', otazka=dic['ot'], odp=dic['od'],
                                         bdy=dic['body'], sklonovanie=dic['sklonovanie'])

    if request.form['btn'] == 'Resetuje otazky':
        kokie = request.cookies.get('nameID')
        dic['listotazok'] = list(range(1, 5 + 1))
        pole = (dic['userID'], dic['listotazok'])
        print('toto vypise pole', pole)
        dic['sklonovanie'] = 'ok'
        dic['body'] = 0
        respond = make_response(
            flask.render_template('layout.html', control='List otazok sa zresetoval.', bdy=dic['body'],
                                  sklonovanie=dic['sklonovanie']))
        respond.set_cookie('nameID', json.dumps(pole))
        return respond

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

