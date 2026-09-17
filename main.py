import sqlite3

conexao = sqlite3.connect("banco.db")
conexao.row_factory = sqlite3.Row

cursor = conexao.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tarefas (
        pk_tarefa INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        descricao TEXT NOT NULL,
        concluida INTEGER DEFAULT 0
    )
""")

conexao.commit()

while True:
    opcao = int(input("""======================
Lista de tarefas.
======================

1- Adicionar tarefa
2 - Listar tarefas
3 - Concluir tarefa
4 - Excluir tarefa
5 - Sair

Escolha uma opção: """))

    match opcao:
        case 1:
            try:
                tarefa = input("Digite a tarefa: ")
                
                cursor.execute("INSERT INTO tarefas (descricao) VALUES (?)", (tarefa,))
                conexao.commit()
    
                print("Tarefa cadastrada.")
            except sqlite3.Error as erro:
                print(f"Erro ao cadastrar tarefa: {erro}.")
        case 2:
                   try:
                       tarefas = cursor.execute("SELECT * FROM tarefas")
       
                       tarefas = tarefas.fetchall()
       
                       for tarefa in tarefas:
                           print(f"{tarefa["pk_tarefa"]} - {tarefa["descricao"]} - { "Concluída" if tarefa["concluida"] == 1 else "Pendente" }")
       
                   except sqlite3.Error as erro:
                       print(f"Erro ao buscar tarefas: {erro}.")

conexao.close()