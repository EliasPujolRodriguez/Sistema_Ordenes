#Clase conexión a la base de datos 
import mysql.connector

class Connection():
    def __init__(self, usr, host, psw, database, port):     
        #Atributos de clase   
        self.usr = usr
        self.host = host
        self.psw = psw
        self.database = database
        self.port = port
        self.con = None
        
    def dbConnect(self): #Conexión con la base de datos
        if self.con is None:
            self.con = mysql.connector.connect(
                 user = self.usr,
            host = self.host, passwd = self.psw,
            database = self.database,
                                    port = self.port                    
        ) 

        return self.con

    

