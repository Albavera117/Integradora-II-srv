import string
from types import MethodDescriptorType
from MySQLdb import apilevel
from flask import Flask,Response, wrappers
from flask import request, redirect, url_for, flash,session
from flask import render_template,make_response
from flask import url_for,session
from flask.globals import current_app
from flask_mysqldb import MySQL
from fpdf import FPDF
from datetime import date
from datetime import datetime
from functools import wraps
#from flask_wtf import CsrfProtect, csrf
import random
import io
import xlwt
import Files


app = Flask(__name__)
mysql= MySQL(app)

#Conexion a MySQL
app.config['MYSQL_HOST'] = 'testdb-1.c9uecaufvfyj.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'#Userdentalcare'
app.config['MYSQL_PASSWORD'] = 'H1rb4Bu3n4_123?'#'utez_123?'
app.config['MYSQL_DB'] = 'dentalcare'

#csrf = CsrfProtect(app)
app.secret_key = 'd3nt4lcl1n1c'

#Decorador de autenticacion
def requires_access_level(puesto):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
                #Validar que el usuario se ha logeado
                if not session.get('email'):
                    flash("Debes iniciar sesion para acceder a este sitio")
                    return redirect(url_for('login'))

                #Query de puesto de usuario activo
                usr = session.get('email')
                cur = mysql.connection.cursor()
                cur.execute('SELECT Puesto FROM users WHERE Correo=%s', [usr])
                datos = cur.fetchall()
                id_puesto = datos[0][0]

                #Autorizacion de usuario
                if id_puesto != puesto:
                    return redirect(url_for('login'))
                return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.errorhandler(404)
def page_not_found(e):
    return render_template ('404.html'), 404

@app.route('/')
def indice ():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM subsidiary')
    datos = cur.fetchall()
    cur.execute('SELECT * FROM services')
    datos2 = cur.fetchall()

    return render_template ('index.html',opcion=datos,opcion2=datos2)

@app.route('/agendar/cita',methods = ['POST'])
def agendarcita():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        fecha = request.form['fecha']
        hr = request.form['hours']
        sucursal = request.form['sucursal']
        servicio = request.form['servicio']
        cur = mysql.connection.cursor()
        cur.callproc('registrar_cita',[nombre,apellido,telefono,fecha,hr,sucursal,servicio])
        cur.close()
        mysql.connection.commit()
        return redirect(url_for('indice'))

@app.route('/cancelar_cita' ,methods = ['POST'])
def cancelar_cita():
    folio = request.form['folio']
    num_tel = request.form['num_tel']
    
    cur = mysql.connection.cursor()
    cur.execute('UPDATE dentalcare.citas SET estatus_cita="Cancelada" WHERE folio=%s AND telefono=%s', [folio,num_tel])
    cur.close()
    mysql.connection.commit()
    flash("Cita {} cancelada".format(folio))

    return redirect(url_for('indice'))

@app.route('/login', methods = ['GET','POST'])
def login ():
    if request.method == 'POST':

        #Obtener datos del formulario
        email = str(request.form['email'])
        password = str(request.form['password'])
        cur = mysql.connection.cursor()
        cur.execute('SET @contrasena=%s',[password])
        cur.callproc('generar_hash',[password])
        password = cur.fetchall()
        password=password[0][0]


        #Obtener datos de la base de datos
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE Correo=%s AND Contraseña=%s', [email,password])
        data = cur.fetchall()

        #Validacion de usuario       
        if bool(data):
            emailBD = str(data[0][0])
            passwordBD = str(data[0][1])
            sucursalDB=str(data[0][4])
            if emailBD == email and passwordBD == password:
                #Creacion de sesion
                session['email'] = email
                session['sucursal'] = sucursalDB
                flash("Bienvenido {}".format(str(data[0][2])))
                if data[0][3] == "Doctor":
                    session['nombre'] = data[0][2]
                    return redirect(url_for('dashboard_doctor'))
                elif data[0][3] == "Manager":
                    return redirect(url_for('dashboard_manager'))
                else:
                    return redirect(url_for('dashboard_assistant'))

        #Datos incorrectos
        flash ("Usuario o contraseña inválido")
        return redirect(url_for('login'))

    return render_template ('login.html')

@app.route('/logout')
def logout():

    #session.pop('email',None)
    session.clear()
    #falta definir bien la salida de sesión
    return redirect(url_for('login'))

@app.route('/appointments_assistant')
@requires_access_level('Asistente')
def appointments_assistant ():
    #Query de datos para llenar tabla de registros
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM appointments WHERE Sucursal=%s ORDER BY Folio',[session['sucursal']])
    datos = cur.fetchall()

    return render_template ('appointments_assistant.html', datos = datos)

@app.route('/register_appointment', methods = ['GET', 'POST'])
@requires_access_level('Asistente')
def register_appointment ():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM services')
    datos = cur.fetchall()

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        fecha = request.form['fecha']
        hr = request.form['hours']
        sucursal = session['sucursal']
        servicio = request.form['servicio']
        cur = mysql.connection.cursor()
        cur.callproc('registrar_cita',[nombre,apellido,telefono,fecha,hr,sucursal,servicio])
        cur.close()
        mysql.connection.commit()
        return redirect(url_for('register_appointment'))

    return render_template('register_appointment.html', opcion=datos)


@app.route('/employees')
@requires_access_level('Manager')
def employees ():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM employees WHERE Sucursal = %s ORDER BY Sucursal',[session['sucursal']])
    session['x'] = None
    datos = cur.fetchall()


    return render_template ('employees.html', datos = datos)
    #id de empleado dato[6]





@app.route('/register_employees', methods = ['GET', 'POST'])
@requires_access_level('Manager')
def register_employees():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM job')
    datos = cur.fetchall()
    cur.execute('SELECT * FROM subsidiary')
    datos2 = cur.fetchall()
    cur.execute('SELECT `Numero`,`Nombre Sucursal` FROM doctors_office WHERE `Nombre Sucursal` = %s GROUP BY `Nombre Sucursal`,`Numero` ORDER BY `Numero`',[session['sucursal']])
    datos3 = cur.fetchall()

    if request.method == 'POST':

        nombre = request.form['name']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['phone']
        puesto = request.form['position']
        contraseña = request.form['password']
        sucursal = session['sucursal']
        consultorio=str()
        try:
            consultorio= request.form['consultorio']
        except:
            consultorio = 0
        print(consultorio)
        cur = mysql.connection.cursor()
        cur.callproc('registrar_empleado',[puesto,sucursal,nombre,apellido,email,telefono,contraseña,consultorio])
        cur.close()
        mysql.connection.commit()
        return redirect(url_for('register_employees'))

    return render_template ('register_employees.html',opcion=datos,opcion2=datos2,opcion3=datos3)
    

@app.route('/appointments_manager')
@requires_access_level('Manager')
def appointments_manager ():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM appointments WHERE Sucursal= %s ORDER BY Folio',[session['sucursal']])
    session['x'] = None
    datos = cur.fetchall()

    return render_template ('appointments_manager.html', datos = datos)

@app.route('/appointments_doctor')
@requires_access_level('Doctor')
def appointments_doctor ():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM appointments WHERE Sucursal = %s AND Doctor = %s ORDER BY Folio',[session['sucursal'],session['nombre']])
    datos = cur.fetchall()
    

    return render_template ('appointments_doctor.html', datos = datos)

@app.route('/dashboard_doctor')
@requires_access_level('Doctor')
def dashboard_doctor ():
    return render_template ('dashboard_doctor.html')

@app.route('/dashboard_manager')
@requires_access_level('Manager')
def dashboard_manager ():
    return render_template ('dashboard_manager.html')

@app.route('/dashboard_assistant')
@requires_access_level('Asistente')
def dashboard_assistant ():
    return render_template ('dashboard_assistant.html')

@app.route('/search',methods =['POST', 'GET'])
def search():
    if request.method == 'POST':
        busqueda= request.form.get("buscar",False).capitalize()
        filtro = request.form.get("filtro", False)
        session['x'] = busqueda
        session['y'] = filtro
        cur = mysql.connection.cursor()
        if filtro == 'puesto':
            cur.execute('SELECT * FROM employees WHERE Cargo=%s AND Sucursal=%s',[busqueda, session['sucursal']])
            datos = cur.fetchall()
        elif filtro == 'estatus':
            cur.execute('SELECT * FROM employees WHERE Estatus=%s AND Sucursal=%s', [busqueda, session['sucursal']])
            datos = cur.fetchall()
        else:
            cur.execute('SELECT * FROM employees WHERE Sucursal=%s', [session['sucursal']])
            datos = cur.fetchall()


    return render_template ('employees.html', datos = datos)

@app.route('/search/appointments/manager',methods =['POST', 'GET'])
def search_appointments_manager():
    if request.method == 'POST':
        busqueda= request.form.get("buscar",False)
        filtro= request.form.get("filtro",False)
        busqueda= string.capwords(busqueda)
        session['x'] = busqueda
        session['y'] = filtro
        cur = mysql.connection.cursor()
        if filtro=="consultorio":
            cur.execute('SELECT * FROM appointments WHERE Consultorio=%s AND Sucursal=%s',[busqueda,  session['sucursal']])
            datos = cur.fetchall()
            print(busqueda)
            print(filtro)
        elif filtro == "nombre":
            cur.execute('SELECT * FROM appointments WHERE Doctor=%s AND Sucursal=%s', [busqueda,  session['sucursal']])
            datos = cur.fetchall()
        else:
            cur.execute('SELECT * FROM appointments WHERE Sucursal=%s' , [session['sucursal']])
            datos = cur.fetchall()
        return render_template('appointments_manager.html', datos=datos)

#Generar PDF
@app.route('/download/report/pdf')
def download_report():
    pdf = Files.download_report()
    return pdf

@app.route('/download/report/excel')
def download_report_excel():
   xls= Files.download_report_excel()
   return xls

@app.route('/download/report_appointments/pdf')
def dowload_report_pdf_appointments_manager():
    pdf=Files.download_report_pdf_manager()
    return pdf

@app.route('/download/report_excel/manager')
def dowload_report_excel_appointments_manager():
   xls= Files.download_report_excel_manager()
   return xls

@app.route('/edit_employee/<id>')
def obtener_id(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM employees WHERE Sucursal = %s AND ID=%s ', [session['sucursal'], id])
    dato = cur.fetchall()
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM job')
    datos = cur.fetchall()
    cur.execute('SELECT * FROM subsidiary')
    datos2 = cur.fetchall()
    cur.execute(
        'SELECT `Numero`,`Nombre Sucursal` FROM doctors_office WHERE `Nombre Sucursal` = %s GROUP BY `Nombre Sucursal`,`Numero` ORDER BY `Numero`',
        [session['sucursal']])
    datos3 = cur.fetchall()

    return render_template('edit_employee.html', dato = dato[0], opcion=datos,opcion2=datos2,opcion3=datos3)



if __name__ == '__main__':
	app.run(debug = True, port = 8000, host = '0.0.0.0')