import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Conexión a base de datos
def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
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
    ventana_agregar.geometry("300x200")
    ventana_agregar.configure(bg="#f4f4f4")

    frame_form = tk.Frame(ventana_agregar, bg="#f4f4f4")
    frame_form.pack(pady=20, padx=20)

    tk.Label(frame_form, text="Nombre:", bg="#f4f4f4", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=5)
    entry_nombre = tk.Entry(frame_form, font=("Segoe UI", 10))
    entry_nombre.grid(row=0, column=1, pady=5)

    tk.Label(frame_form, text="Edad:", bg="#f4f4f4", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=5)
    entry_edad = tk.Entry(frame_form, font=("Segoe UI", 10))
    entry_edad.grid(row=1, column=1, pady=5)

    tk.Button(ventana_agregar, text="Guardar", font=("Segoe UI", 10, "bold"),
              bg="#4CAF50", fg="white", command=guardar_registro).pack(pady=10)

# Ver registros
def ver_registros():
    ventana_ver = tk.Toplevel(ventana_principal)
    ventana_ver.title("Ver Registros")
    ventana_ver.configure(bg="#f4f4f4")
    ventana_ver.geometry("400x400")
    actualizar_registros(ventana_ver)

# Editar registros
def editar_registro(nombre, ventana_ver):
    def guardar_cambios():
        nuevo_nombre = entry_nombre.get()
        nueva_edad = entry_edad.get()

        if nuevo_nombre and nueva_edad:
            try:
                conexion = conectar_db()
                cursor = conexion.cursor()
                cursor.execute("UPDATE registros SET nombre = %s, edad = %s WHERE nombre = %s",
                               (nuevo_nombre, nueva_edad, nombre))
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
    ventana_editar.geometry("300x200")
    ventana_editar.configure(bg="#f4f4f4")

    frame_form = tk.Frame(ventana_editar, bg="#f4f4f4")
    frame_form.pack(pady=20, padx=20)

    tk.Label(frame_form, text="Nombre:", bg="#f4f4f4", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=5)
    entry_nombre = tk.Entry(frame_form, font=("Segoe UI", 10))
    entry_nombre.grid(row=0, column=1, pady=5)

    tk.Label(frame_form, text="Edad:", bg="#f4f4f4", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=5)
    entry_edad = tk.Entry(frame_form, font=("Segoe UI", 10))
    entry_edad.grid(row=1, column=1, pady=5)

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

    tk.Button(ventana_editar, text="Guardar Cambios", font=("Segoe UI", 10, "bold"),
              bg="#2196F3", fg="white", command=guardar_cambios).pack(pady=10)

# Eliminar registros
def eliminar_registro(nombre, ventana_ver):
    respuesta = messagebox.askyesno("Confirmar", f"¿Deseas eliminar el registro de {nombre}?")
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

# Actualizar registros
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
                frame = tk.Frame(ventana_ver, bg="#ffffff", relief="solid", bd=1)
                frame.pack(padx=10, pady=5, fill="x")

                tk.Label(frame, text=f"Nombre: {registro[0]}", bg="#ffffff",
                         font=("Segoe UI", 10)).pack(anchor="w", padx=10)
                tk.Label(frame, text=f"Edad: {registro[1]}", bg="#ffffff",
                         font=("Segoe UI", 10)).pack(anchor="w", padx=10)

                botones = tk.Frame(frame, bg="#ffffff")
                botones.pack(anchor="e", padx=10, pady=5)

                tk.Button(botones, text="Editar", bg="#FFC107", fg="black",
                          font=("Segoe UI", 9), command=lambda n=registro[0]: editar_registro(n, ventana_ver)).pack(side="left", padx=5)
                tk.Button(botones, text="Eliminar", bg="#f44336", fg="white",
                          font=("Segoe UI", 9), command=lambda n=registro[0]: eliminar_registro(n, ventana_ver)).pack(side="left", padx=5)
        else:
            tk.Label(ventana_ver, text="No hay registros", bg="#f4f4f4", font=("Segoe UI", 11)).pack(pady=20)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al obtener los registros: {err}")
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Gestor de Registros")
ventana_principal.geometry("300x200")
ventana_principal.configure(bg="#e0f7fa")

tk.Label(ventana_principal, text="Menú Principal", font=("Segoe UI", 14, "bold"),
         bg="#e0f7fa", fg="#333").pack(pady=15)

tk.Button(ventana_principal, text="Agregar Registro", font=("Segoe UI", 10, "bold"),
          bg="#4CAF50", fg="white", width=20, command=agregar_registro).pack(pady=5)

tk.Button(ventana_principal, text="Ver Registros", font=("Segoe UI", 10, "bold"),
          bg="#2196F3", fg="white", width=20, command=ver_registros).pack(pady=5)

ventana_principal.mainloop()
