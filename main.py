import sqlite3

conexao = sqlite3.connect("banco.db")

cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        pk_tarefa INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        descricao TEXT NOT NULL,
        concluida INTEGER DEFAULT 0
    )
""")

conexao.commit()
conexao.close()

print("Configurado.")