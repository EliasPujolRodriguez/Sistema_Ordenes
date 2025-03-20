from Connection import Connection
import tkinter as tk
from tkinter import messagebox
from tkinter import * 
from tkinter import filedialog
import UpdateUserView as UpdateUserView, UpdateEnterprise as UpdateEnterprise, CustomerView as CustomerView, OrderRegisterView as OrderRegisterView, CustomersCRUDView as CustomersCRUDView, OrderCRUD as OrderCRUD

#Instancia de clase conexión
conn = Connection("root", "localhost", "", "muebles", "3306")
query = conn.dbConnect().cursor()

def setWindow(window):
    window.update()
    w, h = window.maxsize()
    window.wm_overrideredirect(True)
    window.geometry(f'{w}x{h}+0+0')  
     
def customersView():
     window.withdraw()
     CustomerView.createWindow();    
def orderView():
     window.withdraw()
     OrderRegisterView.createWindow()
         
def configurationView():
         window.withdraw()
         UpdateUserView.createWindow()
def configurationView2():
         window.withdraw()
         UpdateEnterprise.createWindow()
         
def orderCrudView():
      window.withdraw()
      OrderCRUD.createWindow() 
      
def logout():
     window.withdraw()
     exit() 

def updSystem(): #Forzar a actualizar datos de la base de datos
     sql3 = "SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED;"
     query.execute(sql3)
     conn.dbConnect().commit()
     #conn.dbConnect().cursor().close()
     tk.messagebox.showinfo(title="Operación realizada correctamente", message="Se ha actualizado la base de datos correctamente")

def customersCRUDView():
     window.withdraw()
     CustomersCRUDView.createWindow()

def createWindow():
    global window, enterprise_entry, enterprise_ph_1_entry, enterprise_ph_2_entry, enterprise_ph_3_entry, enterprise_ph_4_entry, enterprise_email_entry, enterprise_dir_entry, enterprise_note_entry
    #Inicia componentes
    window = tk.Tk()
    window.title("Apartado principal")
    #window.geometry("500x400")
    setWindow(window)
    
    menubar = Menu(window)
    window.config(menu=menubar)  # Creación de componente menú
    #Submenús
    customerseMenu = Menu(menubar, tearoff=0)
    customerseMenu.add_command(label="Registrar clientes", command=customersView)
    customerseMenu.add_command(label="Administración de clientes", command=customersCRUDView)
    customerseMenu.add_command(label="Administración de orden de trabajo", command=orderCrudView)
    configMenu = Menu(menubar, tearoff=0)
    configMenu.add_command(label="Editar Perfil usuario", command=configurationView)
    configMenu.add_command(label="Configuración datos empresa", command=configurationView2)
    logoutMenu = Menu(menubar, tearoff=0) 
    logoutMenu.add_command(label="Salir del sistema", command=logout)
    
    menubar.add_cascade(label="Clientes", menu=customerseMenu)
    menubar.add_cascade(label="Configuración", menu=configMenu)
    menubar.add_cascade(label="Cerrar sesión", menu=logoutMenu)

    #Componentes gráficos formulario subida información
    Label(window, text = 'Apartado principal').pack(side = TOP, pady = 10) 
    
    customerBtnMenu = tk.Button(window, text="Clientes - Registrar nuevo cliente", command=customersView)
    customerBtnMenu.pack(side = TOP, pady = 45) 
    
    orderViewBtnMenu = tk.Button(window, text="Clientes - Registro de ordenes", command=orderView)
    orderViewBtnMenu.pack(side = TOP, pady = 50) 
    
    updBtnMenu = tk.Button(window, text="Configuración - Actualizar sistema", command=updSystem)
    updBtnMenu.pack(side = TOP, pady = 55) 
    
    config1BtnMenu = tk.Button(window, text="Configuración - Editar perfil usuario", command=configurationView)
    config1BtnMenu.pack(side = TOP, pady = 60) 
    
    config2BtnMenu = tk.Button(window, text="Configuración - Configuración general sistema", command=configurationView2)
    config2BtnMenu.pack(side = TOP, pady = 65) 
    
    window.mainloop()
    
   
    

    
    
    