import requests
import json
from flask import Flask, render_template, request, redirect, url_for
from cryptography.fernet import Fernet



def getOrderStatus(data):
    headers = {
        "accept":"*/*",
        "accept-language": "fr-FR,fr;q=0.9",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "x-csrf-token": "x"

    }

    f = Fernet(b'ioRmZuU09M1_flNU9VKh3hCMnSjpoG2wEZK-ElkNCpo=')
    data = f.decrypt(str.encode(data))
    data = data.decode()
    payload= {
        "orderUuid": data,
        "timezone": "Europe/Paris"
        }
    r = requests.post('https://www.ubereats.com/api/getActiveOrdersV1?localeCode=fr',data=payload, headers=headers)
    data = json.loads(r.text)["data"]["orders"][0]
    print(len(data))
    if len(data) <= 7:
        return 'Votre commande a été livrée'
    
    return {    
                "name": f'Nom à donner au livreur: {data["orderInfo"]["customerInfos"][0]["firstName"]}',
                "state" : f'Etat de la commande: {data["feedCards"][0]["status"]["titleSummary"]["summary"]["text"]}',
                "time": f'Heure de livraison estimée: {data["feedCards"][0]["status"]["subtitleSummary"]["summary"]["text"]}'
    }


app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def home_page():
    if request.method == "POST":
        order_id = request.form['nm']
        return redirect(url_for("orderStatus", order_id=order_id))
    return render_template('index.html')

@app.route("/<order_id>")
def orderStatus(order_id):
        
        order_status = getOrderStatus(order_id)
        if order_status == 'Votre commande à été livrée':
            return render_template('order-complete.html', order_status=order_status )
        else:
            try:
                if order_status["state"] == "Arrivée imminente !":
                    order_status["hour"] = ""
                return render_template('order-status.html', order_status=order_status )
            except:
                pass



