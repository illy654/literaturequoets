import json
import random
import smtplib
from email.message import EmailMessage
from bs4 import BeautifulSoup



def getRandomQuotes(amount):
    ToReturn = {
        "Stave":None,
        "Quote": [],
        "Explaination": [],
    }
    with open("quotes.json") as f:
        data = json.loads(f.read())
        ToReturn["Stave"] = random.randint(1,2)
        data = data["S" + str(ToReturn["Stave"])]

    while len(ToReturn["Quote"]) != amount:
        isThere = False
        rand = data[random.randint(0, len(data) - 1)]

        for quote in ToReturn["Quote"]:
            if quote == rand["Quote"]:
                isThere = True
                break


        if isThere: continue

        ToReturn["Quote"].append(rand["Quote"])
        ToReturn["Explaination"].append(rand["Explaination"])
    return ToReturn




def sendEmail(sender, password):
    
    msg = EmailMessage()
    msg["Subject"] = "You got rejected."
    msg["From"] = "notababy008@gmail.com"
    msg["To"] = "notababy008@gmail.com"
    msg.set_content("We are sorry, your grade just wasn't good enough.")
    
    with open("template.html", "r") as f:
        data = f.read()

    soup = BeautifulSoup(data, "html.parser")

    lis = soup.find_all("li")
    quotes = getRandomQuotes(3)

    for index,i in enumerate(lis):
        i.string.replace_with("'" + quotes["Quote"][index]+"'", soup.new_tag("br"),soup.new_tag("br")  ,"Explaination:", quotes["Explaination"][index])

    msg.add_alternative(
        soup.prettify(), subtype="html"
    )

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)

    return 0
    



print(sendEmail("notababy008@gmail.com","Illy654!"))


