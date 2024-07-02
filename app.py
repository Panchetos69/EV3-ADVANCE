from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# Configuración de MariaDB
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'turismo'
app.config['MYSQL_PASSWORD'] = 'Panchetos1234'
app.config['MYSQL_DB'] = 'turismo'

mysql = MySQL(app)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        rut = request.form['rut']
        nombre_completo = request.form['nombre_completo']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo_electronico = request.form['correo_electronico']
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (rut, nombre_completo, direccion, telefono, correo_electronico) VALUES (%s, %s, %s, %s, %s)', (rut, nombre_completo, direccion, telefono, correo_electronico))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('register_confirmation', rut=rut, nombre_completo=nombre_completo, direccion=direccion, telefono=telefono, correo_electronico=correo_electronico))
    return render_template('register.html')

@app.route('/register_confirmation')
def register_confirmation():
    return render_template('register_confirmation.html', rut=request.args.get('rut'), nombre_completo=request.args.get('nombre_completo'), direccion=request.args.get('direccion'), telefono=request.args.get('telefono'), correo_electronico=request.args.get('correo_electronico'))

@app.route('/suggestions', methods=['GET', 'POST'])
def suggestions():
    if request.method == 'POST':
        correo_electronico = request.form['correo_electronico']
        mensaje = request.form['mensaje']
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO suggestions (correo_electronico, mensaje) VALUES (%s, %s)', (correo_electronico, mensaje))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('suggestion_confirmation', correo_electronico=correo_electronico, mensaje=mensaje))
    return render_template('suggestions.html')

@app.route('/suggestion_confirmation')
def suggestion_confirmation():
    return render_template('suggestion_confirmation.html', correo_electronico=request.args.get('correo_electronico'), mensaje=request.args.get('mensaje'))

@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

if __name__ == '__main__':
    app.run(debug=True)
