from Connection import Connection
import tkinter as tk
from tkinter import messagebox
from tkinter import * 
from tkinter import filedialog
from datetime import date
import MainView
import re
#Instancia de clase conexión
conn = Connection("root", "localhost", "", "muebles", "3306")
query = conn.dbConnect().cursor()

def isNumber(n): #Validación caracteres numéricos
    pattern = r'^[0-9]{10}$'
    regex = re.compile(pattern)
    return bool(regex.search(n))

def storeData():
    custNameValue = customer_name_entry.get()
    custPhNumberValue = customer_ph.get()
    currentDay = date.today()
    errorFlag = FALSE; #Manejo errores de validación con bandera booleana
    
    #Validaciones de campos
    if custNameValue == "":
       tk.messagebox.showerror(title="Error", message="El nombre del cliente no debe de estar vacío")
       errorFlag = True;
       
    if custPhNumberValue == "":
       tk.messagebox.showerror(title="Error", message="El número de teléfono del cliente no debe de estar vacío")
       errorFlag = True;
       
     #Validación longitud caracteres
    if custNameValue != "" and len(custNameValue) > 75:
        tk.messagebox.showerror(title="Error", message="El nombre del cliente no debe superar los 75 caracteres")
        errorFlag = True;

    if custPhNumberValue != "" and len(custPhNumberValue) > 10:
        tk.messagebox.showerror(title="Error", message="El número de teléfono del cliente no debe superar los 10 caracteres")
        errorFlag = True;
    
     #Validación integridad de los datos
    if isNumber(custPhNumberValue) is False:
        tk.messagebox.showerror(title="Error", message="El valor del teléfono debe ser un número de 10 digítos")
        errorFlag = True;
    
    if errorFlag != True:
        sql = "INSERT INTO clientes (Nombre, Telefono, RegistradoEn) values(%s,%s,%s)"
        values = (custNameValue, custPhNumberValue, currentDay )
        query.execute(sql, values)
        conn.dbConnect().commit()
        tk.messagebox.showinfo(title="Operación realizada correctamente", message="Se ha registrado al cliente correctamente")
        reset()
        conn.dbConnect().cursor().close()
        
def setMainWindow():
    window.withdraw()
    MainView.createWindow()
    
def reset():
    customer_name_entry.delete(0, END)
    customer_ph.delete(0, END)

def setWindow(window):
    window.update()
    w, h = window.maxsize()
    window.wm_overrideredirect(True)
    window.geometry(f'{w}x{h}+0+0')  
     
def createWindow():
    global window, customer_name_entry, customer_ph
    #Inicia componentes
    window = tk.Tk()
    window.title("Registro de clientes")
    window.geometry("500x400")
    setWindow(window)

    #Componentes gráficos formulario subida información
    Label(window, text = 'Registro de clientes relacionados a las ordenes de trabajo. ').pack(side = TOP, pady = 10) 
    Label(window, text = 'Los campos asignados con un asterisco son obligatorios (*)').pack(side = TOP, pady = 15) 
    Label(window, text = 'Nombre completo del cliente (*)').place(x=125, y=100)
    
    customer_name_entry = tk.Entry(window, font=('calibre',10,'normal'))
    customer_name_entry.place(x=125, y=130, width = 200)

    customer_ph = tk.Entry(window, font=('calibre',10,'normal'))
    customer_ph.place(x=400, y=130, width = 100)
    Label(window, text = 'Teléfono (*)').place(x=400, y=100)
    
    save_button = tk.Button(window, text="Guardar datos", command=storeData)
    save_button.place(x=125, y=200)

    cancel_button = tk.Button(window, text="Limpiar", command=reset)
    cancel_button.place(x=225, y=200)
    
    back_button = tk.Button(window, text="Regresar menú principal", command=setMainWindow)
    back_button.place(x=325, y=200)
    
    window.resizable(0, 0) 

    window.mainloop()
