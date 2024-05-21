from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from datetime import datetime
from config import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'chave secreta'

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/consultas', methods=['GET', 'POST'])
def consultas():
    if request.method == 'POST':
        campo = request.form['campo']
        valor = request.form['valor']

        if campo == 'cpf':
            cursor.execute('SELECT * FROM pacientes WHERE cpf = %s', (valor,))
        elif campo == 'nome':
            cursor.execute('SELECT * FROM pacientes WHERE nome ILIKE %s', (f'%{valor}%',))
        elif campo == 'telefone':
            cursor.execute('SELECT * FROM pacientes WHERE telefone = %s', (valor,))

        paciente = cursor.fetchone()

        if paciente:            
            cpf = paciente[0]
            nome = paciente[1]
            telefone = paciente[2]
            endereco = paciente[3]
            
            hepatite_b_info = formatar_vacina(paciente[4], 'Hepatite B')
            dupla_bacteriana_info = formatar_vacina(paciente[5], 'Dupla Bacteriana')
            febre_amarela_info = formatar_vacina(paciente[6], 'Febre Amarela')
            influenza_info = formatar_vacina(paciente[7], 'Influenza')
            covid_19_info = formatar_vacina(paciente[8], 'COVID-19')

            return render_template('consultas.html', cpf=cpf, nome=nome, telefone=telefone, endereco=endereco,
                                   hepatite_b=hepatite_b_info, dupla_bacteriana=dupla_bacteriana_info,
                                   febre_amarela=febre_amarela_info, influenza=influenza_info, covid_19=covid_19_info)
        else:
            flash('Paciente não cadastrado', 'error')

    return render_template('consultas.html')

def formatar_vacina(vacina_info, vacina_nome):
    if vacina_info:
        data, lote = vacina_info.split(' || ')
        data_formatada = datetime.strptime(data, '%Y-%m-%d').strftime('%d-%m-%Y')
        return f'{data_formatada}        Lote: {lote}'
    else:
        return f'Não aplicado'


@app.route('/lancamentos', methods=['POST', 'GET'])
def lancamentos():
    if request.method == 'POST':
        cpf = request.form['cpf']
        vacina = request.form['vacina']
        lote = request.form['lote']
        data = request.form['data']

        cursor.execute('SELECT * FROM pacientes WHERE cpf = %s', (cpf,))
        paciente = cursor.fetchone()

        if paciente:
            try:
                if vacina == 'Hepatite B':
                    cursor.execute('UPDATE pacientes SET hepatite_b = %s WHERE cpf = %s', (f'{data} || {lote}', cpf))
                elif vacina == 'Dupla Bacteriana':
                    cursor.execute('UPDATE pacientes SET dupla_bacteriana = %s WHERE cpf = %s', (f'{data} || {lote}', cpf))
                elif vacina == 'Febre Amarela':
                    cursor.execute('UPDATE pacientes SET febre_amarela = %s WHERE cpf = %s', (f'{data} || {lote}', cpf))
                elif vacina == 'Influenza':
                    cursor.execute('UPDATE pacientes SET influenza = %s WHERE cpf = %s', (f'{data} || {lote}', cpf))
                elif vacina == 'COVID-19':
                    cursor.execute('UPDATE pacientes SET covid_19 = %s WHERE cpf = %s', (f'{data} || {lote}', cpf))

                conn.commit()
                flash('Dados atualizados com sucesso!', 'success')
            except Exception as e:
                flash(f'Erro ao atualizar dados: {str(e)}', 'error')

        else:
            flash('CPF não cadastrado no sistema.', 'error')

    return render_template('lancamentos.html')

if __name__ == '__main__':
    app.run(debug=True)
