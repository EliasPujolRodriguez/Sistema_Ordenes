from Connection import Connection
import RegisterForm as RegisterForm
import UserRegister as UserRegister
import Login as Login

#Instancia de clase conexión
conn = Connection("root", "localhost", "", "muebles", "3306")
query = conn.dbConnect().cursor()
searchSql = ""
q2 = ""
counterEnterprise = 0

#Consulta que sirve para determinar los datos totales de la información de la empresa, que va a servir para determinar que interfaz se verá
searchSql = "SELECT COUNT(IdEmpresa) FROM datosempresa"
query.execute(searchSql)
q = query.fetchall()

for i in q:
         counterEnterprise = i[0]
         
#Consulta que sirve para determinar los datos totales de los usuarios registrados relacionados con la empresa que va a servir para determinar que interfaz se verá
searchSql2 = "SELECT COUNT(IdUsuario) FROM usuarios;"
query.execute(searchSql2)
q2 = query.fetchall()
conn.dbConnect().cursor().close()

for i in q2:
         counterUsrEnterprise2 = i[0]

if counterEnterprise == 0 and counterUsrEnterprise2 == 0: #En caso de que no se haya registrado información de la empresa o del usuario administrador del sistema, se va a mostrar lo siguiente
    RegisterForm.createWindow()
elif counterEnterprise == 1 and counterUsrEnterprise2 == 0:
    UserRegister.createWindow()
elif counterEnterprise == 1 and counterUsrEnterprise2 == 1:
    Login.createWindow() 