import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Configurar la conexión a la base de datos
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Cambia esto si tu usuario de MySQL es diferente
        password="",  # Cambia esto si tu contraseña de MySQL no está vacía
        database="registros_db"
    )

# Función para agregar registros
def agregar_registro():
    def guardar_registro():
        nombre = entry_nombre.get()
        edad = entry_edad.get()

        if nombre and edad:
            try:
                conexion = conectar_db()
                cursor = conexion.cursor()
                cursor.execute("INSERT INTO registros (nombre, edad) VALUES (%s, %s)", (nombre, edad))
                conexion.commit()
                messagebox.showinfo("Éxito", "Registro agregado correctamente")
                ventana_agregar.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al agregar el registro: {err}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()
        else:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos")

    ventana_agregar = tk.Toplevel(ventana_principal)
    ventana_agregar.title("Agregar Registro")

    tk.Label(ventana_agregar, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana_agregar)
    entry_nombre.pack()

    tk.Label(ventana_agregar, text="Edad:").pack()
    entry_edad = tk.Entry(ventana_agregar)
    entry_edad.pack()

    tk.Button(ventana_agregar, text="Guardar", command=guardar_registro).pack()

# Función para ver registros
def ver_registros():
    ventana_ver = tk.Toplevel(ventana_principal)
    ventana_ver.title("Ver Registros")

    actualizar_registros(ventana_ver)
    
# Función para editar registros
def editar_registro(nombre, ventana_ver):
    def guardar_cambios():
        nuevo_nombre = entry_nombre.get()
        nueva_edad = entry_edad.get()

        if nuevo_nombre and nueva_edad:
            try:
                conexion = conectar_db()
                cursor = conexion.cursor()
                cursor.execute("UPDATE registros SET nombre = %s, edad = %s WHERE nombre = %s", (nuevo_nombre, nueva_edad, nombre))
                conexion.commit()
                messagebox.showinfo("Éxito", "Registro actualizado correctamente")
                ventana_editar.destroy()
                actualizar_registros(ventana_ver)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al actualizar el registro: {err}")
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()
        else:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos")

    ventana_editar = tk.Toplevel(ventana_principal)
    ventana_editar.title("Editar Registro")

    tk.Label(ventana_editar, text="Nombre:").pack()
    entry_nombre = tk.Entry(ventana_editar)
    entry_nombre.pack()

    tk.Label(ventana_editar, text="Edad:").pack()
    entry_edad = tk.Entry(ventana_editar)
    entry_edad.pack()

    # Cargar los datos del registro en los campos de entrada
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, edad FROM registros WHERE nombre = %s", (nombre,))
        registro = cursor.fetchone()
        if registro:
            entry_nombre.insert(0, registro[0])
            entry_edad.insert(0, registro[1])
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al obtener el registro: {err}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

    tk.Button(ventana_editar, text="Guardar Cambios", command=guardar_cambios).pack()

# Función para eliminar registros
def eliminar_registro(nombre, ventana_ver):
    respuesta = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar el registro de {nombre}?")
    if respuesta:
        try:
            conexion = conectar_db()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM registros WHERE nombre = %s", (nombre,))
            conexion.commit()
            messagebox.showinfo("Éxito", "Registro eliminado correctamente")
            actualizar_registros(ventana_ver)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al eliminar el registro: {err}")
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

# Función para actualizar la lista de registros
def actualizar_registros(ventana_ver):
    for widget in ventana_ver.winfo_children():
        widget.destroy()

    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, edad FROM registros")
        registros = cursor.fetchall()

        if registros:
            for registro in registros:
                frame_registro = tk.Frame(ventana_ver)
                frame_registro.pack(fill=tk.X, padx=5, pady=5)

                tk.Label(frame_registro, text=f"Nombre: {registro[0]}, Edad: {registro[1]}").pack(side=tk.LEFT)

                tk.Button(frame_registro, text="Editar", command=lambda nombre=registro[0]: editar_registro(nombre, ventana_ver)).pack(side=tk.RIGHT)
                tk.Button(frame_registro, text="Eliminar", command=lambda nombre=registro[0]: eliminar_registro(nombre, ventana_ver)).pack(side=tk.RIGHT)
        else:
            tk.Label(ventana_ver, text="No hay registros").pack()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al obtener los registros: {err}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()



# Configurar la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Aplicación de Registros")

tk.Button(ventana_principal, text="Agregar Registro", command=agregar_registro).pack()
tk.Button(ventana_principal, text="Ver Registros", command=ver_registros).pack()

ventana_principal.mainloop()
