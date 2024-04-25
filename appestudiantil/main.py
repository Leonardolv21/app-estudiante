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


class Estudiante:
    def __init__(self, id_estudiante, nombre_completo, fecha_nacimiento, carrera):
        self.id_estudiante = id_estudiante
        self.nombre_completo = nombre_completo
        self.fecha_nacimiento = fecha_nacimiento
        self.carrera = carrera
        self.materias = []
        
class Materia:
    def __init__(self, codigo, nombre, num_creditos):
        self.codigo = codigo
        self.nombre = nombre
        self.num_creditos = num_creditos
        self.notas = []
class Nota:
    def __init__(self, id_nota, nombre, puntaje, codigo_materia, id_estudiante):
        self.id_nota = id_nota
        self.nombre = nombre
        self.puntaje = puntaje
        self.codigo_materia = codigo_materia
        self.id_estudiante = id_estudiante


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
        self.menu_estudiantes.add_command(label="Actualizar Estudiante", command=self.actualizar_estudiante)

        self.menu_materias = tk.Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Materias", menu=self.menu_materias)
        self.menu_materias.add_command(label="Agregar Materia", command=self.crear_materia)
        self.menu_materias.add_command(label="Eliminar Materia", command=self.eliminar_materia)
        self.menu_materias.add_command(label="Actualizar Materia", command=self.actualizar_materia)

        self.menu_notas = tk.Menu(self.menu_principal, tearoff=0)
        self.menu_principal.add_cascade(label="Notas", menu=self.menu_notas)
        self.menu_notas.add_command(label="Agregar Nota", command=self.crear_nota)
        self.menu_notas.add_command(label="Calcular Promedio", command=self.calcular_promedio_notas_estudiante_materia)
        self.menu_notas.add_command(label="Ver Materias de Estudiante", command=self.ver_materias_estudiante)
        self.menu_notas.add_command(label="Ver Notas de Estudiante en Materia", command=self.ver_notas_estudiante_materia)

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

    def actualizar_estudiante(self):
        ventana_actualizar_estudiante = tk.Toplevel(self.ventana)
        ventana_actualizar_estudiante.title("Actualizar Estudiante")

        lbl_id_estudiante = tk.Label(ventana_actualizar_estudiante, text="ID del estudiante:")
        lbl_id_estudiante.grid(row=0, column=0)
        entry_id_estudiante = tk.Entry(ventana_actualizar_estudiante)
        entry_id_estudiante.grid(row=0, column=1)

        lbl_nombre_completo = tk.Label(ventana_actualizar_estudiante, text="Nuevo nombre completo:")
        lbl_nombre_completo.grid(row=1, column=0)
        entry_nuevo_nombre = tk.Entry(ventana_actualizar_estudiante)
        entry_nuevo_nombre.grid(row=1, column=1)

        lbl_fecha_nacimiento = tk.Label(ventana_actualizar_estudiante, text="Nueva fecha de nacimiento (YYYY-MM-DD):")
        lbl_fecha_nacimiento.grid(row=2, column=0)
        entry_nueva_fecha = tk.Entry(ventana_actualizar_estudiante)
        entry_nueva_fecha.grid(row=2, column=1)

        lbl_carrera = tk.Label(ventana_actualizar_estudiante, text="Nueva carrera:")
        lbl_carrera.grid(row=3, column=0)
        entry_nueva_carrera = tk.Entry(ventana_actualizar_estudiante)
        entry_nueva_carrera.grid(row=3, column=1)

        def actualizar_estudiante():
            id_estudiante = int(entry_id_estudiante.get())
            nuevo_nombre = entry_nuevo_nombre.get()
            nueva_fecha = entry_nueva_fecha.get()
            nueva_carrera = entry_nueva_carrera.get()

            try:
                cursor.execute("UPDATE Estudiante SET nombre_completo = %s, fecha_nacimiento = %s, carrera = %s WHERE id_estudiante = %s",
                               (nuevo_nombre, nueva_fecha, nueva_carrera, id_estudiante))
                conexion.commit()
                messagebox.showinfo("Actualizar Estudiante", "Información de estudiante actualizada con éxito.")
            except psycopg2.Error as e:
                conexion.rollback()
                messagebox.showerror("Error", f"Error al actualizar estudiante: {e}")

        btn_actualizar_estudiante = tk.Button(ventana_actualizar_estudiante, text="Actualizar", command=actualizar_estudiante)
        btn_actualizar_estudiante.grid(row=4, column=0, columnspan=2)

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

        lbl_id_materia = tk.Label(ventana_agregar_materia, text="ID de la materia:")
        lbl_id_materia.grid(row=2, column=0)
        entry_id_materia = tk.Entry(ventana_agregar_materia)
        entry_id_materia.grid(row=2, column=1)

        def guardar_materia():
            nombre = entry_nombre.get()
            num_creditos = int(entry_num_creditos.get())
            codigo = int(entry_id_materia.get())

            try:
                cursor.execute("INSERT INTO Materia (codigo, nombre, num_creditos) VALUES (%s, %s, %s) RETURNING codigo",
                               (codigo, nombre, num_creditos))
                codigo = cursor.fetchone()[0]
                conexion.commit()
                messagebox.showinfo("Agregar Materia", f"Materia creada con éxito. Código: {codigo}")
            except psycopg2.Error as e:
                conexion.rollback()
                messagebox.showerror("Error", f"Error al crear materia: {e}")

        btn_guardar_materia = tk.Button(ventana_agregar_materia, text="Guardar", command=guardar_materia)
        btn_guardar_materia.grid(row=3, column=0, columnspan=2)

    def actualizar_materia(self):
        ventana_actualizar_materia = tk.Toplevel(self.ventana)
        ventana_actualizar_materia.title("Actualizar Materia")

        lbl_codigo_materia = tk.Label(ventana_actualizar_materia, text="Código de la materia:")
        lbl_codigo_materia.grid(row=0, column=0)
        entry_codigo_materia = tk.Entry(ventana_actualizar_materia)
        entry_codigo_materia.grid(row=0, column=1)

        lbl_nombre_materia = tk.Label(ventana_actualizar_materia, text="Nuevo nombre de la materia:")
        lbl_nombre_materia.grid(row=1, column=0)
        entry_nuevo_nombre_materia = tk.Entry(ventana_actualizar_materia)
        entry_nuevo_nombre_materia.grid(row=1, column=1)

        lbl_num_creditos = tk.Label(ventana_actualizar_materia, text="Nuevo número de créditos:")
        lbl_num_creditos.grid(row=2, column=0)
        entry_nuevo_num_creditos = tk.Entry(ventana_actualizar_materia)
        entry_nuevo_num_creditos.grid(row=2, column=1)

        def actualizar_materia():
            codigo_materia = int(entry_codigo_materia.get())
            nuevo_nombre = entry_nuevo_nombre_materia.get()
            nuevo_num_creditos = int(entry_nuevo_num_creditos.get())

            try:
                cursor.execute("UPDATE Materia SET nombre = %s, num_creditos = %s WHERE codigo = %s",
                               (nuevo_nombre, nuevo_num_creditos, codigo_materia))
                conexion.commit()
                messagebox.showinfo("Actualizar Materia", "Información de materia actualizada con éxito.")
            except psycopg2.Error as e:
                conexion.rollback()
                messagebox.showerror("Error", f"Error al actualizar materia: {e}")

        btn_actualizar_materia = tk.Button(ventana_actualizar_materia, text="Actualizar", command=actualizar_materia)
        btn_actualizar_materia.grid(row=3, column=0, columnspan=2)

    def crear_nota(self):
        ventana_agregar_nota = tk.Toplevel(self.ventana)
        ventana_agregar_nota.title("Agregar Nota")
        
        lbl_id_nota = tk.Label(ventana_agregar_nota, text="ID de la nota:")
        lbl_id_nota.grid(row=0, column=0)
        entry_id_nota = tk.Entry(ventana_agregar_nota)
        entry_id_nota.grid(row=0, column=1)

        lbl_nombre_nota = tk.Label(ventana_agregar_nota, text="Nombre de la nota:")
        lbl_nombre_nota.grid(row=1, column=0)
        entry_nombre_nota = tk.Entry(ventana_agregar_nota)
        entry_nombre_nota.grid(row=1, column=1)

        lbl_puntaje = tk.Label(ventana_agregar_nota, text="Puntaje:")
        lbl_puntaje.grid(row=2, column=0)
        entry_puntaje = tk.Entry(ventana_agregar_nota)
        entry_puntaje.grid(row=2, column=1)

        lbl_codigo_materia = tk.Label(ventana_agregar_nota, text="Código de la materia:")
        lbl_codigo_materia.grid(row=3, column=0)
        entry_codigo_materia = tk.Entry(ventana_agregar_nota)
        entry_codigo_materia.grid(row=3, column=1)

        lbl_id_estudiante = tk.Label(ventana_agregar_nota, text="ID del estudiante:")
        lbl_id_estudiante.grid(row=4, column=0)
        entry_id_estudiante = tk.Entry(ventana_agregar_nota)
        entry_id_estudiante.grid(row=4, column=1)

        def guardar_nota():
            id_nota = int(entry_id_nota.get())
            nombre_nota = entry_nombre_nota.get()
            puntaje = float(entry_puntaje.get())
            codigo_materia = int(entry_codigo_materia.get())
            id_estudiante = int(entry_id_estudiante.get())

            try:
                cursor.execute("INSERT INTO Notas (id_nota, nombre_nota, puntaje, codigo_materia, id_estudiante) VALUES (%s, %s, %s, %s, %s)",
                               (id_nota, nombre_nota, puntaje, codigo_materia, id_estudiante))
                conexion.commit()
                messagebox.showinfo("Agregar Nota", "Nota creada con éxito.")
            except psycopg2.Error as e:
                conexion.rollback()
                messagebox.showerror("Error", f"Error al crear nota: {e}")

        btn_guardar_nota = tk.Button(ventana_agregar_nota, text="Guardar", command=guardar_nota)
        btn_guardar_nota.grid(row=5, column=0, columnspan=2)

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

        def calcular_promedio():
            estudiante_seleccionado = combo_estudiante.get().split(" - ")[0]
            materia_seleccionada = combo_materia.get().split(" - ")[0]

            try:
                cursor.execute("SELECT AVG(puntaje) FROM Notas WHERE id_estudiante = %s AND codigo_materia = %s",
                               (estudiante_seleccionado, materia_seleccionada))
                promedio = cursor.fetchone()[0]
                if promedio is None:
                    messagebox.showinfo("Calcular Promedio", "No hay notas registradas para este estudiante en esta materia.")
                else:
                    messagebox.showinfo("Calcular Promedio", f"El promedio de notas es: {promedio:.2f}")
            except psycopg2.Error as e:
                messagebox.showerror("Error", f"Error al calcular promedio: {e}")

        btn_calcular_promedio = tk.Button(ventana_calcular_promedio, text="Calcular", command=calcular_promedio)
        btn_calcular_promedio.grid(row=2, column=0, columnspan=2)

    def ver_materias_estudiante(self):
        ventana_ver_materias = tk.Toplevel(self.ventana)
        ventana_ver_materias.title("Ver Materias de Estudiante")

        lbl_estudiante = tk.Label(ventana_ver_materias, text="Seleccione el estudiante:")
        lbl_estudiante.grid(row=0, column=0)
        combo_estudiante = ttk.Combobox(ventana_ver_materias)
        cursor.execute("SELECT id_estudiante, nombre_completo FROM Estudiante")
        estudiantes = cursor.fetchall()
        combo_estudiante['values'] = [f"{estudiante[0]} - {estudiante[1]}" for estudiante in estudiantes]
        combo_estudiante.grid(row=0, column=1)

        def ver_materias():
            estudiante_seleccionado = combo_estudiante.get().split(" - ")[0]

            try:
                cursor.execute("SELECT DISTINCT M.codigo, M.nombre FROM Materia M INNER JOIN Notas N ON M.codigo = N.codigo_materia WHERE N.id_estudiante = %s",
                               (estudiante_seleccionado,))
                materias = cursor.fetchall()
                if not materias:
                    messagebox.showinfo("Ver Materias", "El estudiante no está registrado en ninguna materia.")
                else:
                    mensaje = "Materias en las que está registrado el estudiante:\n"
                    for materia in materias:
                        mensaje += f"Código: {materia[0]}, Nombre: {materia[1]}\n"
                    messagebox.showinfo("Ver Materias", mensaje)
            except psycopg2.Error as e:
                messagebox.showerror("Error", f"Error al recuperar las materias del estudiante: {e}")

        btn_ver_materias = tk.Button(ventana_ver_materias, text="Ver Materias", command=ver_materias)
        btn_ver_materias.grid(row=1, column=0, columnspan=2)

    def ver_notas_estudiante_materia(self):
        ventana_ver_notas = tk.Toplevel(self.ventana)
        ventana_ver_notas.title("Ver Notas de Estudiante en Materia")

        lbl_estudiante = tk.Label(ventana_ver_notas, text="Seleccione el estudiante:")
        lbl_estudiante.grid(row=0, column=0)
        combo_estudiante = ttk.Combobox(ventana_ver_notas)
        cursor.execute("SELECT id_estudiante, nombre_completo FROM Estudiante")
        estudiantes = cursor.fetchall()
        combo_estudiante['values'] = [f"{estudiante[0]} - {estudiante[1]}" for estudiante in estudiantes]
        combo_estudiante.grid(row=0, column=1)

        lbl_materia = tk.Label(ventana_ver_notas, text="Seleccione la materia:")
        lbl_materia.grid(row=1, column=0)
        combo_materia = ttk.Combobox(ventana_ver_notas)
        cursor.execute("SELECT codigo, nombre FROM Materia")
        materias = cursor.fetchall()
        combo_materia['values'] = [f"{materia[0]} - {materia[1]}" for materia in materias]
        combo_materia.grid(row=1, column=1)

        def ver_notas():
            estudiante_seleccionado = combo_estudiante.get().split(" - ")[0]
            materia_seleccionada = combo_materia.get().split(" - ")[0]

            try:
                cursor.execute("SELECT nombre_nota, puntaje FROM Notas WHERE id_estudiante = %s AND codigo_materia = %s",
                               (estudiante_seleccionado, materia_seleccionada))
                notas = cursor.fetchall()
                if not notas:
                    messagebox.showinfo("Ver Notas", "El estudiante no tiene notas registradas en esta materia.")
                else:
                    mensaje = "Notas del estudiante en la materia seleccionada:\n"
                    for nota in notas:
                        mensaje += f"{nota[0]}: {nota[1]}\n"
                    messagebox.showinfo("Ver Notas", mensaje)
            except psycopg2.Error as e:
                messagebox.showerror("Error", f"Error al recuperar las notas: {e}")

        btn_ver_notas = tk.Button(ventana_ver_notas, text="Ver Notas", command=ver_notas)
        btn_ver_notas.grid(row=2, column=0, columnspan=2)

def main():
    ventana_principal = tk.Tk()
    aplicacion = Aplicacion(ventana_principal)
    ventana_principal.mainloop()

if __name__ == "__main__":
    main()
