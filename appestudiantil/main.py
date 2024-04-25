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



# # Lista para almacenar estudiantes
# estudiantes = []

# # Lista para almacenar materias
# materias = []

# # Lista para almacenar notas
# notas = []

# # Función para agregar un nuevo estudiante
# def agregar_estudiante():
#     id_estudiante = entry_id_estudiante.get()
#     nombre_completo = entry_nombre_completo.get()
#     fecha_nacimiento = entry_fecha_nacimiento.get()
#     carrera = entry_carrera.get()

#     if not (id_estudiante and nombre_completo and fecha_nacimiento and carrera):
#         show_message("Por favor, complete todos los campos.")
#         return

#     nuevo_estudiante = Estudiante(id_estudiante, nombre_completo, fecha_nacimiento, carrera)
#     estudiantes.append(nuevo_estudiante)
#     show_message("Estudiante agregado correctamente.")
#     mostrar_toda_informacion()

# # Función para agregar una nueva materia
# def agregar_materia():
#     id_estudiante = entry_id_estudiante_materia.get()
#     codigo = entry_codigo.get()
#     nombre = entry_nombre.get()
#     num_creditos = entry_num_creditos.get()

#     if not (id_estudiante and codigo and nombre and num_creditos):
#         show_message("Por favor, complete todos los campos.")
#         return

#     nueva_materia = Materia(codigo, nombre, num_creditos)
#     for estudiante in estudiantes:
#         if estudiante.id_estudiante == id_estudiante:
#             estudiante.materias.append(nueva_materia)
#             materias.append(nueva_materia)
#             show_message("Materia agregada correctamente.")
#             mostrar_toda_informacion()
#             return

#     show_message("ID de estudiante no encontrado.")

# # Función para agregar una nueva nota
# def agregar_nota():
#     id_nota = entry_id_nota.get()
#     nombre = entry_nombre_nota.get()
#     puntaje = entry_puntaje.get()
#     id_materia = entry_id_materia.get()
#     id_grupo = entry_id_grupo.get()

#     if not (id_nota and nombre and puntaje and id_materia and id_grupo):
#         show_message("Por favor, complete todos los campos.")
#         return

#     nueva_nota = Nota(id_nota, nombre, puntaje, id_materia, id_grupo)
#     for materia in materias:
#         if materia.codigo == id_materia:
#             materia.notas.append(nueva_nota)
#             notas.append(nueva_nota)
#             show_message("Nota agregada correctamente.")
#             mostrar_toda_informacion()
#             return

#     show_message("Código de materia no encontrado.")

# # Función para eliminar un estudiante
# def eliminar_estudiante():
#     id_estudiante = entry_id_estudiante_eliminar.get()

#     if not id_estudiante:
#         show_message("Por favor, ingrese el ID del estudiante a eliminar.")
#         return

#     for estudiante in estudiantes:
#         if estudiante.id_estudiante == id_estudiante:
#             estudiantes.remove(estudiante)
#             show_message("Estudiante eliminado correctamente.")
#             mostrar_toda_informacion()
#             return

#     show_message("ID de estudiante no encontrado.")

# # Función para eliminar una materia
# def eliminar_materia():
#     codigo = entry_codigo_eliminar.get()

#     if not codigo:
#         show_message("Por favor, ingrese el código de la materia a eliminar.")
#         return

#     for materia in materias:
#         if materia.codigo == codigo:
#             materias.remove(materia)
#             for estudiante in estudiantes:
#                 for mat in estudiante.materias:
#                     if mat.codigo == codigo:
#                         estudiante.materias.remove(mat)
#                         show_message("Materia eliminada correctamente.")
#                         mostrar_toda_informacion()
#                         return

#     show_message("Código de materia no encontrado.")

# # Función para eliminar una nota
# def eliminar_nota():
#     nombre_nota = entry_nombre_nota_eliminar.get()
#     id_materia = entry_id_materia_eliminar.get()

#     if not (nombre_nota and id_materia):
#         show_message("Por favor, ingrese el nombre de la nota y el ID de la materia.")
#         return

#     for nota in notas:
#         if nota.nombre == nombre_nota and nota.id_materia == id_materia:
#             notas.remove(nota)
#             for materia in materias:
#                 if materia.codigo == id_materia:
#                     for nt in materia.notas:
#                         if nt.nombre == nombre_nota:
#                             materia.notas.remove(nt)
#                             show_message("Nota eliminada correctamente.")
#                             mostrar_toda_informacion()
#                             return

#     show_message("Nota no encontrada.")

# # Función para modificar un estudiante
# def modificar_estudiante():
#     id_estudiante = entry_id_estudiante_modificar.get()
#     nuevo_nombre = entry_nuevo_nombre_estudiante.get()
#     nueva_fecha_nacimiento = entry_nueva_fecha_nacimiento.get()
#     nueva_carrera = entry_nueva_carrera.get()

#     if not id_estudiante:
#         show_message("Por favor, ingrese el ID del estudiante a modificar.")
#         return

#     for estudiante in estudiantes:
#         if estudiante.id_estudiante == id_estudiante:
#             if nuevo_nombre:
#                 estudiante.nombre_completo = nuevo_nombre
#             if nueva_fecha_nacimiento:
#                 estudiante.fecha_nacimiento = nueva_fecha_nacimiento
#             if nueva_carrera:
#                 estudiante.carrera = nueva_carrera
#             show_message("Datos del estudiante modificados correctamente.")
#             mostrar_toda_informacion()
#             return

#     show_message("ID de estudiante no encontrado.")

# # Función para modificar una materia
# def modificar_materia():
#     codigo = entry_codigo_modificar.get()
#     nuevo_nombre = entry_nuevo_nombre_materia.get()
#     nuevos_creditos = entry_nuevos_creditos.get()

#     if not codigo or not (nuevo_nombre or nuevos_creditos):
#         show_message("Por favor, ingrese el código de la materia y al menos uno de los campos a modificar.")
#         return

#     try:
#         # Crear una instancia de la clase conexionpg con los argumentos requeridos
#         conexion = conexionpg()
#         # Crear una instancia del cursor con la conexion
#         cursor = conexion.cursor()

#         # Verificar si se desea modificar el nombre de la materia
#         if nuevo_nombre:
#             # Ejecutar la consulta para actualizar el nombre de la materia
#             cursor.execute("UPDATE materia SET nombre = %s WHERE codigo = %s", (nuevo_nombre, codigo))

#         # Verificar si se desea modificar los créditos de la materia
#         if nuevos_creditos:
#             # Ejecutar la consulta para actualizar los créditos de la materia
#             cursor.execute("UPDATE materia SET num_creditos = %s WHERE codigo = %s", (nuevos_creditos, codigo))

#         # Confirmar la transacción
#         conexion.commit()

#         # Cerrar el cursor y la conexion
#         cursor.close()
#         conexion.close()

#         # Mostrar mensaje de éxito
#         show_message("Materia modificada correctamente.")
#         mostrar_toda_informacion()

#     except (Exception, psycopg2.Error) as error:
#         # Mostrar mensaje de error
#         show_message(f"Error al modificar la materia: {error}")

# # Función para mostrar toda la información
# def mostrar_toda_informacion():
#     text_output.delete('1.0', tk.END)
#     text_output.insert(tk.END, "Estudiantes:\n")
#     for estudiante in estudiantes:
#         text_output.insert(tk.END, f"ID: {estudiante.id_estudiante}, Nombre: {estudiante.nombre_completo}, "
#                                     f"Fecha de Nacimiento: {estudiante.fecha_nacimiento}, Carrera: {estudiante.carrera}\n")
#         text_output.insert(tk.END, "Materias:\n")
#         for materia in estudiante.materias:
#             text_output.insert(tk.END, f"Código: {materia.codigo}, Nombre: {materia.nombre}, "
#                                         f"Número de Créditos: {materia.num_creditos}\n")
#             text_output.insert(tk.END, "Notas:\n")
#             for nota in materia.notas:
#                 text_output.insert(tk.END, f"ID Nota: {nota.id_nota}, Nombre: {nota.nombre}, "
#                                             f"Puntaje: {nota.puntaje}, ID Materia: {nota.id_materia}, ID Grupo: {nota.id_grupo}\n")
#     text_output.insert(tk.END, "\nMaterias:\n")
#     for materia in materias:
#         text_output.insert(tk.END, f"Código: {materia.codigo}, Nombre: {materia.nombre}, "
#                                     f"Número de Créditos: {materia.num_creditos}\n")
#         text_output.insert(tk.END, "Notas:\n")
#         for nota in materia.notas:
#             text_output.insert(tk.END, f"ID Nota: {nota.id_nota}, Nombre: {nota.nombre}, "
#                                         f"Puntaje: {nota.puntaje}, ID Materia: {nota.id_materia}, ID Grupo: {nota.id_grupo}\n")

# # Función para mostrar un mensaje
# def show_message(message):
#     messagebox.showinfo("Mensaje", message)

# # Función para mostrar los campos correspondientes al menú de Estudiantes
# def mostrar_campos_estudiantes():
#     hide_all_fields()
#     label_id_estudiante.grid(row=0, column=0)
#     entry_id_estudiante.grid(row=0, column=1)
#     label_nombre_completo.grid(row=1, column=0)
#     entry_nombre_completo.grid(row=1, column=1)
#     label_fecha_nacimiento.grid(row=2, column=0)
#     entry_fecha_nacimiento.grid(row=2, column=1)
#     label_carrera.grid(row=3, column=0)
#     entry_carrera.grid(row=3, column=1)
#     button_agregar_estudiante.grid(row=4, column=0, columnspan=2)

# # Función para mostrar los campos correspondientes al menú de Materias
# def mostrar_campos_materias():
#     hide_all_fields()
#     label_id_estudiante_materia.grid(row=0, column=2)
#     entry_id_estudiante_materia.grid(row=0, column=3)
#     label_codigo.grid(row=1, column=2)
#     entry_codigo.grid(row=1, column=3)
#     label_nombre.grid(row=2, column=2)
#     entry_nombre.grid(row=2, column=3)
#     label_num_creditos.grid(row=3, column=2)
#     entry_num_creditos.grid(row=3, column=3)
#     button_agregar_materia.grid(row=4, column=2, columnspan=2)

# # Función para mostrar los campos correspondientes al menú de Notas
# def mostrar_campos_notas():
#     hide_all_fields()
#     label_id_nota.grid(row=0, column=4)
#     entry_id_nota.grid(row=0, column=5)
#     label_nombre_nota.grid(row=1, column=4)
#     entry_nombre_nota.grid(row=1, column=5)
#     label_puntaje.grid(row=2, column=4)
#     entry_puntaje.grid(row=2, column=5)
#     label_id_materia.grid(row=3, column=4)
#     entry_id_materia.grid(row=3, column=5)
#     label_id_grupo.grid(row=4, column=4)
#     entry_id_grupo.grid(row=4, column=5)
#     button_agregar_nota.grid(row=5, column=4, columnspan=2)

# # Función para ocultar todos los campos
# def hide_all_fields():
#     for widget in root.winfo_children():
#         if isinstance(widget, tk.Entry) or isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
#             widget.grid_remove()

# # Crear la ventana principal
# root = tk.Tk()
# root.title("Sistema de Gestión Académica")

# # Crear los menús
# menubar = tk.Menu(root)
# estudiante_menu = tk.Menu(menubar, tearoff=0)
# estudiante_menu.add_command(label="Agregar Estudiante", command=mostrar_campos_estudiantes)
# estudiante_menu.add_command(label="Eliminar Estudiante", command=eliminar_estudiante)
# estudiante_menu.add_command(label="Modificar Estudiante", command=modificar_estudiante)
# menubar.add_cascade(label="Estudiantes", menu=estudiante_menu)

# materia_menu = tk.Menu(menubar, tearoff=0)
# materia_menu.add_command(label="Agregar Materia", command=mostrar_campos_materias)
# materia_menu.add_command(label="Eliminar Materia", command=eliminar_materia)
# materia_menu.add_command(label="Modificar Materia", command=modificar_materia)
# menubar.add_cascade(label="Materias", menu=materia_menu)

# nota_menu = tk.Menu(menubar, tearoff=0)
# nota_menu.add_command(label="Agregar Nota", command=mostrar_campos_notas)
# nota_menu.add_command(label="Eliminar Nota", command=eliminar_nota)
# menubar.add_cascade(label="Notas", menu=nota_menu)

# root.config(menu=menubar)

# # Crear un widget de texto para mostrar la información
# text_output = tk.Text(root, height=20, width=80)
# text_output.grid(row=1, column=0, columnspan=6)

# # Iniciar el bucle de eventos
# root.mainloop()
