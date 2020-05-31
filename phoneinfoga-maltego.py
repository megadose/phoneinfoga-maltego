from MaltegoTransform import *
import json,requests
num=sys.argv[1]
import os
trx = MaltegoTransform()
from time import sleep
def KillPhoneInfoga():
    os.system("killall phoneinfoga")
def StartPhoneInfoga():
    os.system("phoneinfoga serve > /dev/null &")

def numverify():
    response = requests.get('http://127.0.0.1:5000/api/numbers/'+num+'/scan/numverify')
    #print(response.text)
    if str(json.loads(response.text)["success"])=="True":
        result = json.loads(response.text)["result"]
        if str(result["valid"])=="True":
            if str(result["carrier"])!="":
                trx.addEntity("maltego.Phrase",result["carrier"]).setNote("Carrier")
            if str(result["country_code"])!="":
                if result["location"]!="":
                    location = trx.addEntity("maltego.Location",str(result["country_name"]+" , "+result["location"]))
                else:
                    location = trx.addEntity("maltego.Location",result["country_name"])
                location.addProperty(fieldName="countrycode",value=result["country_code"])
            if str(result["line_type"])!="":
                trx.addEntity("maltego.Phrase",result["line_type"]).setNote("Line Type")
        else:
            trx.addEntity("maltego.Phrase","Invaid Phone Number")
    else:
        trx.addEntity("maltego.Phrase","Invaid Phone Number")



def ovh():
    response = requests.get('http://127.0.0.1:5000/api/numbers/'+num+'/scan/ovh')
    #print(response.text)
    if str(json.loads(response.text)["success"])=="True":
        result = json.loads(response.text)["result"]
        if str(result["found"])!="False":
            if str(result["numberRange"])!="":
                trx.addEntity("maltego.Phrase",result["numberRange"]).setNote("numberRange")
            if str(result["city"])!="":
                location = trx.addEntity("maltego.Location")
                location.addProperty(fieldName="city",value=result["city"])
KillPhoneInfoga()
StartPhoneInfoga()
sleep(0.2)
numverify()
ovh()
KillPhoneInfoga()

print(trx.returnOutput())
