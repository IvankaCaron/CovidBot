from flask import Flask, render_template
from socket import gethostname
#from flask_socketio import SocketIO
from flask_socketio import SocketIO
import json

import multiPreprocessing 
import covidBot 

phrases_nettoyees = multiPreprocessing.tokens_net()
sent_tokens = multiPreprocessing.tokens()
tfidf = multiPreprocessing.matrix_tfidf_fit(phrases_nettoyees)
phrases_tf = multiPreprocessing.matrix_tfidf_trans(tfidf, phrases_nettoyees)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ensemblealamaison'
socketio = SocketIO(app)


@app.route('/')
def sessions():
    return render_template('session.html')


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

# écoute connection
@socketio.on('connection')
def handle_connection(data, methods=['GET', 'POST']):
    print('user connected' + str(data))


#si envoi message 
@socketio.on('message')
def handle_message(data, methods=['GET', 'POST']):
    print('le message de l user ' + str(data))
    json_str = json.dumps(data) # récup json en string
    json_object = json.loads(json_str) # json -> dict
    user = json_object['username'] # récup nom utilisateur
    message = json_object['message'] # récup message de l'utilisateur
    print(message)

    # envoi d'abord le message de l'utilisateur a afficher  div.message_holder
    # if (data.is_bot) = False  
    # div class="message user"
    socketio.emit('my response', data, callback=messageReceived)
    
    #div class="message bot"
    # réponse du bot
    bot_response = covidBot.bot_reponse(message, phrases_tf, sent_tokens, user, tfidf)
    
    # ajout is_bot dans json, affiche jquery différent si bot 
    response = {
        'is_bot': True,
        'username': 'CovidBot',
        'message': bot_response
    }
    print(response)
    socketio.emit('my response', response, callback=messageReceived)



    
if __name__ == '__main__':
    socketio.run(app)   
