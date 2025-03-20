import tkinter as tk
from tkinter import ttk
import tkinter
from Connection import Connection
from tkinter import messagebox
from tkinter import * 
from tkinter import filedialog
import datetime
import MainView as MainView, CustomerView as CustomerView, OrderRegisterView as OrderRegisterView
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
     
def searchData():
    searchName = searchText.get()
    
    sql = f"SELECT IdCliente, Nombre, Telefono, RegistradoEn FROM clientes WHERE Nombre LIKE '%{searchName}%' ORDER BY Nombre ASC;";
    query.execute(sql)
    q2 = query.fetchall()
     
    for records in table.get_children():
        table.delete(records)
    
    for data in q2:
        table.insert('', 'end', value = (data[0], data[1], data[2], data[3]))    

def updateCustomerData():
     try:
        record = table.selection()[0]
        item = table.item(record)
        customerId = item.get("values")[0]
        
        sql = f"SELECT Nombre, Telefono FROM clientes WHERE IdCliente = {customerId}";
        query.execute(sql)
        row = query.fetchall()
     
        for data in row:
            custName = data[0] 
            custPhName = data[1] 
        
        phNumberText.insert(0, custPhName)
        csNameInput.insert(0, custName)
        
     except IndexError:
        return tk.messagebox.showerror(title="Error", message="Debes de seleccionar un cliente antes de editar sus datos")

def isNumber(n): #Validación caracteres numéricos
    pattern = r'^[0-9]{10}$'
    regex = re.compile(pattern)
    return bool(regex.search(n))
 
def updateWindow(): #Buscar desde cero 
    sql = ''
    searchText.delete(0, END)
    searchName = searchText.get()
    
    if searchName == '':
       sql =f"SELECT IdCliente, Nombre, Telefono, DATE_FORMAT(RegistradoEn, '%d-%m-%Y') FROM clientes ORDER BY Nombre ASC;" 
    
    query.execute(sql)
    q2 = query.fetchall()
     
    for records in table.get_children():
        table.delete(records)
    
    for data in q2:
        table.insert('', 'end', value = (data[0], data[1], data[2], data[3])) 

def udpData(): #Agregar productos a la orden de trabajo
     record = table.selection()[0]
     item = table.item(record)
     customerId = item.get("values")[0]
     phone = phNumberText.get()
     name = csNameInput.get()
     errorFlag = FALSE;
     
      #Validaciones de campos
     if name == "":
       tk.messagebox.showerror(title="Error", message="El nombre del cliente no debe de estar vacío")
       errorFlag = True;
       
     if phone == "":
       tk.messagebox.showerror(title="Error", message="El número de teléfono del cliente no debe de estar vacío")
       errorFlag = True;
       
     #Validación longitud caracteres
     if name != "" and len(name) > 75:
        tk.messagebox.showerror(title="Error", message="El nombre del cliente no debe superar los 75 caracteres")
        errorFlag = True;

     if phone != "" and len(phone) > 10:
        tk.messagebox.showerror(title="Error", message="El número de teléfono del cliente no debe superar los 10 caracteres")
        errorFlag = True;
        
     if isNumber(phone) is False:
        tk.messagebox.showerror(title="Error", message="El valor del teléfono debe ser un número de 10 digítos")
        errorFlag = True;
        
     if errorFlag == FALSE:
        sql = "UPDATE clientes SET Nombre = %s, Telefono = %s WHERE IdCliente = %s"
        values = (name, phone, customerId)
        query.execute(sql, values)
        conn.dbConnect().commit()
        reset()
        tk.messagebox.showinfo(title="Operación realizada correctamente", message="Se ha actualizado la información del cliente correctamente")
        conn.dbConnect().cursor().close()
        
def reset(): #Reiniciar formulario
        phNumberText.delete(0, END)
        csNameInput.delete(0, END)
        
def do_popup(event): #Lanzar método de menús al dar click derecho
    try:
        m.tk_popup(event.x_root, event.y_root)
    finally:
        m.grab_release()
        
def deleteCustomer(): #Eliminar cliente seleccionado
     try:
        record = table.selection()[0]
        item = table.item(record)
        customerId = item.get("values")[0]
        customerName = item.get("values")[1]
        
        sql = "DELETE FROM clientes WHERE IdCliente = %s AND Nombre = %s"
        values = (customerId, customerName)
        query.execute(sql, values)
        conn.dbConnect().commit()
        tk.messagebox.showinfo(title="Operación realizada correctamente", message="Se ha eliminado al cliente seleccionado")
        updateWindow()
     except IndexError:
        return tk.messagebox.showerror(title="Error", message="Debes de seleccionar un cliente antes de editar sus datos")

def createWindow():
    global window, table, searchText, customerDetailView, phNumberText, csNameInput, m
    #Inicia componentes
    window = tk.Tk()
    window.title("Administración clientes")
    setWindow(window)
    
    #Componentes gráficos
    lbl1 = Label(window, text = "Administración de clientes registrados") #Componente etiqueta de ventana principal que será vista en la parte principal
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
    
     #Menús que se van a desplegar al dar click derecho sobre cualquier columna de la tabla de ordenes
    m = Menu(window, tearoff=0)
    m.add_command(label="Editar cliente", command=updateCustomerData)
    m.add_command(label="Eliminar cliente", command=deleteCustomer)
    
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
    
    selectCustBtn = Button(window, text = "Editar",  command = updateCustomerData, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    selectCustBtn.grid(row = 2, column = 0) 
    selectCustBtn.place(x=1250, y=150)
    
    replaceBtn = Button(window, text = "Eliminar",  command = deleteCustomer, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    replaceBtn.grid(row = 2, column = 0) 
    replaceBtn.place(x=1250, y=200)
    
    updBtn = Button(window, text = "Actualizar búsqueda",  command = updateWindow, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    updBtn.grid(row = 2, column = 0) 
    updBtn.place(x=1250, y=250)
    
    customerDetailView = Label(window) #Componente etiqueta de ventana principal que será vista en la parte principal
    customerDetailView.grid(row = 1, column = 2)
    customerDetailView.place(x=350, y=350)
    
    lblQt = Label(window, text = "Nombre completo del cliente") #Componente etiqueta de ventana principal que será vista en la parte principal
    lblQt.grid(row = 2, column = 0)
    lblQt.place(x=350, y=400)
    
    csNameInput = tkinter.Entry(window)
    csNameInput.grid(row = 2, column = 0)
    csNameInput.place(x=350, y=450,  width = 250)
    
    lblDescrp = Label(window, text = "Teléfono") #Componente etiqueta de ventana principal que será vista en la parte principal
    lblDescrp.grid(row = 2, column = 0)
    lblDescrp.place(x=750, y=400)
    
    phNumberText = tkinter.Entry(window)
    phNumberText.grid(row = 2, column = 0)
    phNumberText.place(x=750, y=450)
    
    addProductBtn = Button(window, text = "Guardar",  command = udpData, height = 2, width=23, compound = RIGHT) #Creación componente botones principales referentes a las categorías que serán mostradas en la aplicación
    addProductBtn.grid(row = 2, column = 0) 
    addProductBtn.place(x=1250, y=450)

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
