from Connection import Connection
import tkinter as tk
from tkinter import messagebox
from tkinter import * 
from tkinter import filedialog
import MainView
from cryptography.fernet import Fernet

#Instancia de clase conexión
conn = Connection("root", "localhost", "", "muebles", "3306")
query = conn.dbConnect().cursor()

def setWindow(window):
     width = window.winfo_screenwidth()
     height = window.winfo_screenheight()
     x = (width - window.winfo_reqwidth()) // 2
     y = (height - window.winfo_reqheight()) // 2
     window.geometry(f"+{x}+{y}")
     
def storeData():
    password_value = password_entry.get()
    username_value = username_entry.get()
    
    key = Fernet.generate_key()
    refKey = Fernet(key)
    password_value = password_entry.get().encode()
    username_value = username_entry.get()
    encryptedPWD = refKey.encrypt(password_value)

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
        sql = "UPDATE usuarios SET Usuario = %s, Contraseña = %s, ClaveKey = %s"
        values = (username_value, encryptedPWD, key)
        query.execute(sql, values)
        conn.dbConnect().commit()
        tk.messagebox.showinfo(title="Operación realizada correctamente", message="Se ha actualizado la información del usuario")
    
def setMainWindow():
     window.withdraw()
     MainView.createWindow()

def createWindow():
    global window, password_entry, username_entry
    #Inicia componentes
    window = tk.Tk()
    window.title("Configuración de datos del usuario - Actualizar datos usuario")
    window.geometry("500x400")
    setWindow(window)
    #Componentes gráficos formulario subida información
    Label(window, text = 'Los campo marcados con asterísco son obligatorios').pack(side = TOP, pady = 10) 
    
    #Consulta a base de datos con base a lo registrado
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
    
    Label(window, text = 'Nombre de usuario (*)').pack(side = TOP, pady = 15) 
    username_entry = tk.Entry(window, font=('calibre',10,'normal'))
    username_entry.pack(side = TOP, pady = 18) 
    username_entry.insert(0,usr)
    
    Label(window, text = 'Contraseña (*)').pack(side = TOP, pady = 20) 
    password_entry = tk.Entry(window, font=('calibre',10,'normal')) 
    password_entry.pack(side = TOP, pady = 21) 
    password_entry.insert(0,paswAuth)
    
    save_button = tk.Button(window, text="Guardar datos", command=storeData)
    save_button.pack(side = TOP, pady = 22) 
    
    back_button = tk.Button(window, text="Regresar menú principal", command=setMainWindow)
    back_button.pack(side = TOP, pady = 23) 

    
    window.resizable(0, 0) 
    window.mainloop()