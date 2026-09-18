from flask import Flask, render_template, jsonify, request
import main

app = Flask(__name__) 

@app.route('/')
def inicio():
    return render_template("index.html")

@app.route('/api/tarefas', methods=['GET'])
def apiBuscarTarefas():
    return jsonify(main.buscarTarefas())

@app.route('/api/tarefa/<int:id>', methods=['GET'])
def apiBuscarTarefa(id):
    return jsonify(main.buscarTarefa(id))

@app.route('/api/tarefa', methods=["POST"])
def apiAddTarefa():
    body = request.get_json()

    resposta = main.adicionarTarefa(body)

    return jsonify(resposta)

@app.route('/api/tarefa/<int:id>', methods=["PUT"])
def apiEditarTarefa(id):
    body = request.get_json()

    resposta = main.editarTarefa(id, body)

    return jsonify(resposta)

@app.route('/api/tarefa/<int:id>', methods=["DELETE"])
def apiDeletarTarefa(id):
    resposta = main.deletarTarefa(id)

    return jsonify(resposta)

@app.route('/api/tarefa/<int:id>/concluir', methods=["PUT"])
def apiConcluir(id):
    resposta = main.concluirTarefa(id)

    return jsonify(resposta)

app.run(debug=True)