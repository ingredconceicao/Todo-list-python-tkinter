import sqlite3

class Database:
    def __init__(self, db):
        #Criar a conexão com o banco
        self.con = sqlite3.connect(db)
        #Criar um cursor para realizar as operações no banco
        self.cursor = self.con.cursor()
        #Criar a tabela de funcionarios
        sql = """CREATE TABLE IF NOT EXISTS todo(
id INTEGER PRIMARY KEY,
titulo TEXT,
data TEXT,
descricao TEXT,
concluida INTEGER DEFAULT 0)"""
        #Executando o comando acima
        self.cursor.execute(sql)
        #Persistindo o que foi feito
        self.con.commit()



    def insert(self, titulo, data, descricao):
        self.cursor.execute("INSERT INTO todo (titulo, data, descricao) VALUES (?, ?, ?)", (titulo, data, descricao))
        self.con.commit()

    def update(self, id, titulo, data, descricao):
        #Edita um funcionario na tabela
        self.cursor.execute("""UPDATE todo SET titulo=?, data=?, descricao=? WHERE id=?""",(titulo, data, descricao, id))
        #Persistindo o que foi feito
        self.con.commit()

    def remove(self, id):
        #Remove um funcionario na tabela
        self.cursor.execute("""DELETE FROM todo WHERE id=?""",(id, ))
        #Persistindo o que foi feito
        self.con.commit()
        
    def fetch(self):
        #Seleciona os funcionarios da tabela
        self.cursor.execute("""SELECT * FROM todo""")
        #Salva os funcionarios na lista
        linhas = self.cursor.fetchall()
        #retorna a lista
        return linhas
    
    def concluir(self, id):
        self.cursor.execute("UPDATE todo SET concluida = 1 WHERE id = ?", (id,))
        self.con.commit()

    def concluidas(self):
        self.cursor.execute("SELECT * FROM todo WHERE concluida = 1")
        return self.cursor.fetchall()