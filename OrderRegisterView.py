import tkinter as tk
from tkinter import ttk
import tkinter
from Connection import Connection
from tkinter import messagebox
from tkinter import * 
from tkinter import filedialog
import datetime
import MainView as MainView, CustomerView as CustomerView, OrderRegisterView as OrderRegisterView, OrderCRUD as OrderCRUD
import re
#Instancia de clase conexión
conn = Connection("root", "localhost", "", "muebles", "3306")
query = conn.dbConnect().cursor()

def setMainWindow():
    window.withdraw()
    MainView.createWindow()
    
def setWindow(window):
    window.update()
    w, h = window.maxsize()
    window.wm_overrideredirect(True)
    window.geometry(f'{w}x{h}+0+0')  

def customersView():
     window.withdraw()
     CustomerView.createWindow();    
     
def setOrderCRUDWindow():
     window.withdraw()
     OrderCRUD.createWindow()  
     
def searchData():
    searchName = searchText.get()
    
    sql = f"SELECT IdCliente, Nombre, Telefono, RegistradoEn FROM clientes WHERE Nombre LIKE '%{searchName}%' ORDER BY Nombre ASC;";
    query.execute(sql)
    q2 = query.fetchall()
     
    for records in table.get_children():
        table.delete(records)
    
    for data in q2:
        table.insert('', 'end', value = (data[0], data[1], data[2], data[3]))    

def selectCustomerOrder():
     currentDay = datetime.datetime.now()
     
     date = currentDay.strftime("%Y-%m-%d")
     curTime = currentDay.strftime("%H:%M:%S")
     
     try:
        record = table.selection()[0]
        item = table.item(record)
        customerId = item.get("values")[0]
        name = item.get("values")[1]
     except IndexError:
        return tk.messagebox.showerror(title="Error", message="Debes de seleccionar un cliente antes de asignar una orden de trabajo")
     
     sql = "INSERT INTO ordenestrabajo (FechaSolicitud, Total, IdCliente, HoraRegistro) values(%s,%s,%s,%s)"
     values = (date, 0, customerId, curTime )
     query.execute(sql, values)
     conn.dbConnect().commit()
     tk.messagebox.showinfo(title="Operación realizada correctamente", message="Se ha asociado al cliente seleccionado con la orden de compra correctamente")
     conn.dbConnect().cursor().close()
     customerDetailView.config(text=f"Orden de trabajo asignada a {name}")
     
def replaceCustomerOrder():
    try:
       record = table.selection()[0]
       item = table.item(record)
       customerId = int(item.get("values")[0])  
    except IndexError:
        return tk.messagebox.showerror(title="Error", message="Debes de seleccionar un cliente antes de remplazarlo para agregarlo a una orden de trabajo")
    
    #Consulta referente a las ordenes para ver cual fue la última que se agregó
    searchSql = "SELECT IdOrden FROM ordenestrabajo ORDER BY IdOrden DESC LIMIT 1;"
    query.execute(searchSql)
    q = query.fetchall()

    for i in q:
            orderId = i[0]
    
    name = item.get("values")[1]
    #print(customerId) 
    sql = "UPDATE ordenestrabajo SET IdCliente = %s WHERE IdOrden = %s"
    values = (customerId, orderId)
    query.execute(sql, values)
    conn.dbConnect().commit()
    tk.messagebox.showinfo(title="Operación realizada correctamente", message="Se ha modifcado al cliente seleccionado de la orden de compra correctamente")
    customerDetailView.config(text=f"Orden de trabajo asignada a {name}")
    conn.dbConnect().cursor().close()

def isNumber(n): #Validación caracteres numéricos
    pattern = r'^[0-9]+(\.[0-9]{2})*$'
    regex = re.compile(pattern)
    return bool(regex.search(n))

def saveOrder(): # Guardar orden de trabajo y redireccionar al apartado principal
    name = customerDetailView.cget("text")
    errorFlag = FALSE;
    #Consulta referente a las ordenes para ver cual fue la última que se agregó
    searchSql = "SELECT IdOrden FROM ordenestrabajo ORDER BY IdOrden DESC LIMIT 1;"
    query.execute(searchSql)
    q = query.fetchall()

    for i in q:
            orderId = i[0]
            
    #Sumar monto acumulado de las ordenes
    searchSql2 = f"SELECT SUM(Importe * Cantidad) FROM detallesorden WHERE IdOrden = {orderId}"
    query.execute(searchSql2)
    q2 = query.fetchall()
    
    for i in q2:
            total = i[0]
                     
    if name == "":
        tk.messagebox.showerror(title="Error", message="No se ha seleccionado a un cliente. Para asignar una orden de trabajo se debe de seleccionar algún cliente")
        errorFlag = True
    
    if errorFlag == False:
       sql = "UPDATE ordenestrabajo SET Total = %s WHERE IdOrden = %s"
       values = (total, orderId)
       query.execute(sql, values)
       conn.dbConnect().commit()
       conn.dbConnect().cursor().close()
       reset()
       tk.messagebox.showinfo(title="Operación realizada correctamente", message="Se ha actualizado el monto total de la orden de compra correctamente")
       setMainWindow()
       
def addProduct(): #Agregar productos a la orden de trabajo
     searchSql2 = "SELECT IdOrden FROM ordenestrabajo ORDER BY IdOrden DESC LIMIT 1;"
     query.execute(searchSql2)
     q2 = query.fetchall()
     name = customerDetailView.cget("text")
     description = descText.get()
     price = priceText.get()
     quantity = qtText.get()
     
     errorFlag = FALSE;  #Manejo errores de validación con bandera booleana
     
     for row in q2:
         orderId = row[0]
    
     if name == "":
        tk.messagebox.showerror(title="Error", message="No se ha seleccionado a un cliente. Para asignar una ordeb de trabajo se debe de seleccionar algún cliente")
        errorFlag = True;
     
     if description == "":
        tk.messagebox.showerror(title="Error", message="No haz agregado una descripción. Para dar de alta una orden de trabajo es necesario agregar una descripción.")
        errorFlag = True;
     
     if len(description) > 200:
        tk.messagebox.showerror(title="Error", message="La descripción del producto NO debe constar de más de 200 caracteres")
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
        
     sql = "INSERT INTO detallesorden (IdOrden, Cantidad, Descripcion, Importe) values(%s,%s,%s,%s)"
     values = (orderId, quantity, description, price)
     query.execute(sql, values)
     conn.dbConnect().commit()
     tk.messagebox.showinfo(title="Operación realizada correctamente", message="Se ha agregado el producto a la orden de trabajo")
     reset();
     conn.dbConnect().cursor().close()
     
def reset(): #Reiniciar formulario
        descText.delete(0, END)
        priceText.delete(0, END)
        qtText.delete(0, END)

def do_popup(evt):
      try:
        m.tk_popup(evt.x_root, evt.y_root)
      finally:
        m.grab_release()
        
def updateWindow(): #Buscar desde cero 
    sql = ''
    searchText.delete(0, END)
    searchName = searchText.get()
    
    if searchName == '':
       sql =f"SELECT IdCliente, Nombre, Telefono, DATE_FORMAT(RegistradoEn, '%d-%m-%Y') FROM clientes ORDER BY Nombre ASC" 
    
    query.execute(sql)
    q2 = query.fetchall()
     
    for records in table.get_children():
        table.delete(records)
    
    for data in q2:
        table.insert('', 'end', value = (data[0], data[1], data[2], data[3])) 

def createWindow():
    global window, table, searchText, customerDetailView, descText, priceText, qtText, m
    #Inicia componentes
    window = tk.Tk()
    window.title("Registro de ordenes de trabajo")
    setWindow(window)
    
    #Componentes gráficos
    lbl1 = Label(window, text = "Crear orden de trabajo - Seleccione o ingrese un nuevo cliente para registrar una orden de trabajo") #Componente etiqueta de ventana principal que será vista en la parte principal
    lbl1.grid(row = 0, column = 0)
    lbl1.place(x=350, y=0)
    
    searchLbl = Label(window, text = "Buscar por nombre de cliente") #Componente etiqueta de ventana principal que será vista en la parte principal
    searchLbl.grid(row = 1, column = 2)
    searchLbl.place(x=350, y=100)
    searchText = tkinter.Entry(window)
    searchText.grid(row = 1, column = 2)
    searchText.place(x=550, y=100,  width = 200)
    
    searchBtn = Button(window, text = "Buscar clientes",  command = searchData, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    searchBtn.grid(row = 1, column = 2) 
    searchBtn.place(x=800, y=100)

    addNewCustomerBtn = Button(window, text = "Registrar nuevo cliente",  command = customersView, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    addNewCustomerBtn.grid(row = 1, column = 2)
    addNewCustomerBtn.place(x=350, y=50)
    
    returnBtn = Button(window, text = "Regresar al menú principal",  command = setMainWindow, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    returnBtn.grid(row = 1, column = 2)
    returnBtn.place(x=550, y=50)
    
    viewOrders = Button(window, text = "Administrar ordenes de trabajo",  command = setOrderCRUDWindow, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    viewOrders.grid(row = 1, column = 2)
    viewOrders.place(x=800, y=50)
    
    #Menús que se van a desplegar al dar click derecho sobre cualquier columna de la tabla de ordenes
    m = Menu(window, tearoff=0)
    m.add_command(label="Asignar compra", command=selectCustomerOrder)
    m.add_command(label="Remplazar cliente", command=replaceCustomerOrder)
    
    table = ttk.Treeview(window, columns=("c1", "c2", "c3", "c4"), show='headings', height=8)
    table.column("# 1", anchor=CENTER)
    table.heading("# 1", text="Id cliente")
    table.column("# 2", anchor=CENTER)
    table.heading("# 2", text="Nombre cliente")
    table.column("# 3", anchor=CENTER)
    table.heading("# 3", text="Teléfono")
    table.column("# 4", anchor=CENTER)
    table.heading("# 4", text="Fecha de registro")
    table.grid(row = 2, column = 0)
    table.place(x=350, y=150)
    
    table.bind("<Button-3>", do_popup)
    
    scroll_y = Scrollbar(window, orient="vertical", command=table.yview)
    scroll_y.grid(row=1, column=0, sticky="ns")
    table.configure(yscrollcommand=scroll_y.set)
    scroll_y.place(x=1150, y=150)
    
    selectCustBtn = Button(window, text = "Asignar compra",  command = selectCustomerOrder, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    selectCustBtn.grid(row = 2, column = 0) 
    selectCustBtn.place(x=1250, y=150)
    
    replaceBtn = Button(window, text = "Remplazar cliente",  command = replaceCustomerOrder, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    replaceBtn.grid(row = 2, column = 0) 
    replaceBtn.place(x=1250, y=200)
    
    updDataBtn = Button(window, text = "Actualizar datos",  command = updateWindow, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    updDataBtn.grid(row = 2, column = 0) 
    updDataBtn.place(x=1250, y=250)
    
    customerDetailView = Label(window) #Componente etiqueta de ventana principal que será vista en la parte principal
    customerDetailView.grid(row = 1, column = 2)
    customerDetailView.place(x=350, y=350)
    
    lbl = Label(window, text = "Agregar productos a la orden de trabajo - Detalle de orden") #Componente etiqueta de ventana principal que será vista en la parte principal
    lbl.grid(row = 0, column = 0)
    lbl.place(x=350, y=380)
    
    lblQt = Label(window, text = "Cantidad") #Componente etiqueta de ventana principal que será vista en la parte principal
    lblQt.grid(row = 2, column = 0)
    lblQt.place(x=350, y=400)
    
    qtText = tkinter.Entry(window)
    qtText.grid(row = 2, column = 0)
    qtText.place(x=350, y=450,  width = 100)
    
    lblDescrp = Label(window, text = "Descripción") #Componente etiqueta de ventana principal que será vista en la parte principal
    lblDescrp.grid(row = 2, column = 0)
    lblDescrp.place(x=550, y=400)
    
    descText = tkinter.Entry(window)
    descText.grid(row = 2, column = 0)
    descText.place(x=550, y=450,  width = 350)
    
    lblPrice = Label(window, text = "Importe") #Componente etiqueta de ventana principal que será vista en la parte principal
    lblPrice.grid(row = 2, column = 0)
    lblPrice.place(x=950, y=400)
    
    priceText = tkinter.Entry(window)
    priceText.grid(row = 2, column = 0)
    priceText.place(x=950, y=450,  width = 200)
    
    addProductBtn = Button(window, text = "Agregar a la orden",  command = addProduct, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    addProductBtn.grid(row = 2, column = 0) 
    addProductBtn.place(x=1250, y=450)
    
    saveOrderBtn = Button(window, text = "Completar orden",  command = saveOrder, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    saveOrderBtn.grid(row = 2, column = 0) 
    saveOrderBtn.place(x=350, y=550)

    #Consultar clientes
    sql = "SELECT IdCliente, Nombre, Telefono, DATE_FORMAT(RegistradoEn, '%d-%m-%Y') FROM clientes ORDER BY Nombre ASC";
    query.execute(sql)
    q2 = query.fetchall()
     
    for row in q2:
         idCliente = row[0]
         nombre = row[1]
         phone = row[2]
         fechaRegistro = row[3] 
         table.insert('', 'end', value = (idCliente, nombre, phone, fechaRegistro))
    
         
    window.mainloop()
