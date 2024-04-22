import tkinter as tk
from tkinter import messagebox  
import psycopg2
from conexionpg import conexionpg  

# Definición de clases
class Nota:
    def __init__(self, id_nota, nombre, puntaje, id_materia, id_grupo):
        self.id_nota = id_nota
        self.nombre = nombre
        self.puntaje = puntaje
        self.id_materia = id_materia
        self.id_grupo = id_grupo

class Materia:
    def __init__(self, codigo, nombre, num_creditos, id_estudiante):
        self.codigo = codigo
        self.nombre = nombre
        self.num_creditos = num_creditos
        self.id_estudiante = id_estudiante
        self.notas = []

    def agregar_nota(self, id_nota, nombre, puntaje, id_materia, id_grupo):
        nota = Nota(id_nota, nombre, puntaje, id_materia, id_grupo)
        self.notas.append(nota)
        
    def buscar_nota_por_nombre(self, nombre_nota):
        for nota in self.notas:
            if nota.nombre == nombre_nota:
                return True
        return False

    def obtener_promedio(self):
        if len(self.notas) == 0:
            return 0
        total_puntajes = sum(float(nota.puntaje) for nota in self.notas)
        return total_puntajes / len(self.notas)

class Estudiante:
    def __init__(self, id_estudiante, nombre_completo, fecha_nacimiento, carrera):
        self.id_estudiante = id_estudiante
        self.nombre_completo = nombre_completo
        self.fecha_nacimiento = fecha_nacimiento
        self.carrera = carrera
        self.materias = []

    def agregar_materia(self, materia):
        self.materias.append(materia)

    def promedio_total(self):
        if len(self.materias) == 0:
            return 0
        total_promedios = sum(materia.obtener_promedio() for materia in self.materias)
        return total_promedios / len(self.materias)
    
    def buscar_materia_por_codigo(self, codigo):
        for materia in self.materias:
            if materia.codigo == codigo:
                return True
        return False

# Variables globales
estudiantes = []
materias = []

# Función para validar la entrada
def validate_input(*args):
    for entry in args:
        if not entry.get():
            show_message("Por favor, complete todos los campos.")
            return False
    return True

# Funciones para agregar elementos
# Función para agregar estudiantes
def agregar_estudiante():
    if validate_input(entry_id_estudiante, entry_nombre_completo, entry_fecha_nacimiento, entry_carrera):
        id_estudiante = entry_id_estudiante.get()
        nombre_completo = entry_nombre_completo.get()
        fecha_nacimiento = entry_fecha_nacimiento.get()
        carrera = entry_carrera.get()
        
        try:
            # Crear una instancia de la clase conexionpg con los argumentos requeridos
            conexion_pg = conexionpg(dbname="registroestudiantil", user="postgres", password="123456789")
            cursor = conexion_pg.cursor()

            # Ejecutar la consulta SQL para insertar el estudiante
            cursor.execute("INSERT INTO estudiante (id_estudiante, nombre_completo, fecha_nacimiento, carrera) VALUES (%s, %s, %s, %s)",
                           (id_estudiante, nombre_completo, fecha_nacimiento, carrera))
            conexion_pg.commit()

            cursor.close()
            conexion_pg.close()

            show_message("Estudiante agregado correctamente.")
            mostrar_toda_informacion()

        except (Exception, psycopg2.Error) as error:
            show_message(f"Error al agregar estudiante: {error}")


# Función para agregar materias
def agregar_materia():
    if validate_input(entry_codigo, entry_nombre, entry_num_creditos):
        codigo = entry_codigo.get()
        nombre = entry_nombre.get()
        num_creditos = entry_num_creditos.get()
        id_estudiante = entry_id_estudiante_materia.get()

        if not id_estudiante:
            show_message("Por favor, ingrese el ID del estudiante.")
            return

        # Verificar si el estudiante existe
        estudiante_encontrado = None
        for estudiante in estudiantes:
            if estudiante.id_estudiante == id_estudiante:
                estudiante_encontrado = estudiante
                break

        if estudiante_encontrado is None:
            show_message("No se encontró el estudiante con el ID proporcionado.")
            return

        # Verificar si la materia ya está asociada al estudiante
        if estudiante_encontrado.buscar_materia_por_codigo(codigo):
            show_message("La materia ya está asociada a este estudiante.")
            return

        try:
            # Crear una instancia de la clase conexionpg con los argumentos requeridos
            conexion = conexionpg(dbname="registroestudiantil", user="postgres", password="123456789")
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para insertar la materia
            cursor.execute("INSERT INTO materia (codigo, nombre, num_creditos, id_estudiante) VALUES (%s, %s, %s, %s)",
                           (codigo, nombre, num_creditos, id_estudiante))
            conexion.commit()

            cursor.close()
            conexion.close()

            # Si la materia no está asociada al estudiante, agregarla
            materia = Materia(codigo, nombre, num_creditos, id_estudiante)
            estudiante_encontrado.agregar_materia(materia)
            materias.append(materia)
            show_message("Materia agregada correctamente.")
            mostrar_toda_informacion()

        except (Exception, psycopg2.Error) as error:
            show_message(f"Error al agregar materia: {error}")

# Funciones para agregar notas
def agregar_notas():
    if validate_input(entry_id_nota, entry_nombre_nota, entry_puntaje, entry_id_materia, entry_id_grupo):
        id_nota = entry_id_nota.get()
        nombre_nota = entry_nombre_nota.get()
        puntaje = entry_puntaje.get()
        id_materia = entry_id_materia.get()
        id_grupo = entry_id_grupo.get()
        
        # Verificar si la nota ya existe
        for materia in materias:
            if materia.codigo == id_materia:
                if materia.buscar_nota_por_nombre(nombre_nota):
                    show_message("La nota ya existe para esta materia.")
                    return
                
        try:
            # Crear una instancia de la clase conexionpg con los argumentos requeridos
            conexion = conexionpg(dbname="registroestudiantil", user="postgres", password="123456789")
            cursor = conexion.cursor()

            # Ejecutar la consulta SQL para insertar la nota
            cursor.execute("INSERT INTO nota (id_nota, nombre, puntaje, id_materia, id_grupo) VALUES (%s, %s, %s, %s, %s)",
                           (id_nota, nombre_nota, puntaje, id_materia, id_grupo))
            conexion.commit()

            cursor.close()
            conexion.close()

            for materia in materias:
                if materia.codigo == id_materia:
                    materia.agregar_nota(id_nota, nombre_nota, puntaje, id_materia, id_grupo)
                    break

            show_message("Nota agregada correctamente.")
            mostrar_toda_informacion()

        except (Exception, psycopg2.Error) as error:
            show_message(f"Error al agregar nota: {error}")

# Funciones para eliminar elementos
# Función para eliminar estudiantes
def eliminar_estudiante():
    id_estudiante = entry_id_estudiante_eliminar.get()
    if not id_estudiante:
        show_message("Por favor, ingrese el ID del estudiante que desea eliminar.")
        return

    try:
        # Crear una instancia de la clase conexionpg con los argumentos requeridos
        conexion = conexionpg(dbname="registroestudiantil", user="postgres", password="123456789")
        cursor = conexion.cursor()

        # Ejecutar la consulta SQL para eliminar el estudiante
        cursor.execute("DELETE FROM estudiante WHERE id_estudiante = %s", (id_estudiante,))
        conexion.commit()

        cursor.close()
        conexion.close()

        for estudiante in estudiantes:
            if estudiante.id_estudiante == id_estudiante:
                estudiantes.remove(estudiante)
                break

        show_message("Estudiante eliminado correctamente.")
        mostrar_toda_informacion()

    except (Exception, psycopg2.Error) as error:
        show_message(f"Error al eliminar estudiante: {error}")

# Función para eliminar materias
def eliminar_materia():
    codigo = entry_codigo_eliminar.get()
    if not codigo:
        show_message("Por favor, ingrese el código de la materia que desea eliminar.")
        return

    try:
        # Crear una instancia de la clase conexionpg con los argumentos requeridos
        conexion = conexionpg(dbname="registroestudiantil", user="postgres", password="123456789")
        cursor = conexion.cursor()

        # Ejecutar la consulta SQL para eliminar la materia
        cursor.execute("DELETE FROM materia WHERE codigo = %s", (codigo,))
        conexion.commit()

        cursor.close()
        conexion.close()

        for materia in materias:
            if materia.codigo == codigo:
                materias.remove(materia)
                break

        show_message("Materia eliminada correctamente.")
        mostrar_toda_informacion()

    except (Exception, psycopg2.Error) as error:
        show_message(f"Error al eliminar materia: {error}")

# Función para eliminar notas
def eliminar_nota():
    nombre_nota = entry_nombre_nota_eliminar.get()
    id_materia = entry_id_materia_eliminar.get()
    if not nombre_nota or not id_materia:
        show_message("Por favor, ingrese el nombre de la nota y el ID de la materia asociada.")
        return

    try:
        # Crear una instancia de la clase conexionpg con los argumentos requeridos
        conexion = conexionpg(dbname="registroestudiantil", user="postgres", password="123456789")
        cursor = conexion.cursor()

        # Ejecutar la consulta SQL para eliminar la nota
        cursor.execute("DELETE FROM nota WHERE nombre = %s AND id_materia = %s", (nombre_nota, id_materia))
        conexion.commit()

        cursor.close()
        conexion.close()

        for materia in materias:
            if materia.codigo == id_materia:
                for nota in materia.notas:
                    if nota.nombre == nombre_nota:
                        materia.notas.remove(nota)
                        break
                break

        show_message("Nota eliminada correctamente.")
        mostrar_toda_informacion()

    except (Exception, psycopg2.Error) as error:
        show_message(f"Error al eliminar nota: {error}")

# Funciones para modificar elementos
# Función para modificar estudiantes
def modificar_estudiante():
    id_estudiante = entry_id_estudiante_modificar.get()
    nuevo_nombre = entry_nuevo_nombre_estudiante.get()
    nueva_fecha = entry_nueva_fecha_nacimiento.get()
    nueva_carrera = entry_nueva_carrera.get()

    if not id_estudiante or not (nuevo_nombre or nueva_fecha or nueva_carrera):
        show_message("Por favor, ingrese el ID del estudiante y al menos uno de los campos a modificar.")
        return

    try:
        # Crear una instancia de la clase conexionpg con los argumentos requeridos
        conexion = conexionpg(dbname="registroestudiantil", user="postgres", password="123456789")
        cursor = conexion.cursor()

        # Construir la consulta SQL para modificar los datos del estudiante
        query = "UPDATE estudiante SET "
        params = []
        if nuevo_nombre:
            query += "nombre_completo = %s, "
            params.append(nuevo_nombre)
        if nueva_fecha:
            query += "fecha_nacimiento = %s, "
            params.append(nueva_fecha)
        if nueva_carrera:
            query += "carrera = %s, "
            params.append(nueva_carrera)
        # Eliminar la última coma y espacio
        query = query[:-2]
        query += " WHERE id_estudiante = %s"
        params.append(id_estudiante)

        # Ejecutar la consulta SQL para modificar los datos del estudiante
        cursor.execute(query, tuple(params))
        conexion.commit()

        cursor.close()
        conexion.close()

        for estudiante in estudiantes:
            if estudiante.id_estudiante == id_estudiante:
                if nuevo_nombre:
                    estudiante.nombre_completo = nuevo_nombre
                if nueva_fecha:
                    estudiante.fecha_nacimiento = nueva_fecha
                if nueva_carrera:
                    estudiante.carrera = nueva_carrera
                break

        show_message("Datos del estudiante modificados correctamente.")
        mostrar_toda_informacion()

    except (Exception, psycopg2.Error) as error:
        show_message(f"Error al modificar datos del estudiante: {error}")

# Función para modificar materias
def modificar_materia():
    codigo = entry_codigo_modificar.get()
    nuevo_nombre = entry_nuevo_nombre_materia.get()
    nuevos_creditos = entry_nuevos_creditos.get()

    if not codigo or not (nuevo_nombre or nuevos_creditos):
        show_message("Por favor, ingrese el código de la materia y al menos uno de los campos a modificar.")
        return

    try:
        # Crear una instancia de la clase conexionpg con los argumentos requeridos
        conexion = conexionpg(dbname="registroestudiantil", user="postgres", password="123456789")
        cursor = conexion.cursor()

        # Construir la consulta SQL para modificar los datos de la materia
        query = "UPDATE materia SET "
        params = []
        if nuevo_nombre:
            query += "nombre = %s, "
            params.append(nuevo_nombre)
        if nuevos_creditos:
            query += "num_creditos = %s, "
            params.append(nuevos_creditos)
        # Eliminar la última coma y espacio
        query = query[:-2]
        query += " WHERE codigo = %s"
        params.append(codigo)

        # Ejecutar la consulta SQL para modificar los datos de la materia
        cursor.execute(query, tuple(params))
        conexion.commit()

        cursor.close()
        conexion.close()

        for materia in materias:
            if materia.codigo == codigo:
                if nuevo_nombre:
                    materia.nombre = nuevo_nombre
                if nuevos_creditos:
                    materia.num_creditos = nuevos_creditos
                break

        show_message("Datos de la materia modificados correctamente.")
        mostrar_toda_informacion()

    except (Exception, psycopg2.Error) as error:
        show_message(f"Error al modificar datos de la materia: {error}")

# Función para mostrar un mensaje en una ventana emergente
def show_message(message):
    messagebox.showinfo("Mensaje", message)

# Función para mostrar toda la información en la ventana de salida
def mostrar_toda_informacion():
    text_output.delete("1.0", tk.END)
    for estudiante in estudiantes:
        text_output.insert(tk.END, f"ID Estudiante: {estudiante.id_estudiante}\nNombre: {estudiante.nombre_completo}\n"
                                   f"Fecha de Nacimiento: {estudiante.fecha_nacimiento}\nCarrera: {estudiante.carrera}\n")
        for materia in estudiante.materias:
            text_output.insert(tk.END, f"\n\tCódigo Materia: {materia.codigo}\n\tNombre Materia: {materia.nombre}\n"
                                       f"\tNúmero de Créditos: {materia.num_creditos}\n")
            for nota in materia.notas:
                text_output.insert(tk.END, f"\t\tID Nota: {nota.id_nota}\n\t\tNombre Nota: {nota.nombre}\n"
                                           f"\t\tPuntaje: {nota.puntaje}\n\t\tID Materia: {nota.id_materia}\n"
                                           f"\t\tID Grupo: {nota.id_grupo}\n")
    text_output.config(state=tk.DISABLED)

# Crear la ventana principal
root = tk.Tk()
root.title("Registro Estudiantil")

# Crear etiquetas y campos de entrada
# Para agregar estudiantes
label_id_estudiante = tk.Label(root, text="ID Estudiante:")
label_id_estudiante.grid(row=0, column=0)
entry_id_estudiante = tk.Entry(root)
entry_id_estudiante.grid(row=0, column=1)

label_nombre_completo = tk.Label(root, text="Nombre Completo:")
label_nombre_completo.grid(row=1, column=0)
entry_nombre_completo = tk.Entry(root)
entry_nombre_completo.grid(row=1, column=1)

label_fecha_nacimiento = tk.Label(root, text="Fecha de Nacimiento:")
label_fecha_nacimiento.grid(row=2, column=0)
entry_fecha_nacimiento = tk.Entry(root)
entry_fecha_nacimiento.grid(row=2, column=1)

label_carrera = tk.Label(root, text="Carrera:")
label_carrera.grid(row=3, column=0)
entry_carrera = tk.Entry(root)
entry_carrera.grid(row=3, column=1)

button_agregar_estudiante = tk.Button(root, text="Agregar Estudiante", command=agregar_estudiante)
button_agregar_estudiante.grid(row=4, column=0, columnspan=2)

# Para agregar materias
label_id_estudiante_materia = tk.Label(root, text="ID Estudiante:")
label_id_estudiante_materia.grid(row=0, column=2)
entry_id_estudiante_materia = tk.Entry(root)
entry_id_estudiante_materia.grid(row=0, column=3)

label_codigo = tk.Label(root, text="Código:")
label_codigo.grid(row=1, column=2)
entry_codigo = tk.Entry(root)
entry_codigo.grid(row=1, column=3)

label_nombre = tk.Label(root, text="Nombre:")
label_nombre.grid(row=2, column=2)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=2, column=3)

label_num_creditos = tk.Label(root, text="Número de Créditos:")
label_num_creditos.grid(row=3, column=2)
entry_num_creditos = tk.Entry(root)
entry_num_creditos.grid(row=3, column=3)

button_agregar_materia = tk.Button(root, text="Agregar Materia", command=agregar_materia)
button_agregar_materia.grid(row=4, column=2, columnspan=2)

# Para agregar notas
label_id_nota = tk.Label(root, text="ID Nota:")
label_id_nota.grid(row=0, column=4)
entry_id_nota = tk.Entry(root)
entry_id_nota.grid(row=0, column=5)

label_nombre_nota = tk.Label(root, text="Nombre Nota:")
label_nombre_nota.grid(row=1, column=4)
entry_nombre_nota = tk.Entry(root)
entry_nombre_nota.grid(row=1, column=5)

label_puntaje = tk.Label(root, text="Puntaje:")
label_puntaje.grid(row=2, column=4)
entry_puntaje = tk.Entry(root)
entry_puntaje.grid(row=2, column=5)

label_id_materia = tk.Label(root, text="ID Materia:")
label_id_materia.grid(row=3, column=4)
entry_id_materia = tk.Entry(root)
entry_id_materia.grid(row=3, column=5)

label_id_grupo = tk.Label(root, text="ID Grupo:")
label_id_grupo.grid(row=4, column=4)
entry_id_grupo = tk.Entry(root)
entry_id_grupo.grid(row=4, column=5)

button_agregar_nota = tk.Button(root, text="Agregar Nota", command=agregar_notas)
button_agregar_nota.grid(row=5, column=4, columnspan=2)

# Para eliminar estudiantes
label_id_estudiante_eliminar = tk.Label(root, text="ID Estudiante:")
label_id_estudiante_eliminar.grid(row=6, column=0)
entry_id_estudiante_eliminar = tk.Entry(root)
entry_id_estudiante_eliminar.grid(row=6, column=1)

button_eliminar_estudiante = tk.Button(root, text="Eliminar Estudiante", command=eliminar_estudiante)
button_eliminar_estudiante.grid(row=7, column=0, columnspan=2)

# Para eliminar materias
label_codigo_eliminar = tk.Label(root, text="Código:")
label_codigo_eliminar.grid(row=6, column=2)
entry_codigo_eliminar = tk.Entry(root)
entry_codigo_eliminar.grid(row=6, column=3)

button_eliminar_materia = tk.Button(root, text="Eliminar Materia", command=eliminar_materia)
button_eliminar_materia.grid(row=7, column=2, columnspan=2)

# Para eliminar notas
label_nombre_nota_eliminar = tk.Label(root, text="Nombre Nota:")
label_nombre_nota_eliminar.grid(row=6, column=4)
entry_nombre_nota_eliminar = tk.Entry(root)
entry_nombre_nota_eliminar.grid(row=6, column=5)

label_id_materia_eliminar = tk.Label(root, text="ID Materia:")
label_id_materia_eliminar.grid(row=7, column=4)
entry_id_materia_eliminar = tk.Entry(root)
entry_id_materia_eliminar.grid(row=7, column=5)

button_eliminar_nota = tk.Button(root, text="Eliminar Nota", command=eliminar_nota)
button_eliminar_nota.grid(row=8, column=4, columnspan=2)

# Para modificar estudiantes
label_id_estudiante_modificar = tk.Label(root, text="ID Estudiante:")
label_id_estudiante_modificar.grid(row=8, column=0)
entry_id_estudiante_modificar = tk.Entry(root)
entry_id_estudiante_modificar.grid(row=8, column=1)

label_nuevo_nombre_estudiante = tk.Label(root, text="Nuevo Nombre:")
label_nuevo_nombre_estudiante.grid(row=9, column=0)
entry_nuevo_nombre_estudiante = tk.Entry(root)
entry_nuevo_nombre_estudiante.grid(row=9, column=1)

label_nueva_fecha_nacimiento = tk.Label(root, text="Nueva Fecha de Nacimiento:")
label_nueva_fecha_nacimiento.grid(row=10, column=0)
entry_nueva_fecha_nacimiento = tk.Entry(root)
entry_nueva_fecha_nacimiento.grid(row=10, column=1)

label_nueva_carrera = tk.Label(root, text="Nueva Carrera:")
label_nueva_carrera.grid(row=11, column=0)
entry_nueva_carrera = tk.Entry(root)
entry_nueva_carrera.grid(row=11, column=1)

button_modificar_estudiante = tk.Button(root, text="Modificar Estudiante", command=modificar_estudiante)
button_modificar_estudiante.grid(row=12, column=0, columnspan=2)

# Para modificar materias
label_codigo_modificar = tk.Label(root, text="Código:")
label_codigo_modificar.grid(row=8, column=2)
entry_codigo_modificar = tk.Entry(root)
entry_codigo_modificar.grid(row=8, column=3)

label_nuevo_nombre_materia = tk.Label(root, text="Nuevo Nombre:")
label_nuevo_nombre_materia.grid(row=9, column=2)
entry_nuevo_nombre_materia = tk.Entry(root)
entry_nuevo_nombre_materia.grid(row=9, column=3)

label_nuevos_creditos = tk.Label(root, text="Nuevos Créditos:")
label_nuevos_creditos.grid(row=10, column=2)
entry_nuevos_creditos = tk.Entry(root)
entry_nuevos_creditos.grid(row=10, column=3)

button_modificar_materia = tk.Button(root, text="Modificar Materia", command=modificar_materia)
button_modificar_materia.grid(row=11, column=2, columnspan=2)

# Crear un widget de texto para mostrar la salida
text_output = tk.Text(root, width=80, height=20)
text_output.grid(row=13, column=0, columnspan=6)

# Mostrar toda la información inicial
mostrar_toda_informacion()

# Ejecutar el bucle principal
root.mainloop()
