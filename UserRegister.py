from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox
from tkinter import * 
from tkinter import filedialog
from pathlib import Path
import os
from PIL import Image
from datetime import date
from Connection import Connection
import MainView as MainView

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
     key = Fernet.generate_key()
     refKey = Fernet(key)
     password_value = password_entry.get().encode()
     username_value = username_entry.get()
     encryptedPWD = refKey.encrypt(password_value)
     currentDay = date.today()
     errorFlag = FALSE; #Manejo errores de validación con bandera booleana
     
     #Validaciones de los datos del formulario
     if len(username_value) > 35:
          tk.messagebox.showerror(title="Error", message="El nombre de usuario no debe superar los 35 caracteres")
          errorFlag = True;
     
     if password_value == "":
          tk.messagebox.showerror(title="Error", message="La contraseña no debe de estar vacía")
          errorFlag = True;
     
     if username_value == "":
          tk.messagebox.showerror(title="Error", message="El usuario no debe de estar vacío")
          errorFlag = True;
     
     if errorFlag == False:
           sql = "INSERT INTO usuarios (Usuario, Contraseña, RegistradoEn, ClaveKey) values(%s,%s,%s,%s)"
           values = (username_value, encryptedPWD, currentDay, key)
           query.execute(sql, values)
           conn.dbConnect().commit()
           tk.messagebox.showinfo(title="Operación realizada correctamente", message="Se ha registrado el usuario")
           window.withdraw()
           MainView.createWindow()
     
def createWindow():
    global window, password_entry, username_entry
    #Inicia componentes
    window = tk.Tk()
    window.title("Registro de usuario")
    window.geometry("500x400")
    setWindow(window)
    #Componentes gráficos formulario subida información
    Label(window, text = 'Registro de datos del usuario').pack(side = TOP, pady = 10) 
    Label(window, text = 'Los campos asignados con un asterisco son obligatorios (*)').pack(side = TOP, pady = 15) 
    
    Label(window, text = 'Nombre de usuario (*)').pack(side = TOP, pady = 15) 
    username_entry = tk.Entry(window, font=('calibre',10,'normal'))
    username_entry.pack(side = TOP, pady = 18) 
    
    Label(window, text = 'Contraseña (*)').pack(side = TOP, pady = 20) 
    password_entry = tk.Entry(window, show="*")  # Show asterisks for password
    password_entry.pack(side = TOP, pady = 25) 
    
    save_button = tk.Button(window, text="Guardar datos", command=storeData)
    save_button.pack(side = TOP, pady = 26) 
    
    window.resizable(0, 0) 
    #upload_button.pack(pady=20)
    window.mainloop()
      