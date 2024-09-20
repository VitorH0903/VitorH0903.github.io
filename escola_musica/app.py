from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Função para criar uma conexão com o banco de dados
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='admin',
            database='escola_musica'
        )
        print("Conexão com o MySQL realizada com sucesso.")
    except Error as e:
        print(f"Erro '{e}' ocorreu.")
        return None  # Retorna None se a conexão falhar
    return connection

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para gerenciar alunos
@app.route('/alunos')
def alunos():
    connection = create_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500  # Retorna uma resposta de erro
    
    alunos = consultar_alunos(connection)
    professores = consultar_professores(connection)  # Obter lista de professores
    connection.close()
    
    return render_template('alunos.html', alunos=alunos, professores=professores)

@app.route('/adicionar_aluno', methods=['POST'])
def adicionar_aluno():
    nome = request.form['nome']
    idade = request.form['idade']
    instrumento = request.form['instrumento']
    id_professor = request.form['id_professor']

    connection = create_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500  # Retorna uma resposta de erro

    insert_aluno(connection, nome, idade, instrumento, id_professor)
    
    connection.close()
    
    return redirect(url_for('alunos'))  # Redireciona para a lista de alunos após adicionar

# Rota para gerenciar aulas
@app.route('/aulas')
def aulas():
    connection = create_connection()
    if connection is None:
        return "Erro ao conectar ao banco de dados.", 500  # Retorna uma resposta de erro
    
    aulas = consultar_aulas(connection)
    connection.close()
    
    return render_template('aulas.html', aulas=aulas)

# Função para consultar alunos
def consultar_alunos(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Aluno")
    alunos = cursor.fetchall()
    cursor.close()  # Fecha o cursor após a consulta
    return alunos

# Função para inserir um aluno
def insert_aluno(connection, nome, idade, instrumento, id_professor):
    cursor = connection.cursor()
    query = "INSERT INTO Aluno (nome_aluno, idade, instrumento, id_professor) VALUES (%s, %s, %s, %s)"
    
    try:
        cursor.execute(query, (nome, idade, instrumento, id_professor))
        connection.commit()
        print("Aluno inserido com sucesso.")
    except Error as e:
        print(f"Erro ao inserir aluno: '{e}'")
        connection.rollback()  # Rollback em caso de erro
    finally:
        cursor.close()  # Garante que o cursor seja fechado

# Função para consultar professores
def consultar_professores(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Professor")  # Supondo que exista uma tabela chamada Professor
    professores = cursor.fetchall()
    cursor.close()  # Fecha o cursor após a consulta
    return professores

# Função para consultar aulas
def consultar_aulas(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Aula")  # Supondo que exista uma tabela chamada Aula
    aulas = cursor.fetchall()
    cursor.close()  # Fecha o cursor após a consulta
    return aulas

if __name__ == "__main__":
    app.run(debug=True)