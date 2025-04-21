import re
import sqlite3
from tkinter import messagebox, END 

# Conexión a la base de datos
def conectar_db():
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()
    sql = "CREATE TABLE IF NOT EXISTS gastos (id INTEGER PRIMARY KEY AUTOINCREMENT, fecha text, categoria text, monto real, descripcion text)"
    cursor.execute(sql)
    conn.commit()
    conn.close()

# Validar monto
def validar_monto(monto):
    return re.match(r"^\d+(\.\d{1,2})?$", monto) is not None

# Función para agregar gasto
def agregar_gasto(tree, entry_fecha, entry_categoria,entry_monto, entry_descripcion):
    fecha = entry_fecha.get()
    categoria = entry_categoria.get()
    monto = entry_monto.get()
    descripcion = entry_descripcion.get()

    if not (fecha and categoria and monto and descripcion):
        messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios")
        return

    if not validar_monto(monto):
        messagebox.showwarning("Monto inválido", "Ingrese un monto válido (ej: 123.45)")
        return

    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO gastos (fecha, categoria, monto, descripcion) VALUES (?, ?, ?, ?)",
                   (fecha, categoria, float(monto), descripcion))
    conn.commit()
    conn.close()
    limpiar_entradas(entry_fecha, entry_categoria,entry_monto, entry_descripcion)
    actualizar_lista(tree)
    


# Consultar base de datos y/o actualizar lista
def actualizar_lista(tree):
    tree.delete(*tree.get_children())
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()
    sql="SELECT * FROM gastos"
    cursor.execute(sql)
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()
    
    
# Eliminar gasto
def eliminar_gasto(tree):
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Seleccionar", "Seleccione un gasto para eliminar")
        return
    gasto_id = tree.item(seleccionado[0])["values"][0]
    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM gastos WHERE id=?", (gasto_id,))
    conn.commit()
    conn.close()
    actualizar_lista(tree)

# Función para prellenar campos al seleccionar un gasto
def seleccionar_gasto(event, tree, entry_fecha, entry_categoria, entry_monto, entry_descripcion):
    seleccionado = tree.selection()
    if not seleccionado:
        return  # No hay nada seleccionado, no hagas nada
    gasto = tree.item(seleccionado[0])["values"]
    
    entry_fecha.delete(0, END)
    entry_fecha.insert(0, gasto[1])

    entry_categoria.delete(0, END)
    entry_categoria.insert(0,gasto[2])

    entry_monto.delete(0, END)
    entry_monto.insert(0, gasto[3])

    entry_descripcion.delete(0, END)
    entry_descripcion.insert(0, gasto[4])

# Editar un gasto seleccionado
def editar_gasto(tree,entry_fecha, entry_categoria,entry_monto, entry_descripcion):
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Seleccionar", "Seleccione un gasto para editar")
        return

    gasto_id = tree.item(seleccionado[0])["values"][0]
    fecha = entry_fecha.get()
    categoria = entry_categoria.get()
    monto = entry_monto.get()
    descripcion = entry_descripcion.get()

    if not (fecha and categoria and monto and descripcion):
        messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios")
        return

    if not validar_monto(monto):
        messagebox.showwarning("Monto inválido", "Ingrese un monto válido (ej: 123.45)")
        return

    conn = sqlite3.connect("gastos.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE gastos SET fecha=?, categoria=?, monto=?, descripcion=? WHERE id=?",
                   (fecha, categoria, float(monto), descripcion, gasto_id))
    conn.commit()
    conn.close()
    limpiar_entradas(entry_fecha, entry_categoria,entry_monto, entry_descripcion)
    actualizar_lista(tree)

# Función para limpiar entradas de los inputs
def limpiar_entradas(entry_fecha, entry_categoria,entry_monto, entry_descripcion):
    entry_fecha.delete(0, END)
    entry_categoria.delete(0, END)
    entry_monto.delete(0, END)
    entry_descripcion.delete(0, END)
