import mysql.connector
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
app = Flask(__name__)
api = Api(app)
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="nfl_play_by_play"
)

mycursor = mydb.cursor()

def inList(list, elem):
  for x in list:
    if x["name"] == elem:
      return True
  return False
def index(list, elem):
  for x in range(len(list)):
    if list[x]["name"] == elem:
      return x
def takeSecond(elem):
    return elem["count"]
def findPlays(playerId):
  mycursor.execute('SELECT receiver_player_name FROM `plays` WHERE passer_player_id=%s AND NOT receiver_player_name="None"', playerId)
  myresult = mycursor.fetchall()
  return myresult

@app.route('/qb')
def test():
  firstName = request.args.get('firstName')
  lastName = request.args.get('lastName')
  mycursor.execute("""SELECT gsisId FROM `players` WHERE firstName="%s" AND lastName="%s" LIMIT 1""" %(firstName, lastName))
  myresult = mycursor.fetchall()
  x = myresult[0]
  nex = findPlays(x)
  players = []
  for x in nex:
    if not inList(players, x[0]):
      players.append({"name":x[0], "count":1})
    else:
      players[index(players, x[0])]["count"] += 1
  players.sort(key=takeSecond)
  return str(players)

if __name__ == "__main__":
    app.run()