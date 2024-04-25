# import psycopg2

# class Estudiante:
#     def __init__(self, id_estudiante, nombre_completo, fecha_nacimiento, carrera):
#         self.id_estudiante = id_estudiante
#         self.nombre_completo = nombre_completo
#         self.fecha_nacimiento = fecha_nacimiento
#         self.carrera = carrera
#         self.materias = []

# class Materia:
#     def __init__(self, codigo, nombre, num_creditos):
#         self.codigo = codigo
#         self.nombre = nombre
#         self.num_creditos = num_creditos
#         self.notas = []
# class Nota:
#     def __init__(self, id_nota, nombre, puntaje, codigo_materia, id_estudiante):
#         self.id_nota = id_nota
#         self.nombre = nombre
#         self.puntaje = puntaje
#         self.codigo_materia = codigo_materia
#         self.id_estudiante = id_estudiante

# def crear_estudiante():
#     id_estudiante = int(input("Ingrese el ID del estudiante: "))
#     nombre_completo = input("Ingrese el nombre completo del estudiante: ")
#     fecha_nacimiento = input("Ingrese la fecha de nacimiento del estudiante (YYYY-MM-DD): ")
#     carrera = input("Ingrese la carrera del estudiante: ")

#     try:
#         cursor.execute("INSERT INTO Estudiante (id_estudiante, nombre_completo, fecha_nacimiento, carrera) VALUES (%s, %s, %s, %s)",
#                        (id_estudiante, nombre_completo, fecha_nacimiento, carrera))
#         conexion.commit()
#         print("Estudiante creado con éxito. ID:", id_estudiante)
#     except psycopg2.Error as e:
#         conexion.rollback()
#         print("Error al crear estudiante:", e)

# def crear_materia():
#     nombre = input("Ingrese el nombre de la materia: ")
#     num_creditos = int(input("Ingrese el número de créditos de la materia: "))

#     try:
#         cursor.execute("INSERT INTO Materia (nombre, num_creditos) VALUES (%s, %s) RETURNING codigo",
#                        (nombre, num_creditos))
#         codigo = cursor.fetchone()[0]
#         conexion.commit()
#         print("Materia creada con éxito. Código:", codigo)
#     except psycopg2.Error as e:
#         conexion.rollback()
#         print("Error al crear materia:", e)

# def crear_nota():
#     nombre_nota = input("Ingrese el nombre de la nota: ")
#     puntaje = float(input("Ingrese el puntaje de la nota: "))
#     codigo_materia = int(input("Ingrese el código de la materia: "))
#     id_estudiante = int(input("Ingrese el ID del estudiante: "))

#     try:
#         cursor.execute("INSERT INTO Notas (nombre_nota, puntaje, codigo_materia, id_estudiante) VALUES (%s, %s, %s, %s)",
#                        (nombre_nota, puntaje, codigo_materia, id_estudiante))
#         conexion.commit()
#         print("Nota creada con éxito.")
#     except psycopg2.Error as e:
#         conexion.rollback()
#         print("Error al crear nota:", e)

# def ver_estudiantes():
#     try:
#         cursor.execute("SELECT * FROM Estudiante")
#         estudiantes = cursor.fetchall()
#         if not estudiantes:
#             print("No hay estudiantes registrados.")
#         else:
#             print("Lista de estudiantes registrados:")
#             for estudiante in estudiantes:
#                 print(f"ID: {estudiante[0]}, Nombre completo: {estudiante[1]}, Fecha de nacimiento: {estudiante[2]}, Carrera: {estudiante[3]}")
#     except psycopg2.Error as e:
#         print("Error al recuperar la lista de estudiantes:", e)

# def ver_materias_estudiante():
#     id_estudiante = int(input("Ingrese el ID del estudiante: "))
#     try:
#         cursor.execute("SELECT m.nombre FROM Materia m INNER JOIN Estudiante_Materia em ON m.codigo = em.codigo_materia WHERE em.id_estudiante = %s", (id_estudiante,))
#         materias = cursor.fetchall()
#         if not materias:
#             print("El estudiante no está inscrito en ninguna materia.")
#         else:
#             print("Materias en las que está inscrito el estudiante:")
#             for materia in materias:
#                 print(materia[0])
#     except psycopg2.Error as e:
#         print("Error al recuperar las materias del estudiante:", e)

# def ver_notas_estudiante_materia():
#     id_estudiante = int(input("Ingrese el ID del estudiante: "))
#     codigo_materia = int(input("Ingrese el código de la materia: "))
#     try:
#         cursor.execute("SELECT nombre_nota, puntaje FROM Notas WHERE id_estudiante = %s AND codigo_materia = %s", (id_estudiante, codigo_materia))
#         notas = cursor.fetchall()
#         if not notas:
#             print("El estudiante no tiene notas registradas en esta materia.")
#         else:
#             print("Notas del estudiante en la materia:")
#             for nota in notas:
#                 print(f"{nota[0]}: {nota[1]}")
#     except psycopg2.Error as e:
#         print("Error al recuperar las notas del estudiante en la materia:", e)

# def calcular_promedio_notas_estudiante_materia():
#     id_estudiante = int(input("Ingrese el ID del estudiante: "))
#     codigo_materia = int(input("Ingrese el código de la materia: "))
#     try:
#         cursor.execute("SELECT AVG(puntaje) FROM Notas WHERE id_estudiante = %s AND codigo_materia = %s", (id_estudiante, codigo_materia))
#         promedio = cursor.fetchone()[0]
#         if promedio is None:
#             print("El estudiante no tiene notas registradas en esta materia.")
#         else:
#             print(f"El promedio de notas del estudiante en la materia es: {promedio}")
#     except psycopg2.Error as e:
#         print("Error al calcular el promedio de notas del estudiante en la materia:", e)

# def actualizar_estudiante():
#     id_estudiante = int(input("Ingrese el ID del estudiante que desea actualizar: "))
#     nombre_completo = input("Ingrese el nuevo nombre completo del estudiante: ")
#     fecha_nacimiento = input("Ingrese la nueva fecha de nacimiento del estudiante (YYYY-MM-DD): ")
#     carrera = input("Ingrese la nueva carrera del estudiante: ")

#     try:
#         cursor.execute("UPDATE Estudiante SET nombre_completo = %s, fecha_nacimiento = %s, carrera = %s WHERE id_estudiante = %s",
#                        (nombre_completo, fecha_nacimiento, carrera, id_estudiante))
#         conexion.commit()
#         print("Información del estudiante actualizada con éxito.")
#     except psycopg2.Error as e:
#         conexion.rollback()
#         print("Error al actualizar la información del estudiante:", e)

# def actualizar_materia():
#     codigo_materia = int(input("Ingrese el código de la materia que desea actualizar: "))
#     nombre = input("Ingrese el nuevo nombre de la materia: ")
#     num_creditos = int(input("Ingrese el nuevo número de créditos de la materia: "))

#     try:
#         cursor.execute("UPDATE Materia SET nombre = %s, num_creditos = %s WHERE codigo = %s",
#                        (nombre, num_creditos, codigo_materia))
#         conexion.commit()
#         print("Información de la materia actualizada con éxito.")
#     except psycopg2.Error as e:
#         conexion.rollback()
#         print("Error al actualizar la información de la materia:", e)


# def eliminar_estudiante():
#     id_estudiante = int(input("Ingrese el ID del estudiante que desea eliminar: "))
#     try:
#         cursor.execute("DELETE FROM Estudiante WHERE id_estudiante = %s", (id_estudiante,))
#         conexion.commit()
#         print("Estudiante eliminado con éxito.")
#     except psycopg2.Error as e:
#         conexion.rollback()
#         print("Error al eliminar el estudiante:", e)


# def eliminar_materia():
#     codigo_materia = int(input("Ingrese el código de la materia que desea eliminar: "))
#     try:
      
#         cursor.execute("select * from estudiante_materia WHERE id = %s", (codigo_materia,))
#         cursor.execute("SELECT * FROM Materia WHERE codigo = %s", (codigo_materia,))
#         materia = cursor.fetchone()
#         if not materia:
#             print("La materia que desea eliminar no existe.")
#         else:
            
#             cursor.execute("DELETE FROM estudiante_materia WHERE id = %s", (codigo_materia,))
#             cursor.execute("DELETE FROM Materia WHERE codigo = %s", (codigo_materia,))
#             conexion.commit()
#             print("Materia eliminada con éxito.")
#     except psycopg2.Error as e:
#         conexion.rollback()
#         print("Error al eliminar la materia:", e)



# def mostrar_menu():
#     print("\nMenú:")
#     print("1. Crear estudiante")
#     print("2. Crear materia")
#     print("3. Crear nota")
#     print("4. Ver lista de estudiantes")
#     print("5. Ver materias de un estudiante")
#     print("6. Ver notas de un estudiante en una materia")
#     print("7. Calcular promedio de notas de un estudiante en una materia")
#     print("8. Actualizar información de un estudiante")
#     print("9. Actualizar información de una materia")
#     print("10. Eliminar estudiante")
#     print("11. Eliminar materia")
#     print("12. Salir")


# try:
#     conexion = psycopg2.connect(
#         dbname="registroestudiantil",
#         user="postgres",
#         password="123456789",
#         host="localhost",
#         port="5432"
#     )
#     print("Conexión exitosa.")
#     cursor = conexion.cursor()

   
#     while True:
#         mostrar_menu()
#         opcion = input("Seleccione una opción: ")

#         if opcion == "1":
#             crear_estudiante()
#         elif opcion == "2":
#             crear_materia()
#         elif opcion == "3":
#             crear_nota()
#         elif opcion == "4":
#             ver_estudiantes()
#         elif opcion == "5":
#             ver_materias_estudiante()
#         elif opcion == "6":
#             ver_notas_estudiante_materia()
#         elif opcion == "7":
#             calcular_promedio_notas_estudiante_materia()
#         elif opcion == "8":
#             actualizar_estudiante()
#         elif opcion == "9":
#             actualizar_materia()
#         elif opcion == "10":
#             eliminar_estudiante()
#         elif opcion == "11":
#             eliminar_materia()
#         elif opcion == "12":
#             print("Saliendo del programa...")
#             break
#         else:
#             print("Opción no válida. Por favor, seleccione una opción válida.")

#     cursor.close()
#     conexion.close()

# except psycopg2.Error as e:
#     print("Error al conectar a la base de datos:", e)

import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2

conexion = psycopg2.connect(
    dbname="registroestudiantil",
    user="postgres",
    password="123456789",
    host="localhost",
    port="5432"
)
cursor = conexion.cursor()

class Aplicacion:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Registro Estudiantil")

        self.menu_principal = tk.Menu(ventana)
        ventana.config(menu=self.menu_principal)

        self.menu_estudiantes = tk.Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Estudiantes", menu=self.menu_estudiantes)
        self.menu_estudiantes.add_command(label="Agregar Estudiante", command=self.crear_estudiante)
        self.menu_estudiantes.add_command(label="Ver Estudiantes", command=self.ver_estudiantes)
        self.menu_estudiantes.add_command(label="Eliminar Estudiante", command=self.eliminar_estudiante)

        self.menu_materias = tk.Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Materias", menu=self.menu_materias)
        self.menu_materias.add_command(label="Agregar Materia", command=self.crear_materia)
        self.menu_materias.add_command(label="Eliminar Materia", command=self.eliminar_materia)

        self.menu_notas = tk.Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Notas", menu=self.menu_notas)
        self.menu_notas.add_command(label="Agregar Nota", command=self.crear_nota)
        self.menu_notas.add_command(label="Calcular Promedio", command=self.calcular_promedio_notas_estudiante_materia)

    def crear_estudiante(self):
        ventana_agregar_estudiante = tk.Toplevel(self.ventana)
        ventana_agregar_estudiante.title("Agregar Estudiante")
        
        lbl_id_estudiante = tk.Label(ventana_agregar_estudiante, text="ID del estudiante:")
        lbl_id_estudiante.grid(row=0, column=0)
        entry_id_estudiante = tk.Entry(ventana_agregar_estudiante)
        entry_id_estudiante.grid(row=0, column=1)

        lbl_nombre_completo = tk.Label(ventana_agregar_estudiante, text="Nombre completo:")
        lbl_nombre_completo.grid(row=1, column=0)
        entry_nombre_completo = tk.Entry(ventana_agregar_estudiante)
        entry_nombre_completo.grid(row=1, column=1)

        lbl_fecha_nacimiento = tk.Label(ventana_agregar_estudiante, text="Fecha de nacimiento (YYYY-MM-DD):")
        lbl_fecha_nacimiento.grid(row=2, column=0)
        entry_fecha_nacimiento = tk.Entry(ventana_agregar_estudiante)
        entry_fecha_nacimiento.grid(row=2, column=1)

        lbl_carrera = tk.Label(ventana_agregar_estudiante, text="Carrera:")
        lbl_carrera.grid(row=3, column=0)
        entry_carrera = tk.Entry(ventana_agregar_estudiante)
        entry_carrera.grid(row=3, column=1)

        def guardar_estudiante():
            id_estudiante = int(entry_id_estudiante.get())
            nombre_completo = entry_nombre_completo.get()
            fecha_nacimiento = entry_fecha_nacimiento.get()
            carrera = entry_carrera.get()

            try:
                cursor.execute("INSERT INTO Estudiante (id_estudiante, nombre_completo, fecha_nacimiento, carrera) VALUES (%s, %s, %s, %s)",
                               (id_estudiante, nombre_completo, fecha_nacimiento, carrera))
                conexion.commit()
                messagebox.showinfo("Agregar Estudiante", "Estudiante creado con éxito.")
            except psycopg2.Error as e:
                conexion.rollback()
                messagebox.showerror("Error", f"Error al crear estudiante: {e}")

        btn_guardar_estudiante = tk.Button(ventana_agregar_estudiante, text="Guardar", command=guardar_estudiante)
        btn_guardar_estudiante.grid(row=4, column=0, columnspan=2)

    def crear_materia(self):
        ventana_agregar_materia = tk.Toplevel(self.ventana)
        ventana_agregar_materia.title("Agregar Materia")
        
        lbl_nombre = tk.Label(ventana_agregar_materia, text="Nombre de la materia:")
        lbl_nombre.grid(row=0, column=0)
        entry_nombre = tk.Entry(ventana_agregar_materia)
        entry_nombre.grid(row=0, column=1)

        lbl_num_creditos = tk.Label(ventana_agregar_materia, text="Número de créditos:")
        lbl_num_creditos.grid(row=1, column=0)
        entry_num_creditos = tk.Entry(ventana_agregar_materia)
        entry_num_creditos.grid(row=1, column=1)

        def guardar_materia():
            nombre = entry_nombre.get()
            num_creditos = int(entry_num_creditos.get())

            try:
                cursor.execute("INSERT INTO Materia (nombre, num_creditos) VALUES (%s, %s) RETURNING codigo",
                               (nombre, num_creditos))
                codigo = cursor.fetchone()[0]
                conexion.commit()
                messagebox.showinfo("Agregar Materia", f"Materia creada con éxito. Código: {codigo}")
            except psycopg2.Error as e:
                conexion.rollback()
                messagebox.showerror("Error", f"Error al crear materia: {e}")

        btn_guardar_materia = tk.Button(ventana_agregar_materia, text="Guardar", command=guardar_materia)
        btn_guardar_materia.grid(row=2, column=0, columnspan=2)

    def crear_nota(self):
        ventana_agregar_nota = tk.Toplevel(self.ventana)
        ventana_agregar_nota.title("Agregar Nota")
        
        lbl_nombre_nota = tk.Label(ventana_agregar_nota, text="Nombre de la nota:")
        lbl_nombre_nota.grid(row=0, column=0)
        entry_nombre_nota = tk.Entry(ventana_agregar_nota)
        entry_nombre_nota.grid(row=0, column=1)

        lbl_puntaje = tk.Label(ventana_agregar_nota, text="Puntaje:")
        lbl_puntaje.grid(row=1, column=0)
        entry_puntaje = tk.Entry(ventana_agregar_nota)
        entry_puntaje.grid(row=1, column=1)

        lbl_materia = tk.Label(ventana_agregar_nota, text="Materia:")
        lbl_materia.grid(row=2, column=0)
        combo_materia = ttk.Combobox(ventana_agregar_nota)
        cursor.execute("SELECT codigo, nombre FROM Materia")
        materias = cursor.fetchall()
        combo_materia['values'] = [f"{materia[0]} - {materia[1]}" for materia in materias]
        combo_materia.grid(row=2, column=1)

        lbl_estudiante = tk.Label(ventana_agregar_nota, text="Estudiante:")
        lbl_estudiante.grid(row=3, column=0)
        combo_estudiante = ttk.Combobox(ventana_agregar_nota)
        cursor.execute("SELECT id_estudiante, nombre_completo FROM Estudiante")
        estudiantes = cursor.fetchall()
        combo_estudiante['values'] = [f"{estudiante[0]} - {estudiante[1]}" for estudiante in estudiantes]
        combo_estudiante.grid(row=3, column=1)

        def guardar_nota():
            nombre_nota = entry_nombre_nota.get()
            puntaje = float(entry_puntaje.get())
            seleccion_materia = combo_materia.get()
            seleccion_estudiante = combo_estudiante.get()

            # Extraer el ID de materia y estudiante de la selección
            codigo_materia = int(seleccion_materia.split('-')[0].strip())
            id_estudiante = int(seleccion_estudiante.split('-')[0].strip())

            try:
                cursor.execute("INSERT INTO Notas (nombre_nota, puntaje, codigo_materia, id_estudiante) VALUES (%s, %s, %s, %s)",
                               (nombre_nota, puntaje, codigo_materia, id_estudiante))
                conexion.commit()
                messagebox.showinfo("Agregar Nota", "Nota creada con éxito.")
            except psycopg2.Error as e:
                conexion.rollback()
                messagebox.showerror("Error", f"Error al crear nota: {e}")

        btn_guardar_nota = tk.Button(ventana_agregar_nota, text="Guardar", command=guardar_nota)
        btn_guardar_nota.grid(row=4, column=0, columnspan=2)

    def ver_estudiantes(self):
        try:
            cursor.execute("SELECT * FROM Estudiante")
            estudiantes = cursor.fetchall()
            if not estudiantes:
                messagebox.showinfo("Ver Estudiantes", "No hay estudiantes registrados.")
            else:
                mensaje = "Lista de estudiantes registrados:\n"
                for estudiante in estudiantes:
                    mensaje += f"ID: {estudiante[0]}, Nombre completo: {estudiante[1]}, Fecha de nacimiento: {estudiante[2]}, Carrera: {estudiante[3]}\n"
                messagebox.showinfo("Ver Estudiantes", mensaje)
        except psycopg2.Error as e:
            messagebox.showerror("Error", f"Error al recuperar la lista de estudiantes: {e}")

    def eliminar_estudiante(self):
        ventana_eliminar_estudiante = tk.Toplevel(self.ventana)
        ventana_eliminar_estudiante.title("Eliminar Estudiante")
        
        lbl_id_estudiante = tk.Label(ventana_eliminar_estudiante, text="ID del estudiante:")
        lbl_id_estudiante.grid(row=0, column=0)
        entry_id_estudiante = tk.Entry(ventana_eliminar_estudiante)
        entry_id_estudiante.grid(row=0, column=1)

        def eliminar_estudiante():
            id_estudiante = int(entry_id_estudiante.get())

            try:
                cursor.execute("DELETE FROM Estudiante WHERE id_estudiante = %s", (id_estudiante,))
                conexion.commit()
                messagebox.showinfo("Eliminar Estudiante", "Estudiante eliminado con éxito.")
            except psycopg2.Error as e:
                conexion.rollback()
                messagebox.showerror("Error", f"Error al eliminar estudiante: {e}")

        btn_eliminar_estudiante = tk.Button(ventana_eliminar_estudiante, text="Eliminar", command=eliminar_estudiante)
        btn_eliminar_estudiante.grid(row=1, column=0, columnspan=2)

    def eliminar_materia(self):
        ventana_eliminar_materia = tk.Toplevel(self.ventana)
        ventana_eliminar_materia.title("Eliminar Materia")
        
        lbl_codigo_materia = tk.Label(ventana_eliminar_materia, text="Código de la materia:")
        lbl_codigo_materia.grid(row=0, column=0)
        entry_codigo_materia = tk.Entry(ventana_eliminar_materia)
        entry_codigo_materia.grid(row=0, column=1)

        def eliminar_materia():
            codigo_materia = int(entry_codigo_materia.get())

            try:
                cursor.execute("DELETE FROM Materia WHERE codigo = %s", (codigo_materia,))
                conexion.commit()
                messagebox.showinfo("Eliminar Materia", "Materia eliminada con éxito.")
            except psycopg2.Error as e:
                conexion.rollback()
                messagebox.showerror("Error", f"Error al eliminar materia: {e}")

        btn_eliminar_materia = tk.Button(ventana_eliminar_materia, text="Eliminar", command=eliminar_materia)
        btn_eliminar_materia.grid(row=1, column=0, columnspan=2)

    def calcular_promedio_notas_estudiante_materia(self):
        ventana_calcular_promedio = tk.Toplevel(self.ventana)
        ventana_calcular_promedio.title("Calcular Promedio de Notas")

        lbl_estudiante = tk.Label(ventana_calcular_promedio, text="Seleccione el estudiante:")
        lbl_estudiante.grid(row=0, column=0)
        combo_estudiante = ttk.Combobox(ventana_calcular_promedio)
        cursor.execute("SELECT id_estudiante, nombre_completo FROM Estudiante")
        estudiantes = cursor.fetchall()
        combo_estudiante['values'] = [f"{estudiante[0]} - {estudiante[1]}" for estudiante in estudiantes]
        combo_estudiante.grid(row=0, column=1)

        lbl_materia = tk.Label(ventana_calcular_promedio, text="Seleccione la materia:")
        lbl_materia.grid(row=1, column=0)
        combo_materia = ttk.Combobox(ventana_calcular_promedio)
        cursor.execute("SELECT codigo, nombre FROM Materia")
        materias = cursor.fetchall()
        combo_materia['values'] = [f"{materia[0]} - {materia[1]}" for materia in materias]
        combo_materia.grid(row=1, column=1)

        lbl_promedio = tk.Label(ventana_calcular_promedio, text="Promedio de Notas:")
        lbl_promedio.grid(row=2, column=0)
        entry_promedio = tk.Entry(ventana_calcular_promedio, state='readonly')
        entry_promedio.grid(row=2, column=1)

        def calcular_promedio():
            seleccion_estudiante = combo_estudiante.get()
            seleccion_materia = combo_materia.get()

            # Extraer el ID de estudiante y materia de la selección
            id_estudiante = int(seleccion_estudiante.split('-')[0].strip())
            codigo_materia = int(seleccion_materia.split('-')[0].strip())

            try:
                cursor.execute("SELECT AVG(puntaje) FROM Notas WHERE id_estudiante = %s AND codigo_materia = %s",
                               (id_estudiante, codigo_materia))
                promedio = cursor.fetchone()[0]
                if promedio:
                    entry_promedio.config(state='normal')
                    entry_promedio.delete(0, tk.END)
                    entry_promedio.insert(0, f"{promedio:.2f}")
                    entry_promedio.config(state='readonly')
                else:
                    entry_promedio.config(state='normal')
                    entry_promedio.delete(0, tk.END)
                    entry_promedio.insert(0, "N/A")
                    entry_promedio.config(state='readonly')
            except psycopg2.Error as e:
                messagebox.showerror("Error", f"Error al calcular promedio: {e}")

        btn_calcular_promedio = tk.Button(ventana_calcular_promedio, text="Calcular", command=calcular_promedio)
        btn_calcular_promedio.grid(row=3, column=0, columnspan=2)

def main():
    ventana_principal = tk.Tk()
    app = Aplicacion(ventana_principal)
    ventana_principal.mainloop()

if __name__ == "__main__":
    main()

conexion.close()
