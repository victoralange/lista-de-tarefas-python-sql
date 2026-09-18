import sqlite3

def conectar():
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
    return conexao

def adicionarTarefa(tarefa):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute("INSERT INTO tarefas (descricao) VALUES (?)", (tarefa["descricao"],))

        conexao.commit()

        return {
            "sucesso": True,
            "tarefaCadastrada": cursor.lastrowid
        }
    except sqlite3.Error as erro:
        return {
            "sucesso": False,
            "erro": str(erro)
        }
    finally:
        conexao.close()

def buscarTarefa(id: int):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        tarefa = cursor.execute(
            "SELECT * FROM tarefas WHERE pk_tarefa = ?",
            (id,)
        ).fetchone()

        return {
            "sucesso": True,
            "tarefa": dict(tarefa) if tarefa else None
        }

    except sqlite3.Error as erro:
        return {
            "sucesso": False,
            "erro": str(erro)
        }
    finally:
        conexao.close()

def buscarTarefas(apenasPendentes=False):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        if apenasPendentes:
            tarefas = cursor.execute(
                "SELECT * FROM tarefas WHERE concluida = 0 ORDER BY pk_tarefa DESC"
            )
        else:
            tarefas = cursor.execute(
                "SELECT * FROM tarefas ORDER BY concluida ASC, pk_tarefa DESC"
            )

        return {
            "sucesso": True,
            "tarefas": [dict(tarefa) for tarefa in tarefas.fetchall()]
        }

    except sqlite3.Error as erro:
        return {
            "sucesso": False,
            "erro": str(erro)
        }
    finally:
        conexao.close()

def concluirTarefa(idTarefa):
    conexao = conectar()
    cursor = conexao.cursor()
    
    try:
        tarefa = cursor.execute("SELECT * FROM tarefas WHERE pk_tarefa = ?", (idTarefa, )).fetchone()
        if tarefa is None or tarefa["concluida"] == 1:
            return {
                "sucesso": False,
                "erro": "Tarefa não existe ou já foi concluida."
            }
        
        cursor.execute("UPDATE tarefas SET concluida = 1 WHERE pk_tarefa = ?", (idTarefa,))
        conexao.commit()

        return {
            "sucesso": True,
            "tarefaConcluida": idTarefa
        }
    except sqlite3.Error as erro:
        return {
            "sucesso": False,
            "erro": str(erro)
        }
    finally:
        conexao.close()

def editarTarefa(idTarefa, dados):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        tarefa = cursor.execute(
            "SELECT * FROM tarefas WHERE pk_tarefa = ?",
            (idTarefa,)
        ).fetchone()

        if tarefa is None:
            return {
                "sucesso": False,
                "erro": "Tarefa não existe."
            }

        cursor.execute(
            "UPDATE tarefas SET descricao = ? WHERE pk_tarefa = ?",
            (dados["descricao"], idTarefa)
        )

        conexao.commit()

        return {
            "sucesso": True,
            "tarefaEditada": idTarefa
        }

    except sqlite3.Error as erro:
        return {
            "sucesso": False,
            "erro": str(erro)
        }
    finally:
        conexao.close()

def deletarTarefa(idTarefa):
    conexao = conectar()
    cursor = conexao.cursor()
    
    try:
        tarefa = cursor.execute("SELECT * FROM tarefas WHERE pk_tarefa = ?", (idTarefa, )).fetchone()
        if tarefa is None:
            return {
                "sucesso": False,
                "erro": "Tarefa não existe ou já foi deletada."
            }
        
        cursor.execute("DELETE FROM tarefas WHERE pk_tarefa = ?", (idTarefa,))
        conexao.commit()

        return True
    except sqlite3.Error as erro:
        return {
            "sucesso": False,
            "erro": str(erro)
        }
    finally:
        conexao.close()
