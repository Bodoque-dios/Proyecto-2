from flask import Flask, render_template, request, redirect, session, flash, jsonify
app = Flask(__name__)

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from tabulate import tabulate

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
    return render_template('algunawea.html')

@app.route('/revisar', methods=['POST'])
def check():
    users = users_gs.get_all_records()
    for user in users:
        if user['usuario'] == request.form['usuario'] and user['contrasena'] == request.form['contraseña']:
            #session['id'] = user['id']
            #session['nombre'] = user['nombre']
            #session['active'] = True
            return jsonify(ranking_gs.get_all_records())
    return jsonify(users_gs.get_all_records())

@app.route('/ranking')
def ranking():

    return jsonify(ranking_gs.get_all_records())

@app.route('/signin.html')
def signin():
    return render_template('/signin.html')

@app.route('/signup.html')
def signup():
    return render_template('/signup.html')

#Aqui agrego la Ruta del perfil
@app.route("perfil.html")#Aqui lo deje asi no mas, me falta cambiarlo a mi al otro link de perfil(pipe)
def perfil():
    return render_template('/perfil.html')
    
if __name__ == "__main__":
    app.run(debug=True)
