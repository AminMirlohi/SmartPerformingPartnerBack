from flask import Flask, render_template,url_for, request, redirect, jsonify
import os
import sys
import openai
openai.api_key = ""
from flask_cors import CORS, cross_origin
import random

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))

CORS(app, support_credentials=True)

prompts = []
ans1 = []
main1 = "Nick talks about his expereinces."

prompts.append("Nick describes a match he watched recently. He talks about the address of the stadium. He talks about the names of both teams. He explains events that happened in the game. He explains how he was feeling during the game. He just talks about himself. He does not make conversation. He does not ask questions.\nNick:")
ans1.append("I watched ")

prompts.append("Nick talks about his experiences. He talks about his feelings. He talks about the activities he does to make himself feel better. He talks about himself. He does not make conversation. He does not ask questions.\nNick:")
ans1.append("I ")

prompts.append("Nick talks about the food he ate recently, like breakfast and coffee. He explains his feeling. He mentions the address of the place he got the food or coffee.\nNick:")
ans1.append("I ")

prompts.append("Nick talks about the specific match he watched with his friends and enjoyed. He explains the game, the name of the teams, and the place of the game. He talks about the food they were eating. He describes how happy he was when he watched the game with his friends.\nNick:")
ans1.append("I watched ")

prompts.append("Nick talks about a specific match he watched about three or four years ago with his friends and the food they had together. He explains the food in detail. He explained the game and the name of the teams. He explains why the food was delicious and why they enjoyed the game.\nNick:")
ans1.append("I watched ")
prompts.append("Nick talks about a specific animal. He selects an animal and talks about it. He talks about their living environment. The food they eat. The country they live in. He talks about whether they are in danger or not.\nNick:")
ans1.append("The ")

prompts.append("Nick talks about a positive movie that he watched and felt good about. He mentions a specific movie and explains why this movie helps people feel better. He explains one of its scenes in detail and explains why he like this scene. He names some of the actors and actresses.\nNick:")
ans1.append("The movie ")

prompts.append("Nick talks about diets. Nick selects a specific diet. Nick explains the diet helps him to feel good. He explains how this diet helps people stay in shape and how it can help them to feel better.\nNick:")
ans1.append("The diet ")

prompts.append("Nick talks about a product he recently purchased.  He explains why it is a great product and how he uses it. He provides the address of the place he bought it from.\nNick:")
ans1.append("I ")

prompts.append("Nick talks about a specific tv show he watched recently. He talks about the acters and actresses. He explains why he liked this tv show. He describes his favorite scene in the show. He explains how this tv show helps him feel better.\nNick:")
ans1.append("I ")

prompts.append("Nick talks about positive things. He tries to help himself feel better. He describes what steps he takes to be happy.\nNick:")
ans1.append("I ")

prompts.append("Nick talks about positive things. He tries to help himself feel better. He describes what steps he takes to be happy.\nNick:")
ans1.append("I ")

prompts.append("Nick names a specific product he recently purchased. He explains it in detail. He gives the address of the store.\nNick:")
ans1.append("I ")

prompts.append("Nick describes a match he watched recently. He explains the address of the stadium. He talks about the names of both teams. He explains the best events and scenes that happened in the game which makes him excited. He explains how he was feeling during the game.\nNick:")
ans1.append("I watched ")

prompts.append("Nick names a specific product he recently purchased. He explains how it works.\nNick:")
ans1.append("I ")

prompts.append("Nick watched a sport game recently. He names the teams and explains what happened in the game.\nNick:")
ans1.append("I watched ")


#####################################################################
#####################################################################

def retrieve_topic(answer2):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=answer2,
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["Nick:","John:", "Emily:","\n"]
            )
    return(response["choices"][0]["text"])
def retrieve_input(answer2):
     
     response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=answer2,
          temperature=0.7,
          max_tokens=1024,
          top_p=1,
          frequency_penalty=0.0,
          presence_penalty=0.0,
          stop=["Nick:","John:", "Emily:","\n"]
               )

     return(response["choices"][0]["text"])


def retrieve_input_topic(answer2):
     response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=answer2,
          temperature=0.7,
          max_tokens=512,
          top_p=1,
          frequency_penalty=0.0,
          presence_penalty=0.0
               )
     answer = response["choices"][0]["text"]
     if len(answer)>1:
          if answer[len(answer)-1]!='.':
               answer = answer+'.'
     return(answer)



def retrieve_input3(answer2):
     
     response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=answer2,
          temperature=0.7,
          max_tokens=512,
          top_p=1,
          frequency_penalty=0.0,
          presence_penalty=0.0
               )
     return(response["choices"][0]["text"])

@app.route('/', methods=['POST', 'GET'])
def index():
     if request.method == "POST":
          body = request.form.get('text')
          # data = request.get_json(force=True)
          # body = data["text"]

          answer_all=""
          topic1 = retrieve_topic("what is the main topic of this paragraph in two words:\n\""+body+"\"\nMain topic:")
          propFinal0 = "Nick talks about "+topic1+". He explains it and describes how he feels about it.\nNick:"
          answer0 = retrieve_input_topic(propFinal0)
          answer0 = answer0.rstrip().lstrip()
          if len(answer0.split('.'))>3:
               answer0 = ".".join(answer0.split('.')[:3])+"."
          answer_all += answer0
          prop_event=""
          propFinal2=""
          if len(body.split('.')) > 5:

               a = random.randint(0, 7)
               if a == 1 or a == 2 or a == 3 or a == 4:
                    prop_event = prompts[len(prompts)-a]
                   
               if len(body.split('.')) > 8:
                    a = random.randint(0, len(prompts)-1)
                    propFinal2 = prompts[a]
               
               pr = main1+" "+prop_event.replace("\nNick:","")+" After That "+propFinal2

               answer_event = retrieve_input3(pr)
               answer_event = answer_event.rstrip().lstrip()

               # if len(answer_event.split('.'))>6:
               #      answer_event = ".".join(answer_event.split('.')[:6])+'.'
               if answer_event != "":
                    answer_all+= " "+answer_event
          data_final={}
          data_final['answer']=answer_all
          resp = jsonify(data_final)
          return(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)