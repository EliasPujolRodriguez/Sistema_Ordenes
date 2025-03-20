import tkinter as tk
from tkinter import messagebox
from tkinter import * 
from tkinter import filedialog
from pathlib import Path
import os
from PIL import Image
from Connection import Connection
import UserRegister as UserRegister

#Instancia de clase conexión
conn = Connection("root", "localhost", "", "muebles", "3306")
query = conn.dbConnect().cursor()

def setWindow(window):
    window.update()
    w, h = window.maxsize()
    window.wm_overrideredirect(True)
    window.geometry(f'{w}x{h}+0+0')  

def counter():
    #Se va a evaluar si ya hay registros de empresa
            searchSql = "SELECT COUNT(IdEmpresa) FROM datosempresa"
            query.execute(searchSql)
            q = query.fetchall()
            
            for i in q:
                counter = i[0]
            return counter

def uploadFiles(): #Método que va a permitir subir un determinado archivo
    path = filedialog.askopenfile()
    coun = counter()
    if path:
            if coun == 0:
                 file = Path(str(path.name)).name
                 url = str(path.name)
                 extension = str(url.split(".")[-1]);
                 if extension == "jpg" or extension == "png": #Validar extensión de los archivos
                            folderPath = '..\\Sistema python\\Resources\Logo\\' + file
                            img = Image.open(url)
                            img.save(folderPath)
                            #Subir foto a la base de datos
                            sql = "INSERT INTO datosempresa (LogoEmpresa, DireccionTaller) values(%s,%s)"
                            values = (file, '')
                            query.execute(sql, values)
                            conn.dbConnect().commit()
                            tk.messagebox.showinfo(title="Operación realizada correctamente", message="Se ha subido el logo de la empresa")
                 elif extension != "jpg" or extension != "png":
                        tk.messagebox.showerror(title="Error", message="Solo se admite subir archivos en formato jpg o png")

def storeData(): #Guardar información en la base de datos
    #Variables de formulario
    enterpriseName = enterprise_entry.get()
    enterprise_ph_1 = enterprise_ph_1_entry.get()
    enterprise_ph_2 = enterprise_ph_2_entry.get()
    enterprise_ph_3 = enterprise_ph_3_entry.get()
    enterprise_ph_4 = enterprise_ph_4_entry.get()
    enterprise_email = enterprise_email_entry.get()
    enterprise_dir = enterprise_dir_entry.get()
    enterprise_dir_2 = enterprise_dir_2_entry.get()
    enterprise_note = enterprise_note_entry.get()
    errorFlag = FALSE;  #Manejo errores de validación con bandera booleana
    
    #Validación campos formulario
    if enterpriseName == "":
       tk.messagebox.showerror(title="Error", message="El nombre de la empresa no debe de estar vacío")
       errorFlag = True;
    if enterprise_ph_1 == "":
       tk.messagebox.showerror(title="Error", message="El número de teléfono de referencia 1 no debe de estar vacío")
       errorFlag = True;
    if enterprise_ph_2 == "":
       tk.messagebox.showerror(title="Error", message="El número de teléfono de referencia 2 no debe de estar vacío")
       errorFlag = True;
    if enterprise_email == "":
       tk.messagebox.showerror(title="Error", message="El correo electrónico no debe de estar vacío")
       errorFlag = True;
    if enterprise_dir == "":
       tk.messagebox.showerror(title="Error", message="La dirección del taller de la empresa no debe de estar vacía")
       errorFlag = True;
    if enterprise_note == "":
       tk.messagebox.showerror(title="Error", message="La nota de la orden de trabajo de la empresa no debe de estar vacía")
       errorFlag = True;
    if enterprise_dir_2 == "":
       tk.messagebox.showerror(title="Error", message="La dirección de la planta de la empresa no debe de estar vacía")
       errorFlag = True;
    
    #Validación longitud caracteres
    if enterpriseName != "" and len(enterpriseName) > 200:
        tk.messagebox.showerror(title="Error", message="El nombre la empresa no debe superar los 200 caracteres")
        errorFlag = True;
    if enterprise_dir != "" and len(enterprise_dir) > 200:
        tk.messagebox.showerror(title="Error", message="La dirección del taller de la empresa no debe de superar los 200 caracteres")
        errorFlag = True;
    if enterprise_dir_2 != "" and len(enterprise_dir_2) > 200:
        tk.messagebox.showerror(title="Error", message="La dirección de la planta de la empresa no debe de superar los 200 caracteres")
        errorFlag = True;
    if enterprise_note != "" and len(enterprise_note) > 200:
        tk.messagebox.showerror(title="Error", message="La nota de la empresa no debe superar los 100 caracteres")
        errorFlag = True;
    if enterprise_ph_1 != "" and len(enterprise_ph_1) > 10:
        tk.messagebox.showerror(title="Error", message="El teléfono de referencia 1 de la empresa no debe superar los 10 caracteres")
        errorFlag = True;
    if enterprise_ph_2 != "" and len(enterprise_ph_2) > 10:
        tk.messagebox.showerror(title="Error", message="El teléfono de referencia 2 de la empresa no debe superar los 10 caracteres")
        errorFlag = True;
    if enterprise_ph_3 != "" and len(enterprise_ph_3) > 10:
        tk.messagebox.showerror(title="Error", message="El teléfono de referencia 3 de la empresa no debe superar los 10 caracteres")
        errorFlag = True;
    if enterprise_ph_4 != "" and len(enterprise_ph_4) > 10:
        tk.messagebox.showerror(title="Error", message="El teléfono de referencia 4 de la empresa no debe superar los 10 caracteres")
        errorFlag = True;
    
    if errorFlag == False:
        sql = "UPDATE datosempresa SET DireccionTaller = %s, Correo = %s, TextoNota = %s, NombreEmpresa = %s, TelReferencia1 = %s, TelReferencia2 = %s, TelReferencia3 = %s, TelReferencia4 = %s, DireccionPlanta = %s"
        values = (enterprise_dir, enterprise_email, enterprise_note, enterpriseName, enterprise_ph_1, enterprise_ph_2, enterprise_ph_3, enterprise_ph_4, enterprise_dir_2)
        query.execute(sql, values)
        conn.dbConnect().commit()
        tk.messagebox.showinfo(title="Operación realizada correctamente", message="Se ha registrado la información de la empresa")
        window.withdraw()
        UserRegister.createWindow()

def reset(): #Reiniciar formulario
        enterprise_entry.delete(0, END)
        enterprise_ph_1_entry.delete(0, END)
        enterprise_ph_2_entry.delete(0, END)
        enterprise_ph_3_entry.delete(0, END)
        enterprise_ph_4_entry.delete(0, END)
        enterprise_email_entry.delete(0, END)
        enterprise_dir_entry.delete(0, END)
        enterprise_note_entry.delete(0, END)
        enterprise_dir_2_entry.delete(0, END)
        
def createWindow():
    global window, enterprise_entry, enterprise_ph_1_entry, enterprise_ph_2_entry, enterprise_ph_3_entry, enterprise_ph_4_entry, enterprise_email_entry, enterprise_dir_entry, enterprise_note_entry, enterprise_dir_2_entry
    #Inicia componentes
    window = tk.Tk()
    window.title("Registro de datos de la empresa - Pre registro")
    setWindow(window)

    #Componentes gráficos formulario subida información
    Label(window, text = 'Registro de datos oficiales de la empresa').pack(side = TOP, pady = 10) 
    Label(window, text = 'Los campos asignados con un asterisco son obligatorios (*)').pack(side = TOP, pady = 15) 
    Label(window, text = 'Subir logo de la empresa (*)').place(x=125, y=100)

    upload_button = tk.Button(window, text="Subir logotipo", command=uploadFiles)
    #upload_button.pack(pady=20)
    upload_button.place(x=125, y=130)

    Label(window, text = 'Subir logo de la empresa (*)').place(x=125, y=100)
    enterprise_entry = tk.Entry(window, font=('calibre',10,'normal'))
    enterprise_entry.place(x=425, y=130)
    Label(window, text = 'Nombre oficial de la empresa (*)').place(x=425, y=100)

    enterprise_ph_1_entry = tk.Entry(window, font=('calibre',10,'normal'))
    enterprise_ph_1_entry.place(x=725, y=130)
    Label(window, text = 'Teléfono oficina (*)').place(x=725, y=100)

    enterprise_ph_2_entry = tk.Entry(window, font=('calibre',10,'normal'))
    enterprise_ph_2_entry.place(x=1025, y=130)
    Label(window, text = 'Teléfono celular (*)').place(x=1025, y=100)

    enterprise_ph_3_entry = tk.Entry(window, font=('calibre',10,'normal'))
    enterprise_ph_3_entry.place(x=1325, y=130)
    Label(window, text = 'Teléfono referencia 3').place(x=1325, y=100)

    enterprise_ph_4_entry = tk.Entry(window, font=('calibre',10,'normal'))
    enterprise_ph_4_entry.place(x=125, y=330)
    Label(window, text = 'Teléfono referencia 4').place(x=125, y=300)

    enterprise_email_entry = tk.Entry(window, font=('calibre',10,'normal'))
    enterprise_email_entry.place(x=425, y=330)
    Label(window, text = 'Correo electrónico (*)').place(x=425, y=300)

    enterprise_dir_entry = tk.Entry(window, font=('Arial',10,'normal'))
    enterprise_dir_entry.place(x=725, y=330)
    Label(window, text = 'Dirección taller (*)').place(x=725, y=300)
    
    enterprise_dir_2_entry = tk.Entry(window, font=('Arial',10,'normal'))
    enterprise_dir_2_entry.place(x=1025, y=330)
    Label(window, text = 'Dirección planta (*)').place(x=1025, y=300)

    enterprise_note_entry = tk.Entry(window, font=('calibre',10,'normal'))
    enterprise_note_entry.place(x=1325, y=330)
    Label(window, text = 'Nota orden trabajo (*)').place(x=1325, y=300)

    save_button = tk.Button(window, text="Guardar datos", command=storeData)
    save_button.place(x=125, y=500)

    cancel_button = tk.Button(window, text="Limpiar", command=reset)
    cancel_button.place(x=225, y=500)

    window.mainloop()

   