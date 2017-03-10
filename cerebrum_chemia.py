# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, make_response
import flask.views
import random
import xml.etree.ElementTree as ET
import sys
import json
import uuid

tree = ET.parse('chemia.xml')
root = tree.getroot()
app = flask.Flask(__name__)
moja = []
ID = []
otazka = []
dic = {'od': 0, 'ot': 0, 'body': 0, 'sklonovanie':'ok', 'userID': 'xyz', 'listotazok':0, 'ypsilon': None}
uvod = 'Zvol spravne odpovede. Skontroluj svoje odpovede kliknutim na tlacitko kontrola.'

class View(flask.views.MethodView):
    def get(self):
        dic['userID'] = ''
        if request.cookies.get('nameID') == None:
            randommeno = str(uuid.uuid4())
            dic['listotazok'] = list(range(1, 5 + 1))
            dic['userID'] = uuid.uuid4()
            print('vypise list2',dic['listotazok'])
            pole = (dic['userID'], dic['listotazok'])
            print('toto vypise pole v newUSER',pole)
            respond = make_response(render_template('layout.html', uvod = True, bdy = dic['body'], sklonovanie = dic['sklonovanie']).encode('utf-8'))
            respond.set_cookie('nameID', json.dumps(pole))
            return respond
        
        else:
            kokie = request.cookies.get('nameID')
            pole1 = json.loads(kokie)
            pole2 = pole1[:1]
            pole3 = str(pole2)
            pole4 = pole3[2:38]
            print('cookie pola', pole4)
            dic['userID'] = pole4
            lstpole2 = pole1[1:3]
            lstpole3 = list(lstpole2)
            lstpole4 = random.choice(lstpole3)
            print('listicek',lstpole4)
            dic['listotazok'] = lstpole4
            pole = (dic['userID'], dic['listotazok'])
            print('toto vypise pole', pole)
            respond = make_response(render_template('layout.html', uvod = True, bdy = dic['body'], sklonovanie = dic['sklonovanie']).encode('utf-8'))
            respond.set_cookie('nameID', json.dumps(pole))
            return respond

    def post(self):
        if request.form['btn'] == 'Nova otazka':
            print('kookie',request.cookies.get('nameID', dic['listotazok']))
            print('list', dic['listotazok'])
            if len(dic['listotazok']) == 0:
                return flask.render_template('layout.html', control='Nemame otazky', bdy = dic['body'], sklonovanie = dic['sklonovanie'])
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
                        return flask.render_template('layout.html', otazka = dic['ot'], control = ('Spravna odpoved je',dic['od']), bdy = dic['body'], sklonovanie = dic['sklonovanie'])

        if request.form['btn'] == 'Kontrola':
            def kont():
                print(request.cookies.get('nameID'))
                A=request.form.get('A')
                if A:
                    moja.append('a')
                B=request.form.get('B')
                if B:
                    moja.append('b')
                C=request.form.get('C')
                if C:
                    moja.append('c')
                D=request.form.get('D')
                if D:
                    moja.append('d')
                E=request.form.get('E')
                if E:
                    moja.append('e')
                F=request.form.get('F')
                if F:
                    moja.append('f')
                G=request.form.get('G')
                if G:
                    moja.append('g')
                H=request.form.get('H')
                if H:
                    moja.append('h')

            kont()
            a = 0
            a = dic['od']
            a = a.replace(',','')
            lst = list(a)
            print('moja', moja, 'od', lst)
            
            if list(moja) == lst:
                
                dic['body'] += 1
                if dic['body'] == 1:
                    dic['sklonovanie']='ku'
                if dic['body'] == 2 or dic['body'] == 3 or dic['body'] == 4:
                    dic['sklonovanie']='ky'
                if dic['body'] >= 5:
                    dic['sklonovanie']='ok'
                moja[:]=[]
                kokie = request.cookies.get('nameID') 
                dic['listotazok'].remove(dic['ypsilon'])
                pole = (dic['userID'], dic['listotazok'])
                print('toto vypise pole', pole)
                respond = make_response(flask.render_template('layout.html', control = 'Vyborne, spravna odpoved!', bdy = dic['body'], sklonovanie = dic['sklonovanie']))
                respond.set_cookie('nameID', json.dumps(pole))
                return respond

            elif list(moja) != lst:
                moja[:]=[]
                return flask.render_template('layout.html', control = 'Bohužiaľ nesprávne.', otazka = dic['ot'], odp = dic['od'], bdy = dic['body'], sklonovanie = dic['sklonovanie'])

        if request.form['btn'] == 'Resetuje otazky':
            kokie = request.cookies.get('nameID')
            dic['listotazok'] = list(range(1, 5 + 1))
            pole = (dic['userID'], dic['listotazok'])
            print('toto vypise pole', pole)
            respond = make_response(flask.render_template('layout.html', control = 'List otazok sa zresetoval.', bdy = dic['body']))
            respond.set_cookie('nameID', json.dumps(pole))
            return respond
            
                                
app.add_url_rule('/', view_func=View.as_view('main'), methods=['GET', 'POST'])
app.debug = True
app.run()
