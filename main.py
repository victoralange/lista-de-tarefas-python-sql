import sqlite3
import math

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

def buscarTarefas():
    try:
        tarefas = cursor.execute("SELECT * FROM tarefas")
        tarefas = tarefas.fetchall()
    
        return tarefas
    except sqlite3.Error as erro:
        return False

def alterarTarefa(idTarefa):
    try:
        cursor.execute("UPDATE tarefas SET concluida = 1 WHERE pk_tarefa = ?", (idTarefa,))
        conexao.commit()

        return True
    except sqlite3.Error as erro:
        return False

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
            tarefas = buscarTarefas()

            for tarefa in tarefas:
                print(f"{tarefa["pk_tarefa"]} - {tarefa["descricao"]} - { "Concluída" if tarefa["concluida"] == 1 else "Pendente" }")

        case 3:
            tarefas = buscarTarefas()

            for tarefa in tarefas:
                print(f"ID: {tarefa["pk_tarefa"]} - {tarefa["descricao"]}")

            tarefaSelecionada = int(input("\n\nInforme o identificador da tarefa para concluí-la."))

            if(math.nan(tarefaSelecionada)):
                print("ID da tarefa inválido.")

            alterarTarefa(tarefaSelecionada)

            

            

conexao.close()