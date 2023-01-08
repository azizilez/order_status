import requests
import json
from flask import Flask, render_template, request, redirect, url_for
def getOrderStatus(data):
    headers = {
        "accept":"*/*",
        "accept-language": "fr-FR,fr;q=0.9",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "x-csrf-token": "x"

    }
    payload= {
            "orderUuid": data,
            "timezone": "Europe/Paris"
            }
    r = requests.post('https://www.ubereats.com/api/getActiveOrdersV1?localeCode=fr',data=payload, headers=headers)
    try:
        data = json.loads(r.text)["data"]["orders"][0]
        print(len(data))
        if len(data) <= 7:
            return 'Votre commande à été livrée'
        return {    
                    "name": f'Nom à donner au livreur: {data["orderInfo"]["customerInfos"][0]["firstName"]}',
                    "state" : f'Etat de la commande: {data["feedCards"][0]["status"]["titleSummary"]["summary"]["text"]}',
                    "time": f'Heure de livraison estimée: {data["feedCards"][0]["status"]["subtitleSummary"]["summary"]["text"]}'
        }
    except KeyError:
        pass

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
            if order_status["state"] == "Arrivée imminente !":
                order_status["hour"] = ""
            return render_template('order-status.html', order_status=order_status )

        

'''
accounts = len(os.listdir('accounts/'))
info = {"name":{"first":"Jeffery","last":"Pacocha","underscore":"jeffery_pacocha"},"date2use":"31/12/2022","creationIP":"93.23.248.89","orderIP":"","usedTimes":0,"promos":{"reduction":"-15 € / 20 €","times":"2 ","duration":"10 janv. 2023 14 h"},"mail":"jeffery_pacocha9686@spinwheelnow.com","cookies":[{"name":"sid","value":"QA.CAESEJlMby0kyUM1hlXPlnQcSvQY0te3ngYiATEqJDdjMzMxMGM0LTExZmYtNDJhMS1iOWQ2LWY3ZTg4YjI5YjA0ZTJAEJJEk0OnUzEoy5Q_bnnR9QhhnyrSJzTE78enOkAxGXozuVZRcQYDxl_qUN6ezkK2Yk7kDshBbVfb2erT_-7M3ToBMUINLnViZXJlYXRzLmNvbQ.8-Ccyx58lB2W18MVGCpVJCymDobQaew08n-yp0W-_y0","domain":".ubereats.com","path":"/","expires":1674439634.705165,"size":252,"httpOnly":True,"secure":True,"session":False,"sameParty":False,"sourceScheme":"Secure","sourcePort":443},{"name":"usl_rollout_id","value":"94c5358a-efd5-436a-a115-ceefc8f3339a","domain":"www.ubereats.com","path":"/","expires":1703383641.331579,"size":50,"httpOnly":True,"secure":True,"session":False,"sameParty":False,"sourceScheme":"Secure","sourcePort":443},{"name":"jwt-session","value":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7Il9fand0X3JwY19wcm90ZWN0aW9uX2V4cGlyZXNfYXRfbXMiOjE2NzE4NDkyMDk1NjAsIl9fand0X3JwY19wcm90ZWN0aW9uX3V1aWQiOiJjM2I3NTlhYS05MGQ5LTRhMDMtODBlNi0yMjIwNzU2ODlhYjYiLCJfX2p3dF9ycGNfcHJvdGVjdGlvbl9jcmVhdGVkX2F0X21zIjoxNjcxODQ3NjM5NTYwfSwiaWF0IjoxNjcxODQ3NjM5LCJleHAiOjE2NzE5MzQwMzl9.-4GRZ-OeHgb4v7nCqnqrlMrjkdIjXraTx_hlmPC0Hx8","domain":"www.ubereats.com","path":"/","expires":1671934039.889427,"size":376,"httpOnly":True,"secure":True,"session":False,"sameParty":False,"sourceScheme":"Secure","sourcePort":443},{"name":"marketing_vistor_id","value":"4507cfbb-5593-4d3b-8ba3-030327cb9a45","domain":".ubereats.com","path":"/","expires":1703383642.333963,"size":55,"httpOnly":False,"secure":True,"session":False,"sameParty":False,"sourceScheme":"Secure","sourcePort":443},{"name":"uev2.ts.session","value":"1671847639542","domain":".ubereats.com","path":"/","expires":1671849442.333955,"size":28,"httpOnly":True,"secure":True,"session":False,"sameParty":False,"sourceScheme":"Secure","sourcePort":443},{"name":"dId","value":"098d0b49-b7a3-46f0-91c0-e93bd4f29ff7","domain":".ubereats.com","path":"/","expires":1703383639.889313,"size":39,"httpOnly":True,"secure":True,"session":False,"sameParty":False,"sourceScheme":"Secure","sourcePort":443},{"name":"uev2.id.session","value":"d6731383-58d6-45a4-8974-e32af9111398","domain":".ubereats.com","path":"/","expires":1671849442.333945,"size":51,"httpOnly":False,"secure":True,"session":False,"sameParty":False,"sourceScheme":"Secure","sourcePort":443},{"name":"uev2.id.xp","value":"ae5af741-b4e2-46f6-acd7-7a8300524086","domain":".ubereats.com","path":"/","expires":-1,"size":46,"httpOnly":True,"secure":True,"session":True,"sameParty":False,"sourceScheme":"Secure","sourcePort":443}]}
with open(f'accounts/{accounts}','w') as file:
        file.write(json.dumps(info))
        #print(json.load(file))
'''