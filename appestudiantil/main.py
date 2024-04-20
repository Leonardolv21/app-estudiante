import tkinter as tk


class Estudiante:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
        self.materias = []

    def agregar_materia(self, materia):
        self.materias.append(materia)

    def __str__(self):
        return f"Estudiante: {self.nombre}, Edad: {self.edad}"


class Materia:
    def __init__(self, nombre):
        self.nombre = nombre
        self.notas = []

    def agregar_nota(self, nota):
        self.notas.append(nota)

    def __str__(self):
        return f"Materia: {self.nombre}"


class Nota:
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return f"Nota: {self.valor}"


class Interfaz:
    def __init__(self, master):
        self.master = master
        self.master.title("Registro de Estudiantes")
        
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.label_nombre = tk.Label(self.frame, text="Nombre:")
        self.label_nombre.grid(row=0, column=0)
        self.entry_nombre = tk.Entry(self.frame)
        self.entry_nombre.grid(row=0, column=1)

        self.label_edad = tk.Label(self.frame, text="Edad:")
        self.label_edad.grid(row=1, column=0)
        self.entry_edad = tk.Entry(self.frame)
        self.entry_edad.grid(row=1, column=1)

        self.button_agregar_estudiante = tk.Button(self.frame, text="Agregar Estudiante", command=self.agregar_estudiante)
        self.button_agregar_estudiante.grid(row=2, columnspan=2)

    def agregar_estudiante(self):
        nombre = self.entry_nombre.get()
        edad = int(self.entry_edad.get())
        estudiante = Estudiante(nombre, edad)
        self.mostrar_info_estudiante(estudiante)

    def mostrar_info_estudiante(self, estudiante):
        info = str(estudiante) + "\n"
        for materia in estudiante.materias:
            info += str(materia) + "\n"
            for nota in materia.notas:
                info += str(nota) + "\n"
        self.label_info = tk.Label(self.frame, text=info)
        self.label_info.grid(row=3, columnspan=2)


if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()
