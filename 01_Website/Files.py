
from flask import Flask,Response
from flask import request, redirect, url_for, flash,session
from flask import render_template,make_response
from flask import url_for,session
from flask_mysqldb import MySQL
from fpdf import FPDF
from datetime import date,datetime
import io
import xlwt


app = Flask(__name__)
mysql= MySQL(app)
app.config['MYSQL_HOST'] = 'testdb-1.c9uecaufvfyj.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'Userdentalcare'
app.config['MYSQL_PASSWORD'] = 'utez_123?'
app.config['MYSQL_DB'] = 'dentalcare'

app.secret_key = 'd3nt4lcl1n1c'
#pdf empleados_manager
def download_report():
    busqueda = session['x']
    filtro = session['y']


    print(busqueda)


    class PDF(FPDF):

        def header(self):
            # Logo
            self.image('static/dashboard/img/2.png', x=10, y=10, w=20, h=20)


            self.set_font('Arial', 'B', 25)

            # Title
            self.cell(w=0, h=20, txt='Reporte Empleados '+str(today), border=0, ln=1,
                      align='C', fill=0)

            # Line break
            self.ln(5)

        # Page footer
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-20)
            self.set_x(10)
            # Arial italic 8
            self.set_font('Arial', 'I', 12)

            # Page number
            self.cell(w=0, h=10, txt='Página ' + str(self.page_no()) + '/{nb}', border=0,
                      align='C', fill=0)

            # Instantiation of inherited class
    if busqueda == None:

        today = date.today().strftime('%d-%m-%Y')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM employees WHERE Sucursal=%s' , [session['sucursal']])
        result = cur.fetchall()

        pdf = PDF('L','mm','A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_left_margin(35)

        col_width = 50
        col_width2 = 25
        pdf.ln(1)
        pdf.set_font('Arial', 'B', 10)
        pdf.set_draw_color(r=34, g=57, b=110)
        th = 5

        pdf.cell(col_width, h=5, txt='Nombre', border=1, fill=0, align='C')
        pdf.cell(col_width, h=5, txt='Télefono', border=1, fill=0, align='C')
        pdf.cell(col_width, h=5, txt='Correo', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Puesto', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Sucursal', border=1, fill=0, align='C')
        pdf.multi_cell(col_width2, h=5, txt='Estatus', border=1, fill=0, align='C')
        for row in result:
            pdf.set_font('Arial', '', 10)
            pdf.cell(col_width, th, row[0], border=1, fill=0)
            pdf.cell(col_width, th, row[1], border=1, fill=0)
            pdf.cell(col_width, th, row[2], border=1, fill=0)
            pdf.cell(col_width2, th, row[4], border=1, fill=0)
            pdf.cell(col_width2, th, row[6], border=1, fill=0)
            pdf.cell(col_width2, th, row[3], border=1, fill=0)
            pdf.ln(th)
    elif filtro == 'puesto':

        today = date.today().strftime('%d-%m-%Y')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM employees WHERE Cargo=%s AND Sucursal=%s',[busqueda, session['sucursal']])
        result = cur.fetchall()

        pdf = PDF('L','mm','A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_left_margin(35)

        col_width = 50
        col_width2 = 25
        pdf.ln(1)
        pdf.set_font('Arial', 'B', 10)
        pdf.set_draw_color(r=34, g=57, b=110)
        th = 5

        pdf.cell(col_width, h=5, txt='Nombre', border=1, fill=0, align='C')
        pdf.cell(col_width, h=5, txt='Télefono', border=1, fill=0, align='C')
        pdf.cell(col_width, h=5, txt='Correo', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Puesto', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Sucursal', border=1, fill=0, align='C')
        pdf.multi_cell(col_width2, h=5, txt='Estatus', border=1, fill=0, align='C')
        for row in result:
            pdf.set_font('Arial', '', 10)
            pdf.cell(col_width, th, row[0], border=1, fill=0)
            pdf.cell(col_width, th, row[1], border=1, fill=0)
            pdf.cell(col_width, th, row[2], border=1, fill=0)
            pdf.cell(col_width2, th, row[4], border=1, fill=0)
            pdf.cell(col_width2, th, row[6], border=1, fill=0)
            pdf.cell(col_width2, th, row[3], border=1, fill=0)
            pdf.ln(th)

    elif filtro == 'estatus':
            today = date.today().strftime('%d-%m-%Y')

            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM employees WHERE Estatus=%s AND Sucursal=%s', [busqueda, session['sucursal']])
            result = cur.fetchall()

            pdf = PDF('L', 'mm', 'A4')
            pdf.alias_nb_pages()
            pdf.add_page()
            pdf.set_left_margin(35)

            col_width = 50
            col_width2 = 25
            pdf.ln(1)
            pdf.set_font('Arial', 'B', 10)
            pdf.set_draw_color(r=34, g=57, b=110)
            th = 5

            pdf.cell(col_width, h=5, txt='Nombre', border=1, fill=0, align='C')
            pdf.cell(col_width, h=5, txt='Télefono', border=1, fill=0, align='C')
            pdf.cell(col_width, h=5, txt='Correo', border=1, fill=0, align='C')
            pdf.cell(col_width2, h=5, txt='Puesto', border=1, fill=0, align='C')
            pdf.cell(col_width2, h=5, txt='Sucursal', border=1, fill=0, align='C')
            pdf.multi_cell(col_width2, h=5, txt='Estatus', border=1, fill=0, align='C')
            for row in result:
                pdf.set_font('Arial', '', 10)
                pdf.cell(col_width, th, row[0], border=1, fill=0)
                pdf.cell(col_width, th, row[1], border=1, fill=0)
                pdf.cell(col_width, th, row[2], border=1, fill=0)
                pdf.cell(col_width2, th, row[4], border=1, fill=0)
                pdf.cell(col_width2, th, row[6], border=1, fill=0)
                pdf.cell(col_width2, th, row[3], border=1, fill=0)
                pdf.ln(th)

    else:

        today = date.today().strftime('%d-%m-%Y')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM employees WHERE Sucursal=%s' , [session['sucursal']])
        result = cur.fetchall()

        pdf = PDF('L','mm','A4')
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_left_margin(35)

        col_width = 50
        col_width2 = 25
        pdf.ln(1)
        pdf.set_font('Arial', 'B', 10)
        pdf.set_draw_color(r=34, g=57, b=110)
        th = 5

        pdf.cell(col_width, h=5, txt='Nombre', border=1, fill=0, align='C')
        pdf.cell(col_width, h=5, txt='Télefono', border=1, fill=0, align='C')
        pdf.cell(col_width, h=5, txt='Correo', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Puesto', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Sucursal', border=1, fill=0, align='C')
        pdf.multi_cell(col_width2, h=5, txt='Estatus', border=1, fill=0, align='C')
        for row in result:
            pdf.set_font('Arial', '', 10)
            pdf.cell(col_width, th, row[0], border=1, fill=0)
            pdf.cell(col_width, th, row[1], border=1, fill=0)
            pdf.cell(col_width, th, row[2], border=1, fill=0)
            pdf.cell(col_width2, th, row[4], border=1, fill=0)
            pdf.cell(col_width2, th, row[6], border=1, fill=0)
            pdf.cell(col_width2, th, row[3], border=1, fill=0)
            pdf.ln(th)
    pdf=Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                    headers={'Content-Disposition': 'attachment;filename=Employee_Report.pdf'})
    return pdf

#excel_empleados_manager
def download_report_excel():
    busqueda = session['x']
    filtro = session['y']
    if busqueda == None:

        today = date.today().strftime('%d-%m-%Y')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM employees WHERE Sucursal=%s' , [session['sucursal']])
        result = cur.fetchall()
        # output in bytes
        output = io.BytesIO()
        # create WorkBook object
        workbook = xlwt.Workbook()
        # add a sheet
        sh = workbook.add_sheet('Employee Report')

        # add headers
        sh.write(0, 0, 'Nombre')
        sh.write(0, 1, 'Télefono')
        sh.write(0, 2, 'Correo')
        sh.write(0, 3, 'Puesto')
        sh.write(0, 4, 'Sucursal')
        sh.write(0, 5, 'Estatus')

        idx = 0
        for row in result:
            sh.write(idx + 1, 0, row[0])
            sh.write(idx + 1, 1, row[1])
            sh.write(idx + 1, 2, row[2])
            sh.write(idx + 1, 3, row[4])
            sh.write(idx + 1, 4, row[6])
            sh.write(idx + 1, 5, row[3])
            idx += 1

        workbook.save(output)
        output.seek(0)
    elif filtro == 'puesto':
        today = date.today().strftime('%d-%m-%Y')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM employees WHERE Cargo=%s AND Sucursal=%s', [busqueda, session['sucursal']])
        result = cur.fetchall()
        # output in bytes
        output = io.BytesIO()
        # create WorkBook object
        workbook = xlwt.Workbook()
        # add a sheet
        sh = workbook.add_sheet('Employee Report')

        # add headers
        sh.write(0, 0, 'Nombre')
        sh.write(0, 1, 'Télefono')
        sh.write(0, 2, 'Correo')
        sh.write(0, 3, 'Puesto')
        sh.write(0, 4, 'Sucursal')
        sh.write(0, 5, 'Estatus')

        idx = 0
        for row in result:
            sh.write(idx + 1, 0, row[0])
            sh.write(idx + 1, 1, row[1])
            sh.write(idx + 1, 2, row[2])
            sh.write(idx + 1, 3, row[4])
            sh.write(idx + 1, 4, row[6])
            sh.write(idx + 1, 5, row[3])
            idx += 1

        workbook.save(output)
        output.seek(0)

    elif filtro == 'estatus':
        today = date.today().strftime('%d-%m-%Y')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM employees WHERE Estatus=%s AND Sucursal=%s', [busqueda, session['sucursal']])
        result = cur.fetchall()
        # output in bytes
        output = io.BytesIO()
        # create WorkBook object
        workbook = xlwt.Workbook()
        # add a sheet
        sh = workbook.add_sheet('Employee Report')

        # add headers
        sh.write(0, 0, 'Nombre')
        sh.write(0, 1, 'Télefono')
        sh.write(0, 2, 'Correo')
        sh.write(0, 3, 'Puesto')
        sh.write(0, 4, 'Sucursal')
        sh.write(0, 5, 'Estatus')

        idx = 0
        for row in result:
            sh.write(idx + 1, 0, row[0])
            sh.write(idx + 1, 1, row[1])
            sh.write(idx + 1, 2, row[2])
            sh.write(idx + 1, 3, row[4])
            sh.write(idx + 1, 4, row[6])
            sh.write(idx + 1, 5, row[3])
            idx += 1

        workbook.save(output)
        output.seek(0)
    else:
        print("Else")
        today = date.today().strftime('%d-%m-%Y')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM employees WHERE Sucursal=%s' , [session['sucursal']])
        result = cur.fetchall()

        # output in bytes
        output = io.BytesIO()
        # create WorkBook object
        workbook = xlwt.Workbook()
        # add a sheet
        sh = workbook.add_sheet('Employee Report')

        # add headers
        sh.write(0, 0, 'Nombre')
        sh.write(0, 1, 'Télefono')
        sh.write(0, 2, 'Correo')
        sh.write(0, 3, 'Puesto')
        sh.write(0, 4, 'Sucursal')
        sh.write(0, 5, 'Estatus')

        idx = 0
        for row in result:
            sh.write(idx + 1, 0, row[0])
            sh.write(idx + 1, 1, row[1])
            sh.write(idx + 1, 2, row[2])
            sh.write(idx + 1, 3, row[4])
            sh.write(idx + 1, 4, row[6])
            sh.write(idx + 1, 5, row[3])
            idx += 1

        workbook.save(output)
        output.seek(0)
    xls=Response(output, mimetype="application/ms-excel",
                    headers={"Content-Disposition": "attachment;filename=employee_report " +today +".xls"})
    return xls

#PDF citas_manager
def download_report_pdf_manager():
    busqueda =  session['x']
    filtro = session['y']
    suma_dinero = 0
    suma_tiempo = 0
    print(busqueda)


    class PDF(FPDF):


        def header(self):
            # Logo
            self.image('static/dashboard/img/2.png', x=10, y=10, w=20, h=20)


            self.set_font('Arial', 'B', 25)

            # Title
            self.cell(w=0, h=20, txt='Reporte Empleados '+str(today), border=0, ln=1,
                      align='C', fill=0)

            # Line break
            self.ln(5)

        # Page footer
        def footer(self):
            # Position at 1.5 cm from bottom
            self.set_y(-20)
            self.set_x(10)
            # Arial italic 8
            self.set_font('Arial', 'I', 12)

            # Page number
            self.cell(w=0, h=10, txt='Página ' + str(self.page_no()) + '/{nb}', border=0,
                      align='C', fill=0)

            # Instantiation of inherited class

    if  busqueda ==  None:

        today = date.today().strftime('%d-%m-%Y')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM appointments WHERE Sucursal=%s' , [session['sucursal']])
        result = cur.fetchall()

        pdf = PDF('L','mm',(300,450))
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_left_margin(7)

        col_width = 15
        col_width2 = 55
        col_width3 = 28
        col_width4 = 70

        pdf.ln(1)
        pdf.set_font('Arial', 'B', 10)
        pdf.set_draw_color(r=34, g=57, b=110)
        th = 5

        pdf.cell(col_width, h=5, txt='Folio', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Nombre Paciente', border=1, fill=0, align='C')
        pdf.cell(col_width3, h=5, txt='Teléfono', border=1, fill=0, align='C')
        pdf.cell(col_width3, h=5, txt='Consultorio', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Doctor', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Fecha y hora', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Tiempo en consulta', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Total pagado', border=1, fill=0, align='C')
        pdf.multi_cell(col_width2, h=5, txt='Estatus', border=1, fill=0, align='C')
        suma_dinero = 0
        suma_tiempo = 0
        for row in result:
            pdf.set_font('Arial', '', 10)
            pdf.cell(col_width, th, str(row[0]), border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[2]), border=1, fill=0)
            pdf.cell(col_width3, th, str(row[4]), border=1, fill=0)
            pdf.cell(col_width3, th, str(row[7]), border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[1]), border=1, fill=0)
            pdf.cell(col_width2, th, str(row[5]), border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[8]) + " minutos", border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[12]) + " pesos", border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[10]), border=1, fill=0, align='C')


            suma_dinero = suma_dinero + float(row[12])
            suma_tiempo = suma_tiempo + float(row[8])




            pdf.ln(th)
        suma_tiempo = suma_tiempo/60
        pdf.multi_cell(col_width, h=5, txt="", border=0, fill=0, align='C')
        pdf.multi_cell(col_width4, h=5, txt="Promedio tiempo activo: " +str(suma_tiempo) +" horas", border=0, fill=0)
        pdf.multi_cell(col_width4, h=5, txt="Ingresos generados: " + "$" + str(suma_dinero) +" pesos", border=0, fill=0)


    elif filtro == "nombre":
        today = date.today().strftime('%d-%m-%Y')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM appointments WHERE Doctor=%s AND Sucursal=%s', [busqueda, session['sucursal']])
        result = cur.fetchall()

        pdf = PDF('L', 'mm', (300, 450))
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_left_margin(7)

        col_width = 15
        col_width2 = 55
        col_width3 = 25
        col_width4 = 70

        pdf.ln(1)
        pdf.set_font('Arial', 'B', 10)
        pdf.set_draw_color(r=34, g=57, b=110)
        th = 5

        pdf.cell(col_width, h=5, txt='Folio', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Nombre Paciente', border=1, fill=0, align='C')
        pdf.cell(col_width3, h=5, txt='Teléfono', border=1, fill=0, align='C')
        pdf.cell(col_width3, h=5, txt='Consultorio', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Doctor', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Fecha y hora', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Tiempo en consulta', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Total pagado', border=1, fill=0, align='C')
        pdf.multi_cell(col_width2, h=5, txt='Estatus', border=1, fill=0, align='C')
        for row in result:
            pdf.set_font('Arial', '', 10)
            pdf.cell(col_width, th, str(row[0]), border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[2]), border=1, fill=0)
            pdf.cell(col_width3, th, str(row[4]), border=1, fill=0)
            pdf.cell(col_width3, th, str(row[7]), border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[1]), border=1, fill=0)
            pdf.cell(col_width2, th, str(row[5]), border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[8]) + " minutos", border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[12]) + " pesos", border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[10]), border=1, fill=0, align='C')

            suma_dinero = suma_dinero + float(row[12])
            suma_tiempo = suma_tiempo + float(row[8])
            pdf.ln(th)
        suma_tiempo = suma_tiempo / 60
        pdf.multi_cell(col_width, h=5, txt="", border=0, fill=0, align='C')
        pdf.multi_cell(col_width4, h=5, txt="Promedio tiempo activo: " + str(suma_tiempo) + " horas", border=0, fill=0)
        pdf.multi_cell(col_width4, h=5, txt="Ingresos generados: " + "$" + str(suma_dinero) + " pesos", border=0,
                       fill=0)
    elif filtro=="consultorio":

        today = date.today().strftime('%d-%m-%Y')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM appointments WHERE Consultorio=%s AND Sucursal=%s',[busqueda,  session['sucursal']])
        result = cur.fetchall()

        pdf = PDF('L', 'mm', (300, 450))
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_left_margin(7)

        col_width = 15
        col_width2 = 55
        col_width3 = 25
        col_width4 = 70

        pdf.ln(1)
        pdf.set_font('Arial', 'B', 10)
        pdf.set_draw_color(r=34, g=57, b=110)
        th = 5

        pdf.cell(col_width, h=5, txt='Folio', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Nombre Paciente', border=1, fill=0, align='C')
        pdf.cell(col_width3, h=5, txt='Teléfono', border=1, fill=0, align='C')
        pdf.cell(col_width3, h=5, txt='Consultorio', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Doctor', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Fecha y hora', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Tiempo en consulta', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Total pagado', border=1, fill=0, align='C')
        pdf.multi_cell(col_width2, h=5, txt='Estatus', border=1, fill=0, align='C')
        for row in result:
            pdf.set_font('Arial', '', 10)
            pdf.cell(col_width, th, str(row[0]), border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[2]), border=1, fill=0)
            pdf.cell(col_width3, th, str(row[4]), border=1, fill=0)
            pdf.cell(col_width3, th, str(row[7]), border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[1]), border=1, fill=0)
            pdf.cell(col_width2, th, str(row[5]), border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[8])+" minutos", border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[12])+ " pesos", border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[10]), border=1, fill=0, align='C')

            suma_dinero = suma_dinero + float(row[12])
            suma_tiempo = suma_tiempo + float(row[8])
            pdf.ln(th)

        suma_tiempo = suma_tiempo / 60
        pdf.multi_cell(col_width, h=5, txt="", border=0, fill=0, align='C')
        pdf.multi_cell(col_width4, h=5, txt="Promedio tiempo activo: " + str(suma_tiempo) + " horas", border=0, fill=0)
        pdf.multi_cell(col_width4, h=5, txt="Ingresos generados: " + "$" + str(suma_dinero) + " pesos", border=0,
                       fill=0)
    else:

        today = date.today().strftime('%d-%m-%Y')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM appointments WHERE Sucursal=%s' , [session['sucursal']])
        result = cur.fetchall()

        pdf = PDF('L', 'mm', (300, 450))
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_left_margin(7)

        col_width = 15
        col_width2 = 55
        col_width3 = 25
        col_width4 = 70

        pdf.ln(1)
        pdf.set_font('Arial', 'B', 10)
        pdf.set_draw_color(r=34, g=57, b=110)
        th = 5

        pdf.cell(col_width, h=5, txt='Folio', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Nombre Paciente', border=1, fill=0, align='C')
        pdf.cell(col_width3, h=5, txt='Teléfono', border=1, fill=0, align='C')
        pdf.cell(col_width3, h=5, txt='Consultorio', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Doctor', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Fecha y hora', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Tiempo en consulta', border=1, fill=0, align='C')
        pdf.cell(col_width2, h=5, txt='Total pagado', border=1, fill=0, align='C')
        pdf.multi_cell(col_width2, h=5, txt='Estatus', border=1, fill=0, align='C')
        for row in result:
            pdf.set_font('Arial', '', 10)
            pdf.cell(col_width, th, str(row[0]), border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[2]), border=1, fill=0)
            pdf.cell(col_width3, th, str(row[4]), border=1, fill=0)
            pdf.cell(col_width3, th, str(row[7]), border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[1]), border=1, fill=0)
            pdf.cell(col_width2, th, str(row[5]), border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[8]) + " minutos", border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[12]) + " pesos", border=1, fill=0, align='C')
            pdf.cell(col_width2, th, str(row[10]), border=1, fill=0, align='C')

            suma_dinero = suma_dinero + float(row[12])
            suma_tiempo = suma_tiempo + float(row[8])
            pdf.ln(th)

        suma_tiempo = suma_tiempo / 60
        pdf.multi_cell(col_width, h=5, txt="", border=0, fill=0, align='C')
        pdf.multi_cell(col_width4, h=5, txt="Promedio tiempo activo: " + str(suma_tiempo) + " horas", border=0, fill=0)
        pdf.multi_cell(col_width4, h=5, txt="Ingresos generados: " + "$" + str(suma_dinero) + " pesos", border=0,fill=0)


    pdf=Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                    headers={'Content-Disposition': 'attachment;filename=Appointments_Report.pdf'})
    return pdf

#excel citas_manager
def download_report_excel_manager():
    busqueda = session['x']
    filtro = session['y']
    suma_dinero = 0
    suma_tiempo = 0

    print(busqueda)

    if  busqueda ==  None:
        today = date.today().strftime('%d-%m-%Y')

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM appointments WHERE Sucursal=%s' , [session['sucursal']])
        result = cur.fetchall()
        # output in bytes
        output = io.BytesIO()
        # create WorkBook object
        workbook = xlwt.Workbook()
        # add a sheet
        sh = workbook.add_sheet('Appointments Report')

        # add headers
        sh.write(0, 0, 'Folio')
        sh.write(0, 1, 'Nombre Paciente')
        sh.write(0, 2, 'Télefono')
        sh.write(0, 3, 'Consultorio')
        sh.write(0, 4, 'Doctor')
        sh.write(0, 5, 'Fecha y hora')
        sh.write(0, 6, 'Tiempo en consulta')
        sh.write(0, 7, 'Total pagado')
        sh.write(0, 8, 'Estatus')



        idx = 0
        for row in result:
            sh.write(idx + 1, 0, row[0])
            sh.write(idx + 1, 1, row[2])
            sh.write(idx + 1, 2, row[4])
            sh.write(idx + 1, 3, row[7])
            sh.write(idx + 1, 4, row[1])
            sh.write(idx + 1, 5, row[5])
            sh.write(idx + 1, 6, str (row[8])+" minutos")
            sh.write(idx + 1, 7, str (row[12])+" pesos")
            sh.write(idx + 1, 8, row[10])
            idx += 1

            suma_dinero = suma_dinero + float(row[12])
            suma_tiempo = suma_tiempo + float(row[8])
        suma_tiempo = suma_tiempo / 60
        sh.write(idx + 1, 0, 'Promedio tiempo activo: ' + str(suma_tiempo) +" horas")
        sh.write(idx + 2, 0, 'Ingresos generados: ' + str(suma_dinero) +" pesos")
        workbook.save(output)
        output.seek(0)


    elif filtro == "nombre":
            today = date.today().strftime('%d-%m-%Y')

            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM appointments WHERE Doctor=%s AND Sucursal=%s', [busqueda, session['sucursal']])
            result = cur.fetchall()
            # output in bytes
            output = io.BytesIO()
            # create WorkBook object
            workbook = xlwt.Workbook()
            # add a sheet
            sh = workbook.add_sheet('Appointments Report')

            # add headers
            sh.write(0, 0, 'Folio')
            sh.write(0, 1, 'Nombre Paciente')
            sh.write(0, 2, 'Télefono')
            sh.write(0, 3, 'Consultorio')
            sh.write(0, 4, 'Doctor')
            sh.write(0, 5, 'Fecha y hora')
            sh.write(0, 6, 'Tiempo en consulta')
            sh.write(0, 7, 'Total pagado')
            sh.write(0, 8, 'Estatus')

            idx = 0

            for row in result:
                sh.write(idx + 1, 0, row[0])
                sh.write(idx + 1, 1, row[2])
                sh.write(idx + 1, 2, row[4])
                sh.write(idx + 1, 3, row[7])
                sh.write(idx + 1, 4, row[1])
                sh.write(idx + 1, 5, row[5])
                sh.write(idx + 1, 6, str(row[8]) + " minutos")
                sh.write(idx + 1, 7, str(row[12]) + " pesos")
                sh.write(idx + 1, 8, row[10])
                idx += 1
                suma_dinero = suma_dinero + float(row[12])
                suma_tiempo = suma_tiempo + float(row[8])
            suma_tiempo = suma_tiempo / 60
            sh.write(idx + 1, 0, 'Promedio tiempo activo: ' + str(suma_tiempo) + " horas")
            sh.write(idx + 2, 0, 'Ingresos generados: ' + str(suma_dinero) + " pesos")
            workbook.save(output)
            output.seek(0)

    elif filtro == "consultorio":
            today = date.today().strftime('%d-%m-%Y')

            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM appointments WHERE Consultorio=%s AND Sucursal=%s',[busqueda,  session['sucursal']])
            result = cur.fetchall()
            # output in bytes
            output = io.BytesIO()
            # create WorkBook object
            workbook = xlwt.Workbook()
            # add a sheet
            sh = workbook.add_sheet('Appointments Report')

            # add headers
            sh.write(0, 0, 'Folio')
            sh.write(0, 1, 'Nombre Paciente')
            sh.write(0, 2, 'Télefono')
            sh.write(0, 3, 'Consultorio')
            sh.write(0, 4, 'Doctor')
            sh.write(0, 5, 'Fecha y hora')
            sh.write(0, 6, 'Tiempo en consulta')
            sh.write(0, 7, 'Total pagado')
            sh.write(0, 8, 'Estatus')

            idx = 0
            for row in result:
                sh.write(idx + 1, 0, row[0])
                sh.write(idx + 1, 1, row[2])
                sh.write(idx + 1, 2, row[4])
                sh.write(idx + 1, 3, row[7])
                sh.write(idx + 1, 4, row[1])
                sh.write(idx + 1, 5, row[5])
                sh.write(idx + 1, 6, str(row[8]) + " minutos")
                sh.write(idx + 1, 7, str(row[12]) + " pesos")
                sh.write(idx + 1, 8, row[10])
                idx += 1
                suma_dinero = suma_dinero + float(row[12])
                suma_tiempo = suma_tiempo + float(row[8])
            suma_tiempo = suma_tiempo / 60
            sh.write(idx + 1, 0, 'Promedio tiempo activo: ' + str(suma_tiempo) + " horas")
            sh.write(idx + 2, 0, 'Ingresos generados: ' + str(suma_dinero) + " pesos")
            workbook.save(output)
            output.seek(0)



    else:
            today = date.today().strftime('%d-%m-%Y')

            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM appointments WHERE Sucursal=%s' , [session['sucursal']])
            result = cur.fetchall()
            # output in bytes
            output = io.BytesIO()
            # create WorkBook object
            workbook = xlwt.Workbook()
            # add a sheet
            sh = workbook.add_sheet('Appointments Report')

            # add headers
            sh.write(0, 0, 'Folio')
            sh.write(0, 1, 'Nombre Paciente')
            sh.write(0, 2, 'Télefono')
            sh.write(0, 3, 'Consultorio')
            sh.write(0, 4, 'Doctor')
            sh.write(0, 5, 'Fecha y hora')
            sh.write(0, 6, 'Tiempo en consulta')
            sh.write(0, 7, 'Total pagado')
            sh.write(0, 8, 'Estatus')

            idx = 0
            for row in result:
                sh.write(idx + 1, 0, row[0])
                sh.write(idx + 1, 1, row[2])
                sh.write(idx + 1, 2, row[4])
                sh.write(idx + 1, 3, row[7])
                sh.write(idx + 1, 4, row[1])
                sh.write(idx + 1, 5, row[5])
                sh.write(idx + 1, 6, str(row[8]) + " minutos")
                sh.write(idx + 1, 7, str(row[12]) + " pesos")
                sh.write(idx + 1, 8, row[10])
                idx += 1
                suma_dinero = suma_dinero + float(row[12])
                suma_tiempo = suma_tiempo + float(row[8])
            suma_tiempo = suma_tiempo / 60
            sh.write(idx + 1, 0, 'Promedio tiempo activo: ' + str(suma_tiempo) + " horas")
            sh.write(idx + 2, 0, 'Ingresos generados: ' + str(suma_dinero) + " pesos")
            workbook.save(output)
            output.seek(0)


    xls = Response(output, mimetype="application/ms-excel",
                           headers={"Content-Disposition": "attachment;filename=Appointments_report " + today + ".xls"})
    return xls

#Comprobante de cita
def comprobante_pdf():
    datos = session['cita']
    class PDF(FPDF):

        def header(self):
            self.image('static/dashboard/img/2.png', x=10, y=10, w=20, h=20)
            self.set_font('Arial', 'B', 25)
            self.cell(w=0, h=20, txt='Comprobante de Cita ' , border=0, ln=1,
                      align='C', fill=0)
            self.ln(5)
        def footer(self):
            self.set_y(-20)
            self.set_x(10)
            self.set_font('Arial', 'I', 12)
            self.cell(w=0, h=10, txt='Página ' + str(self.page_no()) + '/{nb}', border=0,
                      align='C', fill=0)

    today = date.today().strftime('%d-%m-%Y')

    pdf = PDF('P', 'mm', 'A4')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_left_margin(35)
    pdf.set_right_margin(15)

    col_width = 15
    col_width2 = 55
    col_width3 = 25
    col_width4 = 70

    pdf.ln(1)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_draw_color(r=34, g=57, b=110)
    th = 5
    pdf.multi_cell(col_width4, h=9, txt='', border=0, fill=0 )
    pdf.multi_cell(col_width4, h=9, txt='', border=0, fill=0 )
    pdf.cell(col_width4, h=9, txt='folio', border=1, fill=0)
    pdf.multi_cell(col_width4, h=9, txt=str(datos[0][0]), border=1, fill=0)
    pdf.cell(col_width4, h=9, txt='Paciente', border=1, fill=0)
    pdf.multi_cell(col_width4, h=9, txt=str(datos[0][2]), border=1, fill=0)
    pdf.cell(col_width4, h=9, txt='Teléfono', border=1, fill=0)
    pdf.multi_cell(col_width4, h=9, txt=str(datos[0][4]), border=1, fill=0)
    pdf.cell(col_width4, h=9, txt='Clínica', border=1, fill=0)
    pdf.multi_cell(col_width4, h=9, txt=str(datos[0][11]), border=1, fill=0)
    pdf.cell(col_width4, h=9, txt='Doctor', border=1, fill=0)
    pdf.multi_cell(col_width4, h=9, txt=str(datos[0][1]), border=1, fill=0)
    pdf.cell(col_width4, h=9, txt='Consultorio', border=1, fill=0)
    pdf.multi_cell(col_width4,h=9, txt=str(datos[0][7]), border=1, fill=0)
    pdf.cell(col_width4, h=9, txt='Fecha y hora', border=1, fill=0)
    pdf.multi_cell(col_width4,h=9, txt=str(datos[0][5]), border=1, fill=0)
    pdf.cell(col_width4, h=9, txt='Estatus', border=1, fill=0)
    pdf.multi_cell(col_width4, h=9, txt=str(datos[0][10]), border=1, fill=0)

    pdf = Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                   headers={'Content-Disposition': 'attachment;filename=Comprobante_Cita.pdf'})
    return pdf

def cancelar_cita_pdf():
    datos = session['cita']
    class PDF(FPDF):

        def header(self):
            self.image('static/dashboard/img/2.png', x=10, y=10, w=20, h=20)
            self.set_font('Arial', 'B', 25)
            self.cell(w=0, h=20, txt='Comprobante de Cita ' , border=0, ln=1,
                      align='C', fill=0)
            self.ln(5)
        def footer(self):
            self.set_y(-20)
            self.set_x(10)
            self.set_font('Arial', 'I', 12)
            self.cell(w=0, h=10, txt='Página ' + str(self.page_no()) + '/{nb}', border=0,
                      align='C', fill=0)

    today = date.today().strftime('%d-%m-%Y')

    pdf = PDF('P', 'mm', 'A4')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_left_margin(35)
    pdf.set_right_margin(15)

    col_width = 15
    col_width2 = 55
    col_width3 = 25
    col_width4 = 70

    pdf.ln(1)
    pdf.set_font('Arial', 'B', 10)
    pdf.set_draw_color(r=34, g=57, b=110)
    th = 5
    pdf.multi_cell(col_width4, h=9, txt='', border=0, fill=0 )
    pdf.multi_cell(col_width4, h=9, txt='', border=0, fill=0 )
    pdf.cell(col_width4, h=9, txt='folio', border=1, fill=0)
    pdf.multi_cell(col_width4, h=9, txt=str(datos[0][0]), border=1, fill=0)
    pdf.cell(col_width4, h=9, txt='Paciente', border=1, fill=0)
    pdf.multi_cell(col_width4, h=9, txt=str(datos[0][2]), border=1, fill=0)
    pdf.cell(col_width4, h=9, txt='Teléfono', border=1, fill=0)
    pdf.multi_cell(col_width4, h=9, txt=str(datos[0][4]), border=1, fill=0)
    pdf.cell(col_width4, h=9, txt='Clínica', border=1, fill=0)
    pdf.multi_cell(col_width4, h=9, txt=str(datos[0][11]), border=1, fill=0)
    pdf.cell(col_width4, h=9, txt='Doctor', border=1, fill=0)
    pdf.multi_cell(col_width4, h=9, txt=str(datos[0][1]), border=1, fill=0)
    pdf.cell(col_width4, h=9, txt='Consultorio', border=1, fill=0)
    pdf.multi_cell(col_width4,h=9, txt=str(datos[0][7]), border=1, fill=0)
    pdf.cell(col_width4, h=9, txt='Fecha y hora', border=1, fill=0)
    pdf.multi_cell(col_width4,h=9, txt=str(datos[0][5]), border=1, fill=0)
    pdf.cell(col_width4, h=9, txt='Estatus', border=1, fill=0)
    pdf.multi_cell(col_width4, h=9, txt=str(datos[0][10]), border=1, fill=0)

    pdf = Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf',
                   headers={'Content-Disposition': 'attachment;filename=Comprobante_Cita.pdf'})
    return pdf


