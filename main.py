import json

from oauth2client.service_account import ServiceAccountCredentials
import gspread
from flask import Flask, render_template, request, redirect, session, flash, jsonify

from validate_email import validate_email


from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key='ffa1123e4add4b7c9e5e95f1ce806f8b')

headlines = newsapi.get_top_headlines(category='general',
                                        language='es'
)




app = Flask(__name__)
app.secret_key = 'no revelar clave'

credential = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", ["https://spreadsheets.google.com/feeds",
                                                                                    "https://www.googleapis.com/auth/spreadsheets",
                                                                                    "https://www.googleapis.com/auth/drive.file",
                                                                                    "https://www.googleapis.com/auth/drive"])


client = gspread.authorize(credential)
Proyecto_2_db = client.open('Proyecto-2-db')

users_gs = Proyecto_2_db.get_worksheet(0)
ranking_gs = Proyecto_2_db.get_worksheet(1)


@app.route('/')
def hello_world():
    noticias = headlines['articles']
    return render_template('inicio.html', noticias=noticias)

@app.route('/revisar', methods=['POST'])
def check():
    users = users_gs.get_all_records()
    for user in users:
        if user['usuario'] == request.form['usuario'] and str(user['contrasena']) == str(request.form['contraseña']):
            session['id'] = user['id']
            session['usuario'] = user['usuario']
            session['active'] = True

            noticias = headlines['articles']
            
            return render_template('inicio.html', noticias=noticias) #cambiar a pagina de inicio

    return jsonify(users_gs.get_all_records())


@app.route('/ranking')
def ranking():

    return render_template('/ranking.html')


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
    return render_template('/perfil_.html')

if __name__ == "__main__":
    app.run(debug=True)