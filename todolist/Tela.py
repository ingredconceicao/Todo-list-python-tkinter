from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from turtle import bgcolor, heading
from bd import Database

db = Database("todo.db")
janela = Tk()
janela.title("ToDo List - Organize-se")
janela.geometry("1920x1080")
janela.config(bg = "#000000")
janela.state("zoomed")

titulo = StringVar()
data = StringVar()
descricao = StringVar()

frame1 = Frame(janela, bg = "#000000")
frame1.pack(fill=X)

titulo = Label(frame1, text="ToDo List",
               font=("Calibri", 18, "bold"), bg= "#000000", fg="white")
titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="w")

labelTitulo = Label(frame1, text="Titulo:", bg= "#000000", fg="white",
                  font=("Calibri", 16))
labelTitulo.grid(row=1, column=0, padx=10, pady=10, sticky="w")
txtTitulo = Entry(frame1, textvariable=titulo, font=("Calibri", 16), width=30)
txtTitulo.grid(row=1, column=1, padx=10, pady=10, sticky="w")

labelData = Label(frame1, text="Data (DD/MM/AAAA):", bg= "#000000", fg="white",
                  font=("Calibri", 16))
labelData.grid(row=1, column=2, padx=10, pady=10, sticky="w")
txtData = Entry(frame1, textvariable=data, font=("Calibri", 16), width=30)
txtData.grid(row=1, column=3, padx=10, pady=10, sticky="w")

labelDescricao = Label(frame1, text="Descrição da atividade:", bg= "#000000", fg="white",
                  font=("Calibri", 16))
labelDescricao.grid(row=2, column=0, padx=10, pady=10, sticky="w")
txtDescricao = Entry(frame1, textvariable=descricao, font=("Calibri", 16), width=30)
txtDescricao.grid(row=2, column=1, padx=10, pady=10, sticky="w")

def getData(event):
    #pega a linha da tabela onde o ponteiro está quando ocorre o evento
    selected_row = tv.focus()
    #pega o item(funcionario) que está nessa linha da tabela
    data = tv.item(selected_row)
    global row
    row = data["values"]
    #titulo.set(row[0])
    #data.set(row[3])
    #descricao.set(row[4])
    
def displayAll():
    tv.delete(*tv.get_children())
    for i in db.fetch():
        tv.insert("", END, values=i)

def mostrar_concluidas():
    tv.delete(*tv.get_children())
    for i in db.concluidas():
        tv.insert("", END, values=i)



def add_atividade():
    if(txtTitulo.get() == "" or txtData.get() == "" or txtDescricao.get() == ""):
        messagebox.showerror("Erro na entrada", "Por favor, preencha todos os campos")
    else:
        db.insert(txtTitulo.get(), txtData.get(), txtDescricao.get())
        messagebox.showinfo("Sucesso", "Atividade Cadastrada com sucesso")
        displayAll()

def edit_atividade():
    try:
        if(txtTitulo.get() == "" or txtData.get() == "" or txtDescricao.get() == ""):
            messagebox.showerror("Erro na entrada", "Por favor, preencha todos os campos")
        else:
            db.update(row[0], txtTitulo.get(), txtData.get(), txtDescricao.get())
            messagebox.showinfo("Sucesso", "Atividade atualizada com sucesso")
            displayAll()
    except NameError:
        messagebox.showerror("Erro", "Nenhuma tarefa selecionada para editar")

def del_atividade():
    db.remove(row[0])
    messagebox.showinfo("Sucesso", "Atividade Excluida com sucesso")
    displayAll()

def concluir_atividade():
    try:
        db.concluir(row[0])
        messagebox.showinfo("Sucesso", "Atividade marcada como concluída")
        limpar_campos()
        displayAll()
    except NameError:
        messagebox.showerror("Erro", "Nenhuma tarefa selecionada.")

def limpar_campos():
    txtTitulo.delete(0, END)
    txtData.delete(0, END)
    txtDescricao.delete(0, END)
                  

frame2 = Frame(frame1, bg= "#000000")
frame2.grid(row=6, column=0, columnspan=4, padx=10, pady=10, sticky="w")

add = Button(frame2, text="Adicionar", width=15, font=("Calibri", 16, "bold"),
             fg="white", bg="#16a085", command=add_atividade)
add.grid(row=0, column=0, padx=10)

edit = Button(frame2, text="Editar", width=15, font=("Calibri", 16, "bold"),
             fg="white", bg="#2980b9", command=edit_atividade)
edit.grid(row=0, column=1, padx=10)

delete = Button(frame2, text="Deletar", width=15, font=("Calibri", 16, "bold"),
             fg="white", bg="#c0392b", command=del_atividade)
delete.grid(row=0, column=2, padx=10)

concluir = Button(frame2, text="Concluir", width=15, font=("Calibri", 16), bg="#27ae60", fg="white",
        command=concluir_atividade).grid(row=0, column=3, padx=10)

ver_concluidas = Button(frame2, text="Ver concluidas", width=15, font=("Calibri", 16), bg="#9727ae", fg="white",
        command=mostrar_concluidas).grid(row=0, column=4, padx=10)





frame3 = Frame(janela, bg="#ecf0f1")
frame3.place(x=0, y=430, width=1980, height=520)

style = ttk.Style()
style.configure("mystyle.Treeview", font=("Calibri", 14), rowheight=50)
style.configure("mystyle.Treeview.Heading", font=("Calibri", 14))
tv = ttk.Treeview(frame3, columns=(1,2,3,4,), style="mystyle.Treeview")
tv.heading("1", text="Id")
tv.column("1", width=60, stretch=NO)
tv.heading("2", text="Titulo")
tv.column("2", width=300, stretch=NO)
tv.heading("3", text="Data")
tv.column("3", width=60, stretch=NO)
tv.heading("4", text="Descrição")
tv.column("4", width=165, stretch=NO)
tv["show"] = "headings"
tv.bind("<ButtonRelease-1>", getData)
tv.pack(fill=X)

displayAll()

janela.mainloop()
