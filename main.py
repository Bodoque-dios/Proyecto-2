import json


from oauth2client.service_account import ServiceAccountCredentials
import gspread
from flask import Flask, render_template, request, redirect, session, flash, jsonify

from validate_email import validate_email

from newsapi import NewsApiClient

from sort import get_ranking

#Noticias
newsapi = NewsApiClient(api_key='ffa1123e4add4b7c9e5e95f1ce806f8b')
headlines = newsapi.get_everything(language='es',  sort_by="publishedAt", page_size=30, q='(biodegradable AND reutilizar) OR (reutilizar AND reciclaje)')

#Flask
app = Flask(__name__)
app.secret_key = 'no revelar clave'

#Drive
credential = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", ["https://spreadsheets.google.com/feeds",
                                                                                    "https://www.googleapis.com/auth/spreadsheets",
                                                                                    "https://www.googleapis.com/auth/drive.file",
                                                                                    "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credential)
Proyecto_2_db = client.open('Proyecto-2-db')

# objetos de drive 
users_gs = Proyecto_2_db.get_worksheet(0)
ranking_gs = Proyecto_2_db.get_worksheet(1)
posiciones_gs = Proyecto_2_db.get_worksheet(4)


@app.route('/')
def hello_world():

    noticias = headlines['articles']

    ranking_ = get_ranking()[:10:]

    return render_template('inicio.html', noticias=noticias, ranking= ranking_)

@app.route('/revisar', methods=['POST'])
def check():
    users = users_gs.get_all_records()
    for user in users:
        if user['usuario'] == request.form['usuario'] and str(user['contrasena']) == str(request.form['contraseña']):
            session['id'] = user['id']
            session['usuario'] = user['usuario']
            session['nombre'] = user['nombre']
            session['mail'] = user['mail']
            session['fdn'] = user['fdn']
            session['region/comuna'] = user['region/comuna']
            session['img'] = user['img']
            session['active'] = True

            noticias = headlines['articles']
            
            return redirect('/')#cambiar a pagina de inicio

    flash('Usuario o Clave erronea')
    return redirect("/signin.html") #esto pendiente

@app.route('/ranking')
def ranking():
    
    registros = []
    registros = get_ranking()

    return render_template('/ranking.html', registros = registros)


@app.route('/signin.html')
def signin():
    return render_template('/signin.html')


@app.route('/signup.html')
def signup():
    return render_template('/signup.html')


@app.route('/salir')
def logout():
    session.clear()
    return redirect('/')

@app.route("/perfil")#Aqui lo deje asi no mas, me falta cambiarlo a mi al otro link de perfil(pipe)
def perfil():
    posiciones = []
    posiciones = get_ranking()
    return render_template('/perfil_.html',  posiciones = posiciones)


@app.route('/tips_y_consejos')
def consejos():
    return render_template('/tips_y_consejos.html')

@app.route('/tips/<titulo>')
def tip(titulo):

    return render_template('/tip.html', titulo=titulo)

@app.route('/progreso')
def progresos():
    return render_template('/progreso.html')


@app.route('/puntos')
def puntos():
    return render_template('/puntos.html')

@app.route('/metas')
def metas():
    return render_template('/mismetaseste.html')

@app.route('/nosotros')
def nosotros():
    return render_template('/nosotros.html')


if __name__ == "__main__":
    app.run(debug=True)