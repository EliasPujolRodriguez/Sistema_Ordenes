import tkinter as tk
from tkinter import ttk
import tkinter
from tkcalendar import DateEntry
from Connection import Connection
from datetime import date
from tkinter import messagebox
from tkinter import * 
from tkinter import filedialog
import datetime
from tkinter import *
import os
import MainView, OrderRegisterView, OrderRegisterView
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet


#Instancia de clase conexión
conn = Connection("root", "localhost", "", "muebles", "3306")
query = conn.dbConnect().cursor()

def setMainWindow():
    window.withdraw()
    MainView.createWindow()
    
def setOrderCRUDWindow():
     window.withdraw()
     OrderRegisterView.createWindow()
     
def setWindow(window):
     width = window.winfo_screenwidth()
     height = window.winfo_screenheight()
     x = (width - window.winfo_reqwidth()) // 2
     y = (height - window.winfo_reqheight()) // 2
     window.geometry(f"+{x}+{y}")

def OrdersView():
     window.withdraw()
     OrderRegisterView.createWindow();    

def updateWindow(): #Resetear búsqueda
    searchDate = cal.get_date()
    sql = ''
    currentDay = date.today()
    searchText.delete(0, END)
    searchName = searchText.get()
    
    if currentDay == searchDate and searchName == '' or searchName == '' and currentDay != '' :
       sql =f"SELECT ot.IdOrden, Concat(DATE_FORMAT(ot.FechaSolicitud, '%d-%m-%Y'), ' ', ot.HoraRegistro), Concat('$', ot.Total), c.Nombre FROM ordenestrabajo ot INNER JOIN clientes c ON c.IdCliente = ot.IdCliente ORDER BY ot.FechaSolicitud ASC;" 
    
    query.execute(sql)
    q2 = query.fetchall()
     
    for records in table.get_children():
        table.delete(records)
    
    for data in q2:
        table.insert('', 'end', value = (data[0], data[1], data[2], data[3]))  
         
def searchData():
    searchName = searchText.get()
    searchDate = cal.get_date()
    sql = ''
  
    if searchName == '':
         sql = f"SELECT ot.IdOrden, Concat(DATE_FORMAT(ot.FechaSolicitud, '%d-%m-%Y'), ' ', ot.HoraRegistro), Concat('$', ot.Total), c.Nombre FROM ordenestrabajo ot INNER JOIN clientes c ON c.IdCliente = ot.IdCliente WHERE ot.FechaSolicitud = '{searchDate}'  ORDER BY ot.FechaSolicitud ASC";
    elif searchName !='':
         sql = f"SELECT ot.IdOrden, Concat(DATE_FORMAT(ot.FechaSolicitud, '%d-%m-%Y'), ' ', ot.HoraRegistro), Concat('$', ot.Total), c.Nombre FROM ordenestrabajo ot INNER JOIN clientes c ON c.IdCliente = ot.IdCliente WHERE c.Nombre LIKE '%{searchName}%'  ORDER BY ot.FechaSolicitud ASC"; 
   
    query.execute(sql)
    q2 = query.fetchall()
     
    for records in table.get_children():
        table.delete(records)
    
    for data in q2:
        table.insert('', 'end', value = (data[0], data[1], data[2], data[3]))
        
    conn.dbConnect().cursor().close()    
    
def getPDF(): # Crea un nuevo documento PDF de las ordenes de trabajo
    try:
        record = table.selection()[0]
        item = table.item(record)
        orderId = item.get("values")[0]
        doc = canvas.Canvas("documento.pdf", pagesize=A4) #Inicializar objeto encargado de la creación de los archivos en formato PDF

        #Consulta información de la orden de trabajo
        sqlData = f"SELECT c.Nombre, c.Telefono, DATE_FORMAT(ot.FechaSolicitud, '%d-%m-%Y'), Concat('$', ot.Total) FROM clientes c INNER JOIN ordenestrabajo ot ON ot.IdCliente = c.IdCliente WHERE ot.IdOrden = {orderId};";
        
        query.execute(sqlData)
        q2 = query.fetchall()
    
        for row in q2:
            customerName = row[0]
            customerPhone = row[1]
            orderDate = row[2]
            totalAmount = str(row[3]) + " MXN"
            
        #Consulta de datos de la empresa
        sql = "SELECT DireccionTaller, Correo, TextoNota, NombreEmpresa, TelReferencia1, TelReferencia2, TelReferencia3, TelReferencia4, DireccionPlanta, LogoEmpresa FROM datosempresa;";
    
        query.execute(sql)
        q2 = query.fetchall()
    
        for row in q2:
            dir1 =  str.upper(row[0])
            email = row[1]
            orderNote = str(row[2])
            enterpriseName = str.upper(row[3])
            ph1 = row[4]
            ph2 = row[5]
            dir2 = row[8]
            enterpriseLogo = row[9]

        # Agrega logo empresa
        img = ImageReader(f"..\\Sistema python\\Resources\Logo\\{enterpriseLogo}")
        doc.drawImage(img, 20, 740, 100, 100, mask='auto')
        doc.drawString(130, 820, f"{enterpriseName}")
        doc.drawString(158, 800, f"TALLER:")
        doc.drawString(125, 780, f"RÍO FRÍO No. 174")
        doc.drawString(125, 760, f"COL. M. MIXHUICA")
        
        doc.drawString(254, 800, f"PLANTA:")
        doc.drawString(240, 780, f"FRANCISCO CANO  NO. 17")
        doc.drawString(240, 760, f"COL. SANTA MARTHA ACATITLA")
        
        doc.drawString(440, 800, f"Oficina:{ph1}")
        doc.drawString(440, 780, f"Cel:{ph2}")
        doc.drawString(440, 760, f"E-mail:{email}")
        
        doc.rect(35, 694, 557, 40)
        doc.drawString(40, 720, f"CLIENTE: {customerName}")
        doc.drawString(40, 700, f"TELÉFONO: {customerPhone}")
        doc.rect(410, 694, 183, 40)
        doc.drawString(415, 700, f"Fecha: {orderDate}")
        doc.drawString(415, 720, f"Orden de trabajo: {orderId}")
        #Encabezado principal columnas
        doc.rect(35, 135, 558, 560)#División encabezado cantidad
        doc.drawString(40,680,'Cantidad')
        doc.rect(35, 135, 95, 560)  #División encabezado 
        doc.drawString(140,680,'Descripción')
        doc.rect(130, 135, 225, 560) #División encabezado descripción
        doc.drawString(360,680,'Importe')
        doc.rect(355, 135, 100, 560) #División encabezado importe
        doc.drawString(470,680,'Total')
        width = 400
        height = 250
       
              
        sql = f"SELECT Descripcion, Cantidad, Importe FROM detallesorden WHERE IdOrden = {orderId};";
        
        query.execute(sql)
        q2 = query.fetchall()
        row_gap=0.4 
        line_y=9.1 
        #Mostrar los productos de la venta 
        for row in q2:
            descr = textFormat(row[0], 42)
            q = row[1]
            price = row[2]
            p = "$" + str(row[2])
            t = "$" + str(q * price )
            
            # Crear un estilo
            doc.drawString(45, line_y*inch, str(q)) # p Price
            styles = getSampleStyleSheet()
            styles['Normal'].wordWrap = 'none'  # Deshabilitar el ajuste de palabras
            styles['Normal'].lineBreak = 1  # Permitir saltos de línea
            descr = descr.replace('\n', '<br />\n')
            parrafo = Paragraph(descr, styles['Normal'])
            parrafo.wrapOn(doc, width, height)
            parrafo.drawOn(doc, 140, line_y*inch)
            doc.drawString(360,line_y*inch, p) # p Name
            doc.drawString(470,line_y*inch, t) # p Name
            line_y=line_y-row_gap
        
        doc.drawString(415, 120, "TOTAL:")
        doc.drawString(458.5, 120, totalAmount)
        doc.line(60, 60, 250, 60)
        doc.drawString(60, 45, "FECHA DE ENTREGA")
        doc.line(350, 60, 580, 60)
        doc.drawString(350, 45, "FIRMA DE CONFORMIDAD DEL CLIENTE")
        text = doc.beginText(60, 20)
        text.setFont("Times-Roman", 10)
        text.textLines(f"NOTA: {orderNote}")
        doc.drawText(text)
        doc.save()
  
    except IndexError:
         return tk.messagebox.showerror(title="Error", message="Debes de seleccionar una orden antes de poder generar el PDF")

def textFormat(descr, lineLength): #Función que va a darle un formato de salto de línea de los caracteres relacionados a los productos registrados en la orden
     resultado = ""
     for i in range(0, len(descr), lineLength):
        if len(descr) >= lineLength: 
            resultado += descr[i:i + lineLength] + "\n"
        elif len(descr) <= lineLength:
             resultado = descr
     return resultado
    
def showOrderDetail():
     try:
        record = table.selection()[0]
        item = table.item(record)
        orderId = item.get("values")[0]
        sql = f"SELECT detord.IdOrden, detord.Cantidad, detord.Descripcion,  detord.Importe, detord.IdDetalleOrden FROM detallesorden detord INNER JOIN ordenestrabajo ordt ON detord.IdOrden = ordt.IdOrden WHERE ordt.IdOrden = {orderId} ORDER BY detord.Descripcion ASC;"
        
        query.execute(sql)
        q2 = query.fetchall()
     
        for records in detailTable.get_children():
            detailTable.delete(records)
    
        for data in q2:
            detailTable.insert('', 'end', value = (data[0], data[1], textFormat(data[2], 30), data[3], data[4]))   
      
     except IndexError:
        return tk.messagebox.showerror(title="Error", message="Debes de seleccionar una orden antes de ver el detalle de la orden de trabajo")
     
def showOrderDetailUpd(): #Función que va a mostrar los datos del detalle de la orden seleccionada
     try:
        record = detailTable.selection()[0]
        item = detailTable.item(record)
        orderDetailId = item.get("values")[4]
        
        sql = f"SELECT Cantidad, Descripcion,  Importe , IdDetalleOrden FROM detallesorden WHERE IdDetalleOrden = {orderDetailId}";
        query.execute(sql)
        row = query.fetchall()
     
        for data in row:
            qt = data[0] 
            desc = data[1] 
            price = data[2] 
            
        qtText.insert(0, qt)
        descText.insert(0, desc)
        priceText.insert(0, price)
        
     except IndexError:
        return tk.messagebox.showerror(title="Error", message="Debes de seleccionar una orden de trabajo antes de editar sus datos")

def deleteProduct(): #Eliminar producto contenido en la orden de trabajo
     try:
        record = detailTable.selection()[0]
        item = detailTable.item(record)
        orderId = item.get("values")[0]
        orderDetailId = item.get("values")[4]
        
     except IndexError:
        return tk.messagebox.showerror(title="Error", message="Debes de seleccionar una orden de trabajo antes de eliminar sus datos")
     
     sql = f"DELETE FROM detallesorden WHERE IdDetalleOrden = {orderDetailId}"
     query.execute(sql)
     conn.dbConnect().commit()
     #Actualizar el monto total de la orden de trabajo
     searchSql2 = f"SELECT SUM(Importe * Cantidad) FROM detallesorden WHERE IdOrden = {orderId}"
     query.execute(searchSql2)
     q2 = query.fetchall()
    
     for i in q2:
            total = i[0]
      
     sql3 = "UPDATE ordenestrabajo SET Total = %s WHERE IdOrden = %s"
     values = (total, orderId)
     query.execute(sql3, values)
     conn.dbConnect().commit()
     tk.messagebox.showinfo(title="Operación realizada correctamente", message="Se ha actualizado el monto total de la orden de compra correctamente y se ha eliminado el producto seleccionado satisfactoriamente")
     showOrderDetailUpd()

def deleteOrder(): #Función que va a eliminar la orden seleccionada
    try:
       record = table.selection()[0]
       item = table.item(record)
       orderId = int(item.get("values")[0])  
    except IndexError:
        return tk.messagebox.showerror(title="Error", message="Debes de seleccionar un cliente antes de remplazarlo para agregarlo a una orden de trabajo")
   
    #print(customerId) 
    sql = f"DELETE FROM ordenestrabajo WHERE IdOrden = {orderId}"
    query.execute(sql)
    conn.dbConnect().commit()
    tk.messagebox.showinfo(title="Operación realizada correctamente", message="Se ha eliminado la orden seleccionada satisfactoriamente")
    updateWindow()
    
def udpData(): #Agregar productos a la orden de trabajo
     record = detailTable.selection()[0]
     item = detailTable.item(record)
     idDetail = item.get("values")[4]
     
     description = descText.get()
     price = priceText.get()
     quantity = qtText.get()
     
     errorFlag = FALSE;  #Manejo errores de validación con bandera booleana
     
     if description == "":
        tk.messagebox.showerror(title="Error", message="No haz agregado una descripción. Para dar de alta una orden de trabajo es necesario agregar una descripción.")
        errorFlag = True;
    
     if price == "":
        tk.messagebox.showerror(title="Error", message="No haz agregado el precio. Para dar de alta una orden de trabajo es necesario agregar el precio de la descripción.")
        errorFlag = True;
     
     if quantity == "":
        tk.messagebox.showerror(title="Error", message="No haz agregado la cantidad precio. Para dar de alta una orden de trabajo es necesario agregar la cantidad relacionada con la descripción.")
        errorFlag = True;
      
     #Validación integridad de los datos
     if isNumber(price) is False:
        tk.messagebox.showerror(title="Error", message="El valor del precio debe ser un número")
        errorFlag = True;
        
     if not quantity.isdigit():
        tk.messagebox.showerror(title="Error", message="No haz agregado la cantidad precio. Para dar de alta una orden de trabajo es necesario agregar la cantidad relacionada con la descripción.")
        errorFlag = True;
        
     sql = "UPDATE detallesorden SET Cantidad = %s, Descripcion = %s, Importe = %s WHERE IdDetalleOrden = %s"
     values = (quantity, description, price, idDetail)
     query.execute(sql, values)
     conn.dbConnect().commit()
     tk.messagebox.showinfo(title="Operación realizada correctamente", message="Se ha editado el detalle de la orden seleccionada")
     reset();

def isNumber(n): #Validación caracteres numéricos
    pattern = r'^[0-9]+(\.[0-9]{2})*$'
    regex = re.compile(pattern)
    return bool(regex.search(n))

def saveOrder(): # Guardar orden de trabajo y redireccionar al apartado principal
    record = detailTable.selection()[0]
    item = detailTable.item(record)
    idDetail = item.get("values")[0]
    errorFlag = FALSE;
           
    #Sumar monto acumulado de las ordenes
    searchSql2 = f"SELECT SUM(Importe * Cantidad) FROM detallesorden WHERE IdOrden = {idDetail}"
    query.execute(searchSql2)
    q2 = query.fetchall()
    
    for i in q2:
            total = i[0]
                     
    if errorFlag == False:
       sql = "UPDATE ordenestrabajo SET Total = %s WHERE IdOrden = %s"
       values = (total, idDetail)
       query.execute(sql, values)
       conn.dbConnect().commit()
       reset()
       tk.messagebox.showinfo(title="Operación realizada correctamente", message="Se ha actualizado el monto total de la orden de compra correctamente")
       setMainWindow()
     
def reset(): #Reiniciar formulario
        descText.delete(0, END)
        priceText.delete(0, END)
        qtText.delete(0, END)
        
def do_popup(event):
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()
        
def do_popup2(event):
    try:
        m2.tk_popup(event.x_root, event.y_root)
    finally:
        m2.grab_release()
        
def showData(): #Mostrar reusltados generados
    sql = "SELECT ot.IdOrden, Concat(DATE_FORMAT(ot.FechaSolicitud, '%d-%m-%Y'), ' ', ot.HoraRegistro), Concat('$', ot.Total), c.Nombre FROM ordenestrabajo ot INNER JOIN clientes c ON c.IdCliente = ot.IdCliente ORDER BY ot.FechaSolicitud ASC;";
    
    query.execute(sql)
    q2 = query.fetchall()
    
    for row in q2:
         idOrden= row[0]
         fechaSolicitud = row[1]
         total = row[2]
         cliente = row[3]
         table.insert('', 'end', value = (idOrden, fechaSolicitud, total, cliente))


def createWindow():
    global window, table, searchText, customerDetailView, descText, priceText, qtText, cal, detailTable, m, m2
    #Inicia componentes
    window = tk.Tk()
    window.title("Administración de ordenes de trabajo")
    window.geometry("500x400")
    setWindow(window)
    
    #Componentes gráficos
    lbl1 = Label(window, text = "Administración de ordenes de servicio - Seleccione alguna orden de trabajo para editar, imprimir ordenes de trabajo en PDF, eliminar o ver el contenido de las ordenes") #Componente etiqueta de ventana principal que será vista en la parte principal
    lbl1.grid(row = 0, column = 0)
    lbl1.place(x=350, y=0)
    
    #Menús que se van a desplegar al dar click derecho sobre cualquier columna de la tabla de ordenes
    m = Menu(window, tearoff=0)
    m.add_command(label="Ver y editar detalle de la orden", command=showOrderDetail)
    m.add_command(label="Eliminar orden", command=deleteOrder)
    m.add_command(label="Ver orden en PDF")
    m.add_command(label="Actualizar información", command=updateWindow)
    
    #Menús que se van a desplegar al dar click derecho sobre cualquier columna de la tabla de detalle de orden 
    m2 = Menu(window, tearoff=0)
    m2.add_command(label="Editar producto", command=showOrderDetailUpd)
    m2.add_command(label="Eliminar producto", command=deleteProduct)
   
    searchLbl = Label(window, text = "Filtrar ordenes por nombre de cliente") #Componente etiqueta de ventana principal que será vista en la parte principal
    searchLbl.grid(row = 1, column = 2)
    searchLbl.place(x=350, y=100)
    searchText = tkinter.Entry(window)
    searchText.grid(row = 1, column = 2)
    searchText.place(x=580, y=100,  width = 200)
    
    searchLbl2 = Label(window, text = "Filtrar ordenes por fecha") #Componente etiqueta de ventana principal que será vista en la parte principal
    searchLbl2.grid(row = 1, column = 2)
    searchLbl2.place(x=800, y=100)
    
    cal = DateEntry(window, width=12, background="darkblue", foreground="white", borderwidth=2, locale='es')
    cal.grid(row = 1, column = 2)
    cal.place(x=950, y=100)  
    
    searchBtn = Button(window, text = "Buscar ordenes",  command = searchData, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    searchBtn.grid(row = 1, column = 2) 
    searchBtn.place(x=1100, y=100)

    addNewCustomerBtn = Button(window, text = "Registrar nueva orden",  command = OrdersView, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    addNewCustomerBtn.grid(row = 1, column = 2)
    addNewCustomerBtn.place(x=350, y=50)
    
    returnBtn = Button(window, text = "Regresar al menú principal",  command = setMainWindow, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    returnBtn.grid(row = 1, column = 2)
    returnBtn.place(x=550, y=50)
    
    #Tabla ordenes de trabajo registradas
    table = ttk.Treeview(window, columns=("c1", "c2", "c3", "c4"), show='headings', height=8)
    table.column("# 1", anchor=CENTER)
    table.heading("# 1", text="Id orden")
    table.column("# 2", anchor=CENTER)
    table.heading("# 2", text="Fecha/hora orden")
    table.column("# 3", anchor=CENTER)
    table.heading("# 3", text="Total")
    table.column("# 4", anchor=CENTER)
    table.heading("# 4", text="Nombre")
    table.grid(row = 2, column = 0)
    table.place(x=350, y=150)
    
    scroll_y = Scrollbar(window, orient="vertical", command=table.yview)
    scroll_y.grid(row=1, column=0, sticky="ns")
    table.configure(yscrollcommand=scroll_y.set)
    scroll_y.place(x=1150, y=150)
    
    table.bind("<Button-3>", do_popup)
    
    selectCustBtn = Button(window, text = "Ver y editar detalle orden",  command = showOrderDetail, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    selectCustBtn.grid(row = 2, column = 0) 
    selectCustBtn.place(x=1250, y=150)
    
    replaceBtn = Button(window, text = "Eliminar orden",  command = deleteOrder, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    replaceBtn.grid(row = 2, column = 0) 
    replaceBtn.place(x=1250, y=200)
    
    lbl = Label(window, text = "Ver detalle de la orden") #Componente etiqueta de ventana principal que será vista en la parte principal
    lbl.grid(row = 1, column = 2)
    lbl.place(x=200, y=370)
    
    pdfBtn = Button(window, text = "Ver orden PDF",  command = getPDF, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    pdfBtn.grid(row = 2, column = 0) 
    pdfBtn.place(x=1250, y=250)
    
    updBtn = Button(window, text = "Actualizar búsqueda",  command = updateWindow, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    updBtn.grid(row = 2, column = 0) 
    updBtn.place(x=1250, y=300)
    
    #Tabla detalle de ordenes de trabajo
    detailTable = ttk.Treeview(window, columns=("c1", "c2", "c3", "c4", "c5"), show='headings', height=8)
    detailTable.column("# 1", anchor=CENTER)
    detailTable.heading("# 1", text="Id orden")
    detailTable.column("# 2", anchor=CENTER)
    detailTable.heading("# 2", text="Cantidad")
    detailTable.column("# 3", anchor=CENTER)
    detailTable.heading("# 3", text="Descripción")
    detailTable.column("# 4", anchor=CENTER)
    detailTable.heading("# 4", text="Importe")
    detailTable.column("# 5", anchor=CENTER)
    detailTable.heading("# 5", text="Id descripción")
    detailTable.grid(row = 2, column = 0)
    detailTable.place(x=200, y=400)
    
    detailTable.bind("<Button-3>", do_popup2)
    
    scroll_y = Scrollbar(window, orient="vertical", command=detailTable.yview)
    scroll_y.grid(row=1, column=0, sticky="ns")
    detailTable.configure(yscrollcommand=scroll_y.set)
    scroll_y.place(x=1200, y=400)
    
    updProductDataBtn = Button(window, text = "Editar producto",  command = showOrderDetailUpd, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    updProductDataBtn.grid(row = 2, column = 0) 
    updProductDataBtn.place(x=1250, y=400)
    
    deleteProductBtn = Button(window, text = "Eliminar producto",  command = deleteProduct, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    deleteProductBtn.grid(row = 2, column = 0) 
    deleteProductBtn.place(x=1250, y=450)
 
    customerDetailView = Label(window) #Componente etiqueta de ventana principal que será vista en la parte principal
    customerDetailView.grid(row = 1, column = 2)
    customerDetailView.place(x=350, y=350)
    
    lblQt = Label(window, text = "Cantidad") #Componente etiqueta de ventana principal que será vista en la parte principal
    lblQt.grid(row = 2, column = 0)
    lblQt.place(x=350, y=650)
    
    qtText = tkinter.Entry(window)
    qtText.grid(row = 2, column = 0)
    qtText.place(x=350, y=700,  width = 100)
    
    lblDescrp = Label(window, text = "Descripción") #Componente etiqueta de ventana principal que será vista en la parte principal
    lblDescrp.grid(row = 2, column = 0)
    lblDescrp.place(x=550, y=650)
    
    descText = tkinter.Entry(window)
    descText.grid(row = 2, column = 0)
    descText.place(x=550, y=700,  width = 350)
    
    lblPrice = Label(window, text = "Importe") #Componente etiqueta de ventana principal que será vista en la parte principal
    lblPrice.grid(row = 2, column = 0)
    lblPrice.place(x=950, y=650)
    
    priceText = tkinter.Entry(window)
    priceText.grid(row = 2, column = 0)
    priceText.place(x=950, y=700,  width = 200)
    
    addProductBtn = Button(window, text = "Guardar",  command = udpData, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    addProductBtn.grid(row = 2, column = 0) 
    addProductBtn.place(x=1250, y=700)
    
    saveOrderBtn = Button(window, text = "Completar orden editada",  command = saveOrder, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    saveOrderBtn.grid(row = 2, column = 0) 
    saveOrderBtn.place(x=350, y=750)
    
    window.mainloop()
