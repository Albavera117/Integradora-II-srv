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
from flask import Markup



app = Flask(__name__)
mysql= MySQL(app)

#Conexion a MySQL
app.config['MYSQL_HOST'] = 'dentalcarebd.cvuv52n8tzsh.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'Userdentalcare'
app.config['MYSQL_PASSWORD'] = 'utez_123?'
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
        servicio1 = request.form['servicio1']
        servicio2 = request.form.get('servicio2',"")
        ##COMPROBAR DISPONIBILIDAD DE HORARIO
        fecha2=(fecha+' '+hr)
        cur = mysql.connection.cursor()
        cur.callproc('registrar_cita',[nombre,apellido,telefono,fecha,hr,sucursal,servicio1,servicio2])
        disponibilidad = cur.fetchall()[0][0]
        cur.close()
        mysql.connection.commit()
        if bool(disponibilidad):
            ##RECUPERAR FOLIO
            cur = mysql.connection.cursor()
            cur.execute('SELECT MAX(Folio) FROM appointments')
            folio=cur.fetchall()[0][0]
            # consulta para pdf
            cur.execute('SELECT Folio,Doctor,Paciente,Turno,Telefono,Fecha,`Fecha Cancelación`,Consultorio,`Tiempo Consulta`,Costo,`Estado Cita`,Sucursal,Cobro,ID FROM appointments WHERE Folio=%s', [folio])
            comprobante = cur.fetchall()
            session['cita'] = comprobante
            ##fin consulta pdf
            flash(Markup('Cita Agendada - FOLIO:{} click <a href="/comprobante_pdf" class="alert-link">aquí</a> para descargar su comprobante'.format(folio)))
            return redirect(url_for('indice'))
        else:
            flash("No Hay Horario Disponible - Trata Con Otro Horario - Lo Sentimos")
            return redirect(url_for('indice'))

@app.route('/cancelar_cita' ,methods = ['POST'])
def cancelar_cita():
    folio = request.form['folio']
    num_tel = request.form['num_tel']
    
    cur = mysql.connection.cursor()
    cur.callproc('cancelar_cita',[folio,num_tel])
    validar = cur.fetchall()[0][0]
    cur.close()
    mysql.connection.commit()
    if validar==0:
        flash("La Cita No Existe")
        return redirect(url_for('indice'))
    elif validar==1:
        flash("La Cita Se Encuentra Caduca")
        return redirect(url_for('indice'))
    elif validar==2:
        flash("La cita Se Encuentra Cancelada o Atendida")
        return redirect(url_for('indice'))
    elif validar==3:
        cur = mysql.connection.cursor()
        # consulta para crear pdf
        cur.execute('SELECT Folio,Doctor,Paciente,Turno,Telefono,Fecha,`Fecha Cancelación`,Consultorio,`Tiempo Consulta`,Costo,`Estado Cita`,Sucursal,Cobro,ID FROM appointments WHERE Folio=%s', [folio])
        comprobante2 = cur.fetchall()
        session['cita'] = comprobante2
        # fin consulta pdf
        flash(Markup('Cita con el folio {} cancelada click <a href="/cancelar_cita_pdf" class="alert-link">aquí</a> para descargar su comprobante'.format(folio)))
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
            estatus = str(data[0][6])
            if emailBD == email and passwordBD == password and estatus=="Activo":
                #Creacion de sesion
                session['email'] = email
                session['sucursal'] = sucursalDB
                session['nombre'] = data[0][2]
                session['ID'] = data[0][5]
                flash("Bienvenido {}".format(str(data[0][2])))
                if data[0][3] == "Doctor":
                    return redirect(url_for('dashboard_doctor'))
                elif data[0][3] == "Manager":
                    return redirect(url_for('dashboard_manager'))
                else:
                    return redirect(url_for('dashboard_assistant'))
            elif estatus=="Inactivo":
                flash("Usuario Inactivo")
                return redirect(url_for('login'))

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

@app.route('/appointments_assistant',methods = ['GET','POST'])
@requires_access_level('Asistente')
def appointments_assistant ():
    #Query de datos para llenar tabla de registros
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM appointments WHERE Sucursal=%s ORDER BY Folio',[session['sucursal']])
    datos = cur.fetchall()

    if request.method == 'POST':
        folio = request.form['folio']
        pago = request.form['pago']
        IDuser = session['ID']
        cur = mysql.connection.cursor()
        cur.callproc('pagar',[folio,pago,IDuser])
        tupla = cur.fetchall()
        boleano = tupla[0][0]
        numerico = tupla[0][1]
        cur.close()
        mysql.connection.commit()

        if bool(boleano)==False and numerico==0:
            flash("La Cita con Folio {} No Existe".format(folio))
            return redirect(url_for('appointments_assistant'))
        elif bool(boleano)==False and numerico==1:
            flash("La Cita con Folio {} Ya se Encuentra Pagada".format(folio))
            return redirect(url_for('appointments_assistant'))
        elif bool(boleano)==True and numerico==-1:
            flash("Debes introducir algún numero positivo")
            return redirect(url_for('appointments_assistant'))
        elif bool(boleano)==True and numerico>0:
            flash("La Cita con Folio {} Ha Sido Pagada - Total de Cambio {}".format(folio,numerico))
            return redirect(url_for('appointments_assistant'))
        elif bool(boleano)==True and numerico==0:
            flash("La Cita con Folio {} Ha sido Pagada".format(folio))
            return redirect(url_for('appointments_assistant'))
        return redirect(url_for('appointments_assistant'))

    return render_template ('appointments_assistant.html', datos = datos,sucursal=session['sucursal'],asistente=session['nombre'])

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
        servicio1 = request.form['servicio1']
        servicio2 = request.form.get('servicio2',"")
        ##COMPROBAR DISPONIBILIDAD DE HORARIO
        fecha2=(fecha+' '+hr)
        cur = mysql.connection.cursor()
        cur.callproc('registrar_cita',[nombre,apellido,telefono,fecha,hr,sucursal,servicio1,servicio2])
        disponibilidad = cur.fetchall()[0][0]
        cur.close()
        mysql.connection.commit()
        if bool(disponibilidad):
            ##RECUPERAR FOLIO
            cur = mysql.connection.cursor()
            cur.execute('SELECT MAX(Folio) FROM appointments')
            folio=cur.fetchall()[0][0]
            # pdf comprobante
            cur.execute('SELECT Folio,Doctor,Paciente,Turno,Telefono,Fecha,`Fecha Cancelación`,Consultorio,`Tiempo Consulta`,Costo,`Estado Cita`,Sucursal,Cobro,ID FROM appointments WHERE Folio=%s', [folio])
            comprobante = cur.fetchall()
            session['cita'] = comprobante
            flash(Markup('Cita Agendada - FOLIO:{} click <a href="/comprobante_pdf" class="alert-link">aquí</a> para descargar su comprobante'.format(folio)))
            return redirect(url_for('register_appointment'))
        else:
            flash("No Hay Horario Disponible - Trata Con Otro Horario - Lo Sentimos")
            return redirect(url_for('register_appointment'))

    return render_template('register_appointment.html', opcion=datos,sucursal=session['sucursal'],asistente=session['nombre'])


@app.route('/employees')
@requires_access_level('Manager')
def employees ():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM employees WHERE Sucursal = %s ORDER BY Sucursal',[session['sucursal']])
    session['x'] = None
    session['y'] = None
    datos = cur.fetchall()


    return render_template ('employees.html', datos = datos,sucursal=session['sucursal'],manager=session['nombre'])
    #id de empleado dato[6]





@app.route('/register_employees', methods = ['GET', 'POST'])
@requires_access_level('Manager')
def register_employees():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM job')
    datos = cur.fetchall()
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
        consultorio= request.form.get('consultorio',0)
        cur = mysql.connection.cursor()
        cur.callproc('registrar_empleado',[puesto,sucursal,nombre,apellido,email,telefono,contraseña,consultorio])
        cur.close()
        mysql.connection.commit()
        flash("Registro exitoso")
        return redirect(url_for('register_employees'))

    return render_template ('register_employees.html',opcion=datos,opcion3=datos3, sucursal=session['sucursal'],manager=session['nombre'])
    

@app.route('/appointments_manager')
@requires_access_level('Manager')
def appointments_manager ():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM appointments WHERE Sucursal= %s ORDER BY Folio',[session['sucursal']])
    session['x'] = None
    session['y'] = None
    datos = cur.fetchall()

    return render_template ('appointments_manager.html', datos = datos,sucursal=session['sucursal'],manager=session['nombre'])

@app.route('/appointments_doctor', methods=['GET','POST'])
@requires_access_level('Doctor')
def appointments_doctor ():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM appointments WHERE Sucursal = %s AND Doctor = %s ORDER BY Folio',[session['sucursal'],session['nombre']])
    datos = cur.fetchall()
    session['fecha1'] = None
    session['fecha2'] = None
    if request.method == 'POST':
        folio = request.form['folio']
        pago = request.form['pago']
        IDuser = session['ID']
        cur = mysql.connection.cursor()
        print(pago)
        cur.callproc('pagar',[folio,pago,IDuser])
        tupla = cur.fetchall()
        boleano = tupla[0][0]
        numerico = tupla[0][1]
        cur.close()
        mysql.connection.commit()
        if bool(boleano)==False and numerico==0:
           flash("La Cita con Folio {} No Existe".format(folio))
           return redirect(url_for('appointments_doctor'))
        elif bool(boleano)==False and numerico==1:
            flash("La Cita con Folio {} Ya se Encuentra Pagada".format(folio))
            return redirect(url_for('appointments_doctor'))
        elif bool(boleano)==True and numerico==-1:
            flash("Debes introducir algún numero positivo")
            return redirect(url_for('appointments_doctor'))
        elif bool(boleano)==True and numerico>0:
            flash("La Cita con Folio {} Ha Sido Pagada - Total de Cambio {}".format(folio,numerico))
            return redirect(url_for('appointments_doctor'))
        elif bool(boleano)==True and numerico==0:
            flash("La Cita con Folio {} Ha sido Pagada".format(folio))
            return redirect(url_for('appointments_doctor'))
    

    return render_template ('appointments_doctor.html', datos = datos,doctor=session['nombre'])

@app.route('/dashboard_doctor')
@requires_access_level('Doctor')
def dashboard_doctor ():
    return render_template ('dashboard_doctor.html',doctor=session['nombre'])

@app.route('/dashboard_manager')
@requires_access_level('Manager')
def dashboard_manager ():
    return render_template ('dashboard_manager.html',manager=session['nombre'])

@app.route('/dashboard_assistant')
@requires_access_level('Asistente')
def dashboard_assistant ():
    return render_template ('dashboard_assistant.html',asistente=session['nombre'])

@app.route('/search',methods =['POST', 'GET'])
def search():
    if request.method == 'POST':
        busqueda= request.form.get("buscar",False).capitalize()
        filtro = request.form.get("filtro", False)
        session['x'] = busqueda
        session['y'] = filtro
        cur = mysql.connection.cursor()
        cur.callproc('busqueda_empleado',[busqueda,filtro,session['sucursal']])
        datos = cur.fetchall()
        cur.close()
        mysql.connection.commit()


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
        cur.callproc('busqueda_cita',[busqueda,filtro,session['sucursal']])
        datos = cur.fetchall()
        cur.close()
        mysql.connection.commit()
        return render_template('appointments_manager.html', datos=datos)

@app.route('/busqueda_fechas_assistant', methods=['POST', 'GET'])
def busqueda_fechas_assistant():
    if request.method == 'POST':
        fecha1=request.form.get('fecha',False)
        fecha2 = request.form.get('fecha2', False)
        cur = mysql.connection.cursor()
        cur.callproc('busqueda_fechas_asistente',[fecha1,fecha2,session['sucursal']])
        datos = cur.fetchall()
        cur.close()
        mysql.connection.commit()
        return render_template('appointments_assistant.html',datos = datos,sucursal=session['sucursal'])

@app.route('/busqueda_fechas_doctor', methods=['POST', 'GET'])
def busqueda_fechas_doctor():
    if request.method == 'POST':
        fecha1 = request.form.get('fecha',False)
        fecha2 = request.form.get('fecha2', False)
        session['fecha1'] = fecha1
        session['fecha2'] = fecha2
        cur = mysql.connection.cursor()
        cur.callproc('busqueda_fechas_doctor',[fecha1,fecha2,session['ID'],session['sucursal']])
        datos = cur.fetchall()
        cur.close()
        mysql.connection.commit()
        return render_template('appointments_doctor.html',datos = datos,doctor=session['nombre'])

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

#pdf comprobante de cita
@app.route('/comprobante_pdf')
def comprobante_pdf():
    pdf=Files.comprobante_pdf()
    return pdf

#pdf comprobante cita cancelada
@app.route('/cancelar_cita_pdf')
def cancelar_cita_pdf():
    pdf=Files.cancelar_cita_pdf()
    return pdf
@app.route('/pdf_doctor')
def pdf_doctor():
    pdf=Files.citas_doctor()
    return pdf

@app.route('/excel_doctor')
def excel_doctor():
    xls=Files.citas_doctor_excel()
    return xls

@app.route('/busqueda_asistente_consultorio_doctor', methods=['POST', 'GET'])
def busqueda_asistente_consultorio_doctor():
    if request.method == 'POST':
        busqueda= request.form.get("buscar",False)
        filtro= request.form.get("check",False)
        busqueda= string.capwords(busqueda)
        session['x'] = busqueda
        session['y'] = filtro
        cur = mysql.connection.cursor()
        cur.callproc('busqueda_cita',[busqueda,filtro,session['sucursal']])
        datos = cur.fetchall()
        cur.close()
        mysql.connection.commit()
        print(busqueda)
        print(filtro)
        print(datos)
        return render_template('appointments_assistant.html', datos=datos)



@app.route('/edit_employee',methods =['POST', 'GET'])
def edit_employee():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        userid = request.form['userid']
        cur.execute('SELECT * FROM employees WHERE Sucursal = %s AND ID=%s ', [session['sucursal'], userid])
        datos = cur.fetchall()
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM job')
        datos2 = cur.fetchall()
        cur.execute('SELECT `Numero`,`Nombre Sucursal` FROM doctors_office WHERE `Nombre Sucursal` = %s GROUP BY `Nombre Sucursal`,`Numero` ORDER BY `Numero`',[session['sucursal']])
        datos3 = cur.fetchall()
    

    return render_template('edit_employee.html', datos = datos, opcion=datos2,opcion3=datos3,id=userid)

@app.route("/ajaxdetalles",methods=["POST","GET"])
def ajaxdetalles():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        userid = request.form['citaid']

        cur.execute("SELECT * FROM appointments WHERE Folio = %s", [userid])
        citas = cur.fetchall()

        cur.execute("SELECT Nombre FROM encargos_pagos WHERE `ID Cita`= %s",[userid])
        encargadas=cur.fetchall()

        cur.execute("SELECT * FROM relationship_appointments WHERE Folio = %s",[userid])
        servicios = cur.fetchall()
    return render_template('modal.html',citas=citas,servicios=servicios,encargadas=encargadas)

@app.route("/ajaxeditar",methods=["POST","GET"])
def ajaxeditar():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        userid = request.form['citaid']

        cur.execute("SELECT * FROM appointments WHERE Folio = %s", [userid])
        appointments = cur.fetchall()


        cur.execute("SELECT * FROM relationship_appointments WHERE Folio = %s",[userid])
        servicios = cur.fetchall()
    return render_template('edit_appointments.html',appointments=appointments,servicios=servicios)

@app.route("/editar/empleado",methods=["POST","GET"])
def editar_empleado():
    cur=mysql.connection.cursor()
    if request.method == "POST":
        nombre = request.form['nombre']
        apellidos = request.form["apellido"]
        correo = request.form["email"]
        telefono = request.form["phone"]
        estatus = request.form["estatus"]
        contraseña = request.form.get("password","")
        id = request.form["id"]
        cur = mysql.connection.cursor()
        cur.callproc('editar_personal',[estatus,nombre,apellidos,correo,telefono,contraseña,id])
        cur.close()
        mysql.connection.commit()
        flash("Datos de Usuario Actualizado")
        return redirect(url_for('employees'))

@app.route("/editar/cita",methods=["POST","GET"])
def editar_cita():
    cur=mysql.connection.cursor()
    if request.method == "POST":
        folio = request.form['folio']
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        telefono = request.form['telefono']
        estatus = request.form['estatus']
        fecha = request.form['fecha']
        hora = request.form['hora']
        costo = request.form['costo']
        duracioncita = request.form['duracion']
        cur = mysql.connection.cursor()
        cur.callproc('modificar_cita',[folio,nombre,apellidos,telefono,estatus,fecha,hora,costo,duracioncita,session['sucursal']])
        arreglo = cur.fetchall()
        disponibilidad=arreglo[0][0]
        bandera=arreglo[0][1]
        cur.close()
        mysql.connection.commit()
        if bool(disponibilidad)==True and bandera==1:
            cur = mysql.connection.cursor()
            # consulta para pdf
            cur.execute('SELECT Folio,Doctor,Paciente,Turno,Telefono,Fecha,`Fecha Cancelación`,Consultorio,`Tiempo Consulta`,Costo,`Estado Cita`,Sucursal,Cobro,ID FROM appointments WHERE Folio=%s', [folio])
            comprobante = cur.fetchall()
            session['cita'] = comprobante
            ##fin consulta pdf
            flash(Markup('Datos Cita Actualizados - FOLIO:{} click <a href="/comprobante_pdf" class="alert-link">aquí</a> para descargar su comprobante'.format(folio)))
            return redirect(url_for('appointments_assistant'))
        elif bool(disponibilidad)==False and bandera==0:
            flash("No Hay Horario Disponible - Trata Con Otro Horario - Lo Sentimos")
            return redirect(url_for('appointments_assistant'))
        elif bool(disponibilidad)==True and bandera==0:
            flash("El Cobro de la Cuenta No Puede ser Menor al Pago Abonado")
            return redirect(url_for('appointments_assistant'))
        return redirect(url_for('appointments_assistant'))



if __name__ == '__main__':
	app.run(debug = True, port = 8000, host = '0.0.0.0')