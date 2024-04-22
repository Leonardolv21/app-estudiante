import psycopg2

class conexionpg:
    def __init__(self, dbname, user, password, host="localhost", port="5432"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conexion = None
        self.cursor = None

    def conectar(self):
        try:
            self.conexion = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conexion.cursor()
            print("Conexión establecida correctamente.")
            return self.conexion
        except psycopg2.Error as e:
            print("Error al conectar a la base de datos:", e)
            return None

    def ejecutar_consulta(self, consulta, parametros=None):
        if self.conexion is None:
            self.conectar()  # Intentamos conectar si la conexión aún no está establecida
        try:
            if parametros:
                self.cursor.execute(consulta, parametros)
            else:
                self.cursor.execute(consulta)
            resultado = self.cursor.fetchall()
            self.conexion.commit()
            return resultado
        except psycopg2.Error as e:
            print("Error al ejecutar la consulta:", e)
            return None
        finally:
            if self.conexion:
                self.conexion.close()
                print("Conexión cerrada correctamente.")

bd = conexionpg(dbname="registroestudiantil", user="postgres", password="123456789")

