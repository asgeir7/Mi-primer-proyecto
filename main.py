from tkinter import ttk
from tkinter import *

import sqlite3

class sqlite:

    def connect(self, db):
        self.conn = sqlite3.connect(db)
        return True

    def query(self, query, params=()):
        cursor = self.conn.cursor()
        result = cursor.execute(query,params)
        self.conn.commit()
        return result

class Producto:

    def __init__(self, ventana):
        self.db = sqlite()
        self.db.connect('database.db')

        self.wnd = ventana
        self.wnd.title('Aplicacion')

        frame = LabelFrame(self.wnd, text='Registrar nuevo Producto')
        frame.grid(row=0, column=0, columnspan=2)

        Label(frame,text='Nombre: ').grid(row=1,column=0)
        self.nombre = Entry(frame)
        self.nombre.focus()
        self.nombre.grid(row=1,column=1)

        Label(frame,text='Precio: ').grid(row=2,column=0)
        self.precio = Entry(frame)
        self.precio.grid(row=2,column=1)

        ttk.Button(frame, text='Guardar',command=self.addProduct).grid(row=3,column=0, columnspan=2, sticky=W+E)

        self.msg = Label(text='', fg='blue')
        self.msg.grid(row=3,column=0, columnspan=2, sticky=W+E)

        self.tabla = ttk.Treeview(height=10,columns=2)
        self.tabla.grid(row=4, column=0, columnspan=2)
        self.tabla.heading('#0',text='Nombre',anchor=CENTER)
        self.tabla.heading('#1',text='Precio',anchor=CENTER)
        self.clean_table_selection()
        self.showProduct()

        ttk.Button(text='Editar', command=self.editProduct).grid(row=5,column=0,sticky=W+E)
        ttk.Button(text='Eliminar', command=self.deleteProduct).grid(row=5,column=1,sticky=W+E)

        # print(*db.query('Select * from productos'))

    def message(self, text, item, color):
        self.msg['text'] = text.format(item)
        self.msg['fg'] = color

    def cleanInput(self):
        self.nombre.delete(0,END)
        self.precio.delete(0,END)

    def validate(self):
        return not self.nombre.get() and not self.precio.get()

    def clean_table_selection(self):
        [self.tabla.delete(ele) for ele in self.tabla.get_children()]

    def showProduct(self):
        result = self.db.query('Select * from productos')
        for row in result:
            self.tabla.insert('',0,text=row[1], values=row[2])

    def addProduct(self):
        if self.validate():
            self.message('El producto y precio son requeridos {}!','','red')
        else:
            self.db.query('INSERT INTO productos VALUES(NULL, ?, ?)', (self.nombre.get(),self.precio.get()))
            self.clean_table_selection()
            self.showProduct()
            self.message('Producto {} anadido correctamente!',self.nombre.get(),'blue')
            self.cleanInput()

    def deleteProduct(self):
        self.message('{}','' ,'blue')
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            # self.message('Debe elegir un producto!','','blue')
            print('hubo un error')
            return

        item = self.tabla.item(self.tabla.selection())['text']
        self.db.query('DELETE FROM productos WHERE nombre=?', (item, ))
        self.message('Producto {} eliminado!',item ,'blue')
        self.clean_table_selection()
        self.showProduct()

    def editProduct(self):
        try:
            self.tabla.item(self.tabla.selection())['text'][0]
        except IndexError as e:
            print('hubo un error')
        return

        item = self.tabla.item(self.tabla.selection())['text']

        self.old_wnd = Toplevel()
        # self.db.query('DELETE FROM productos WHERE nombre=?', (item, ))
        # self.message('Producto {} eliminado!',item ,'blue')
    # self.showProduct()


if __name__ == '__main__':
    ventana = Tk()
    app = Producto(ventana)
    ventana.mainloop()
