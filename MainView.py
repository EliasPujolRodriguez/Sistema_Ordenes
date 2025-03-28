from Connection import Connection
import tkinter as tk
from tkinter import ttk as ttk
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
    global window, customerBtnMenu, enterprise_entry, enterprise_ph_1_entry, enterprise_ph_2_entry, enterprise_ph_3_entry, enterprise_ph_4_entry, enterprise_email_entry, enterprise_dir_entry, enterprise_note_entry
    #Inicia componentes
    window = tk.Tk()
    window.title("Apartado principal")
    setWindow(window)
    
    frame = tk.Frame(window, bg='#2A2A2A')
    frame.place(relwidth=1, relheight=1)
    
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
    logoutMenu.add_command(label="Salir del programa", command=logout)
    
    menubar.add_cascade(label="Clientes", menu=customerseMenu)
    menubar.add_cascade(label="Configuración", menu=configMenu)
    menubar.add_cascade(label="Cerrar sesión", menu=logoutMenu)
    
    oficialLogo = PhotoImage(file = r"..\\Sistema python\\Resources\Logo\\logo_principal.JPG", master=window) 

    #Componentes gráficos formulario
    labelLogo = Label(window, text = '', compound="center",  image = oficialLogo,  bg='#2A2A2A', fg="white", font=("Helvetica", 16) )
    labelLogo.place(x=620, y=25)
    
    #Iconos botones
    addCustomerIcon = PhotoImage(file = r"..\Sistema python\Resources\Icons\add_customer.png", master=window) 
    addOrderIcon = PhotoImage(file = r"..\Sistema python\Resources\Icons\add_order.png", master=window) 
    configIcon = PhotoImage(file = r"..\Sistema python\Resources\Icons\refresh.png", master=window) 
    iconUpdateProfile = PhotoImage(file = r"..\Sistema python\Resources\Icons\config.png", master=window) 
    enterpriseData = PhotoImage(file = r"..\Sistema python\Resources\Icons\enterprise_data.png", master=window) 
    logoutIcon  = PhotoImage(file = r"..\Sistema python\Resources\Icons\logout.png", master=window) 

    customerBtnMenu = tk.Button(window, relief="flat", borderwidth=0, text=" Registrar nuevo cliente", fg='White', bg='#2E5EA0', 
                activebackground='White', compound="left", justify="left", image = addCustomerIcon, command=customersView, font =('Helvetica', 14))
    customerBtnMenu.grid(row = 1, column = 2)
    customerBtnMenu.place(x=300, y=300)
    
    orderViewBtnMenu = tk.Button(window, relief="flat", borderwidth=0, text=" Registrar orden de trabajo", fg='White', bg='#2E5EA0', 
                activebackground='White', compound="left", justify="left", image = addOrderIcon, command=orderView, font =('Helvetica', 14))
    orderViewBtnMenu.grid(row = 1, column = 2)
    orderViewBtnMenu.place(x=550, y=300)
    
    updBtnMenu = tk.Button(window, relief="flat", borderwidth=0, text=" Actualizar sistema",  fg='White', bg='#2E5EA0', 
                activebackground='White', compound="left", justify="left", image = configIcon, command=updSystem, font =('Helvetica', 14))
    updBtnMenu.grid(row = 1, column = 2)
    updBtnMenu.place(x=840, y=300)
    
    config1BtnMenu = tk.Button(window, relief="flat", borderwidth=0, text=" Editar mi perfil usuario", fg='White', bg='#2E5EA0', 
                activebackground='White', compound="left", justify="left", image = iconUpdateProfile, command=configurationView, font =('Helvetica', 14) )
    config1BtnMenu.grid(row = 1, column = 2)
    config1BtnMenu.place(x=300, y=400)
    
    config2BtnMenu = tk.Button(window, relief="flat", borderwidth=0, text=" Editar datos de la empresa", fg='White', bg='#2E5EA0', 
                activebackground='White', compound="left", justify="left", image = enterpriseData, command=configurationView2, font =('Helvetica', 14))
    config2BtnMenu.grid(row = 1, column = 2)
    config2BtnMenu.place(x=550, y=400)
    
    logoutBtn =  tk.Button(window, relief="flat", borderwidth=0, text=" Salir del programa", fg='White', bg='#2E5EA0', 
                activebackground='White', compound="left", justify="left", image = logoutIcon, command=logout, font =('Helvetica', 14))
    logoutBtn.grid(row = 1, column = 2)
    logoutBtn.place(x=840, y=400)
    
    window.mainloop()
    
   
    

    
    
    