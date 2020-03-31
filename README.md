## Chatbot infos corona

Dans ce cas pratique on va essayer d'entraîner un chatbot qui permette de répondre automatiquement aux questions de l'utilisateur sur le coronavirus à partir de multiples informations que l'on a regroupées dans le fichier infos_corona.txt. L'idée est que le chatbot renvoie la ou les phrases utilisant le plus de termes similaires à ceux utilisés dans la question de l'utilisateur.

to run:
python app.py

anaconda:
conda create -n chatbot python=3.6
conda activate chatbot

pythonanywhere:
python3.6 -m venv env
source ./env/bin/activate 

pip install -r requirements.txt