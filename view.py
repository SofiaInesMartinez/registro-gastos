from tkinter import Label, Entry, Button
from tkinter.ttk import Treeview
from model import conectar_db, actualizar_lista, agregar_gasto, eliminar_gasto, editar_gasto, seleccionar_gasto

# Interfaz gráfica

def ventana_principal(root):

    root.title("Registro de Gastos Personales")


    label_fecha = Label(root, text="Fecha (YYYY-MM-DD)")
    label_fecha.grid(row=0, column=0, sticky="w")
    label_categoria = Label(root, text="Categoría")
    label_categoria.grid(row=1, column=0, sticky="w")
    label_monto = Label(root, text="Monto")
    label_monto.grid(row=2, column=0, sticky="w")
    label_descripcion = Label(root, text="Descripción")
    label_descripcion.grid(row=3, column=0, sticky="w")

    entry_fecha = Entry(root)
    entry_fecha.grid(row=0, column=1, sticky="w")

    entry_categoria = Entry(root)
    entry_categoria.grid(row=1, column=1, sticky="w")

    entry_monto = Entry(root)
    entry_monto.grid(row=2, column=1, sticky="w")

    entry_descripcion = Entry(root)
    entry_descripcion.grid(row=3, column=1, sticky="w")
   
    # Crear el Treeview
    columns = ("ID", "fecha", "categoría", "monto", "descripcion")
    tree = Treeview(root, columns=columns, show="headings")

    # Definir encabezados de columnas
    tree.heading("ID", text="ID")
    tree.heading("fecha", text="fecha")
    tree.heading("categoría", text="categoría")
    tree.heading("monto", text="monto")
    tree.heading("descripcion", text="descripción")

    # Ajustar el ancho de las columnas
    tree.column("fecha", width=150)
    tree.column("categoría", width=150)
    tree.column("monto", width=150)
    tree.column("descripcion", width=150)

    # Agregar Treeview a la ventana
    tree.grid(row=5, column=0, columnspan=2, sticky="nsew")

    # Conectar la tabla con la función de selección
    tree.bind("<<TreeviewSelect>>", lambda event: seleccionar_gasto(event, tree, entry_fecha, entry_categoria, entry_monto, entry_descripcion))

    # Botones
    boton_alta = Button(root, text="Agregar", command=lambda: agregar_gasto(tree, entry_fecha, entry_categoria, entry_monto, entry_descripcion))
    boton_alta.grid(row=1, column=2, sticky="w")
    boton_eliminar = Button(root, text="Eliminar", command=lambda: eliminar_gasto(tree))
    boton_eliminar.grid(row=2, column=2, sticky="w")
    boton_editar = Button(root, text="Editar", command=lambda: editar_gasto(tree,entry_fecha, entry_categoria, entry_monto, entry_descripcion))
    boton_editar.grid(row=3, column=2, sticky="w")

    # Iniciar base de datos y actualizar lista
    conectar_db()
    actualizar_lista(tree)


