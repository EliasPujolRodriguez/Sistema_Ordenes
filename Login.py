from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox
from tkinter import * 
from tkinter import filedialog
import os
from datetime import date
from Connection import Connection
import MainView

#Instancia de clase conexión
conn = Connection("root", "localhost", "", "muebles", "3306")
query = conn.dbConnect().cursor()

def setWindow(window):
     width = window.winfo_screenwidth()
     height = window.winfo_screenheight()
     x = (width - window.winfo_reqwidth()) // 2
     y = (height - window.winfo_reqheight()) // 2
     window.geometry(f"+{x}+{y}")
     
def storeData(): #Guardar información en la base de datos
     password_value = password_entry.get()
     username_value = username_entry.get()
    #Consulta que sirve para determinar los datos totales de los usuarios registrados relacionados con la empresa que va a servir para determinar que interfaz se verá
     searchSql2 = "SELECT Usuario, Contraseña, ClaveKey FROM usuarios;"
     query.execute(searchSql2)
     q2 = query.fetchall()
     
     for row in q2:
         usr = row[0]
         pswQuery = row[1]
         key = row[2] #Se va a obtener la llave apartir de los resultados dados desde la base de datos
     
     refKey = Fernet(key)
     psw = refKey.decrypt(pswQuery)
     paswAuth = psw.decode('utf-8')
     
     #Validación de los datos
     if password_value == '':
        tk.messagebox.showerror(title="Error", message="La contraseña no debe ir vacía")
     
     if username_value == '':
        tk.messagebox.showerror(title="Error", message="El nombre de usuario no debe ir vacío")
      
     if paswAuth != password_value:
        tk.messagebox.showerror(title="Error", message="La contraseña ingresada no es correcta. Intente con otra")
     
     if usr != username_value:
        tk.messagebox.showerror(title="Error", message="El usuario ingresado no es correcto. Intente con otro")
     
     if paswAuth == password_value and username_value == usr:
        tk.messagebox.showinfo(title="Operación realizada correctamente", message="Inicio de sesión correcto")
        window.withdraw()
        MainView.createWindow()

def createWindow():
    global window, password_entry, username_entry
    #Inicia componentes
    window = tk.Tk()
    window.title("Login - Inicio de sesión usuario")
    window.geometry("500x400")
    setWindow(window)
    #Componentes gráficos formulario subida información
    Label(window, text = 'Inicie sesión con sus datos para acceder al sistema').pack(side = TOP, pady = 10) 
    
    Label(window, text = 'Nombre de usuario').pack(side = TOP, pady = 15) 
    username_entry = tk.Entry(window, font=('calibre',10,'normal'))
    username_entry.pack(side = TOP, pady = 18) 
    
    Label(window, text = 'Contraseña').pack(side = TOP, pady = 20) 
    password_entry = tk.Entry(window, show="*")  # Show asterisks for password
    password_entry.pack(side = TOP, pady = 25) 
    
    save_button = tk.Button(window, text="Guardar datos", command=storeData)
    save_button.pack(side = TOP, pady = 26) 
    
    window.resizable(0, 0) 
    #upload_button.pack(pady=20)
    window.mainloop()
      