import logging
import traceback

import flask
from replit import db

app = flask.Flask(__name__)

@app.errorhandler(500)
def internal_server_error(e: str):
    return flask.jsonify(error=str(e)), 500


@app.route('/', methods=['GET', 'POST'])
def cadastroContatos():
  try:
    contatos = db.get('contatos', {}); 
    print(contatos);
    if flask.request.method == "POST":      
      
      contatos[flask.request.form['email']] = {
          'nome': flask.request.form['nome'],
          'telefone': flask.request.form['telefone'],
          'assunto': flask.request.form['assunto'],
          'mensagem': flask.request.form['mensagem'],
          'resposta': flask.request.form['resposta']
      }
      
    db['contatos'] = contatos
    return flask.render_template('contatos.html', contatos=contatos)
  except Exception as e:
    logging.exception('failed to database')
    flask.abort(500, description=str(e) + ': ' + traceback.format_exc())

@app.route('/limparBanco', methods=['POST'])
def limparBanco():
  try:
    del db["contatos"];
    return flask.render_template('contatos.html')
  except Exception as e:
    logging.exception(e)
    return flask.render_template('contatos.html')

@app.route('/apagarRegistro', methods=['POST'])
def apagarRegistro():
  try:
      # Obtém o email do pedido POST
      email = flask.request.form.get('email')

      # Verifica se o email foi fornecido
      if email:
          # Verifica se o email está no banco de dados
          if email in db["contatos"]:
              # Remove o registro com base no email (chave primária)
              del db["contatos"][email]
              return flask.render_template('contatos.html', contatos=db["contatos"])
          else:
              return flask.render_template('contatos.html', message='Email não encontrado no banco de dados', contatos=db["contatos"])
      else:
          return flask.render_template('contatos.html', message='O email não foi fornecido no pedido', contatos=db["contatos"])
  except Exception as e:
      logging.exception(e)
      return flask.render_template('contatos.html', message='Ocorreu um erro ao apagar o registro', contatos=db["contatos"])
    
app.run('0.0.0.0')