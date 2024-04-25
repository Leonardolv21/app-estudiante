import psycopg2

# Definir la clase Estudiante
class Estudiante:
    def __init__(self, id_estudiante, nombre_completo, fecha_nacimiento, carrera):
        self.id_estudiante = id_estudiante
        self.nombre_completo = nombre_completo
        self.fecha_nacimiento = fecha_nacimiento
        self.carrera = carrera
        self.materias = []

# Definir la clase Materia
class Materia:
    def __init__(self, codigo, nombre, num_creditos):
        self.codigo = codigo
        self.nombre = nombre
        self.num_creditos = num_creditos
        self.notas = []

# Definir la clase Nota
class Nota:
    def __init__(self, id_nota, nombre, puntaje, codigo_materia, id_estudiante):
        self.id_nota = id_nota
        self.nombre = nombre
        self.puntaje = puntaje
        self.codigo_materia = codigo_materia
        self.id_estudiante = id_estudiante

# Función para crear un nuevo estudiante
def crear_estudiante():
    id_estudiante = int(input("Ingrese el ID del estudiante: "))
    nombre_completo = input("Ingrese el nombre completo del estudiante: ")
    fecha_nacimiento = input("Ingrese la fecha de nacimiento del estudiante (YYYY-MM-DD): ")
    carrera = input("Ingrese la carrera del estudiante: ")

    try:
        cursor.execute("INSERT INTO Estudiante (id_estudiante, nombre_completo, fecha_nacimiento, carrera) VALUES (%s, %s, %s, %s)",
                       (id_estudiante, nombre_completo, fecha_nacimiento, carrera))
        conexion.commit()
        print("Estudiante creado con éxito. ID:", id_estudiante)
    except psycopg2.Error as e:
        conexion.rollback()
        print("Error al crear estudiante:", e)

# Función para crear una nueva materia
def crear_materia():
    nombre = input("Ingrese el nombre de la materia: ")
    num_creditos = int(input("Ingrese el número de créditos de la materia: "))

    try:
        cursor.execute("INSERT INTO Materia (nombre, num_creditos) VALUES (%s, %s) RETURNING codigo",
                       (nombre, num_creditos))
        codigo = cursor.fetchone()[0]
        conexion.commit()
        print("Materia creada con éxito. Código:", codigo)
    except psycopg2.Error as e:
        conexion.rollback()
        print("Error al crear materia:", e)

# Función para crear una nueva nota
def crear_nota():
    nombre_nota = input("Ingrese el nombre de la nota: ")
    puntaje = float(input("Ingrese el puntaje de la nota: "))
    codigo_materia = int(input("Ingrese el código de la materia: "))
    id_estudiante = int(input("Ingrese el ID del estudiante: "))

    try:
        cursor.execute("INSERT INTO Notas (nombre_nota, puntaje, codigo_materia, id_estudiante) VALUES (%s, %s, %s, %s)",
                       (nombre_nota, puntaje, codigo_materia, id_estudiante))
        conexion.commit()
        print("Nota creada con éxito.")
    except psycopg2.Error as e:
        conexion.rollback()
        print("Error al crear nota:", e)

# Función para ver la lista de estudiantes registrados
def ver_estudiantes():
    try:
        cursor.execute("SELECT * FROM Estudiante")
        estudiantes = cursor.fetchall()
        if not estudiantes:
            print("No hay estudiantes registrados.")
        else:
            print("Lista de estudiantes registrados:")
            for estudiante in estudiantes:
                print(f"ID: {estudiante[0]}, Nombre completo: {estudiante[1]}, Fecha de nacimiento: {estudiante[2]}, Carrera: {estudiante[3]}")
    except psycopg2.Error as e:
        print("Error al recuperar la lista de estudiantes:", e)

# Función para ver las materias en las que está inscrito un estudiante específico
def ver_materias_estudiante():
    id_estudiante = int(input("Ingrese el ID del estudiante: "))
    try:
        cursor.execute("SELECT m.nombre FROM Materia m INNER JOIN Estudiante_Materia em ON m.codigo = em.codigo_materia WHERE em.id_estudiante = %s", (id_estudiante,))
        materias = cursor.fetchall()
        if not materias:
            print("El estudiante no está inscrito en ninguna materia.")
        else:
            print("Materias en las que está inscrito el estudiante:")
            for materia in materias:
                print(materia[0])
    except psycopg2.Error as e:
        print("Error al recuperar las materias del estudiante:", e)

# Función para ver las notas de un estudiante en una materia específica
def ver_notas_estudiante_materia():
    id_estudiante = int(input("Ingrese el ID del estudiante: "))
    codigo_materia = int(input("Ingrese el código de la materia: "))
    try:
        cursor.execute("SELECT nombre_nota, puntaje FROM Notas WHERE id_estudiante = %s AND codigo_materia = %s", (id_estudiante, codigo_materia))
        notas = cursor.fetchall()
        if not notas:
            print("El estudiante no tiene notas registradas en esta materia.")
        else:
            print("Notas del estudiante en la materia:")
            for nota in notas:
                print(f"{nota[0]}: {nota[1]}")
    except psycopg2.Error as e:
        print("Error al recuperar las notas del estudiante en la materia:", e)

# Función para calcular el promedio de notas de un estudiante en una materia específica
def calcular_promedio_notas_estudiante_materia():
    id_estudiante = int(input("Ingrese el ID del estudiante: "))
    codigo_materia = int(input("Ingrese el código de la materia: "))
    try:
        cursor.execute("SELECT AVG(puntaje) FROM Notas WHERE id_estudiante = %s AND codigo_materia = %s", (id_estudiante, codigo_materia))
        promedio = cursor.fetchone()[0]
        if promedio is None:
            print("El estudiante no tiene notas registradas en esta materia.")
        else:
            print(f"El promedio de notas del estudiante en la materia es: {promedio}")
    except psycopg2.Error as e:
        print("Error al calcular el promedio de notas del estudiante en la materia:", e)

# Función para actualizar la información de un estudiante
def actualizar_estudiante():
    id_estudiante = int(input("Ingrese el ID del estudiante que desea actualizar: "))
    nombre_completo = input("Ingrese el nuevo nombre completo del estudiante: ")
    fecha_nacimiento = input("Ingrese la nueva fecha de nacimiento del estudiante (YYYY-MM-DD): ")
    carrera = input("Ingrese la nueva carrera del estudiante: ")

    try:
        cursor.execute("UPDATE Estudiante SET nombre_completo = %s, fecha_nacimiento = %s, carrera = %s WHERE id_estudiante = %s",
                       (nombre_completo, fecha_nacimiento, carrera, id_estudiante))
        conexion.commit()
        print("Información del estudiante actualizada con éxito.")
    except psycopg2.Error as e:
        conexion.rollback()
        print("Error al actualizar la información del estudiante:", e)

# Función para actualizar la información de una materia
def actualizar_materia():
    codigo_materia = int(input("Ingrese el código de la materia que desea actualizar: "))
    nombre = input("Ingrese el nuevo nombre de la materia: ")
    num_creditos = int(input("Ingrese el nuevo número de créditos de la materia: "))

    try:
        cursor.execute("UPDATE Materia SET nombre = %s, num_creditos = %s WHERE codigo = %s",
                       (nombre, num_creditos, codigo_materia))
        conexion.commit()
        print("Información de la materia actualizada con éxito.")
    except psycopg2.Error as e:
        conexion.rollback()
        print("Error al actualizar la información de la materia:", e)

# Función para eliminar un estudiante
def eliminar_estudiante():
    id_estudiante = int(input("Ingrese el ID del estudiante que desea eliminar: "))
    try:
        cursor.execute("DELETE FROM Estudiante WHERE id_estudiante = %s", (id_estudiante,))
        conexion.commit()
        print("Estudiante eliminado con éxito.")
    except psycopg2.Error as e:
        conexion.rollback()
        print("Error al eliminar el estudiante:", e)

# Función para eliminar una materia
def eliminar_materia():
    codigo_materia = int(input("Ingrese el código de la materia que desea eliminar: "))
    try:
        # Verificar si la materia existe
        cursor.execute("select * from estudiante_materia WHERE id = %s", (codigo_materia,))
        cursor.execute("SELECT * FROM Materia WHERE codigo = %s", (codigo_materia,))
        materia = cursor.fetchone()
        if not materia:
            print("La materia que desea eliminar no existe.")
        else:
            # Eliminar la materia si existe
            cursor.execute("DELETE FROM estudiante_materia WHERE id = %s", (codigo_materia,))
            cursor.execute("DELETE FROM Materia WHERE codigo = %s", (codigo_materia,))
            conexion.commit()
            print("Materia eliminada con éxito.")
    except psycopg2.Error as e:
        conexion.rollback()
        print("Error al eliminar la materia:", e)


# Función para mostrar el menú
def mostrar_menu():
    print("\nMenú:")
    print("1. Crear estudiante")
    print("2. Crear materia")
    print("3. Crear nota")
    print("4. Ver lista de estudiantes")
    print("5. Ver materias de un estudiante")
    print("6. Ver notas de un estudiante en una materia")
    print("7. Calcular promedio de notas de un estudiante en una materia")
    print("8. Actualizar información de un estudiante")
    print("9. Actualizar información de una materia")
    print("10. Eliminar estudiante")
    print("11. Eliminar materia")
    print("12. Salir")

# Conexión a la base de datos
try:
    conexion = psycopg2.connect(
        dbname="registroestudiantil",
        user="postgres",
        password="123456789",
        host="localhost",
        port="5432"
    )
    print("Conexión exitosa.")
    cursor = conexion.cursor()

    # Bucle principal del programa
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            crear_estudiante()
        elif opcion == "2":
            crear_materia()
        elif opcion == "3":
            crear_nota()
        elif opcion == "4":
            ver_estudiantes()
        elif opcion == "5":
            ver_materias_estudiante()
        elif opcion == "6":
            ver_notas_estudiante_materia()
        elif opcion == "7":
            calcular_promedio_notas_estudiante_materia()
        elif opcion == "8":
            actualizar_estudiante()
        elif opcion == "9":
            actualizar_materia()
        elif opcion == "10":
            eliminar_estudiante()
        elif opcion == "11":
            eliminar_materia()
        elif opcion == "12":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")

    # Cerrar conexión
    cursor.close()
    conexion.close()

except psycopg2.Error as e:
    print("Error al conectar a la base de datos:", e)