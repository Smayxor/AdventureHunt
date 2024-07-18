import ujson as json
from discord.ext import tasks
import discord
from discord.ext import commands
from discord import app_commands
import requests

init = json.load(open('apikey.json'))
BOT_TOKEN = init['APP_TOKEN']
BOT_APP_ID = init['APP_ID']
#"APP_ID": 1262814755152990292, "APP_TOKEN"
try :
	#Declarations for slash commands
	url = "https://discord.com/api/v10/applications/" + str(BOT_APP_ID) + "/commands"
	headers = { "Authorization": "Bot " + BOT_TOKEN}

	#Removes slash commands
	#print( requests.delete("https://discord.com/api/v10/applications/" + BOT_APP_ID + "/commands/COMMAND_ID", headers=headers) )
	#print( requests.delete("https://discord.com/api/v10/applications/" + BOT_APP_ID + "/commands/1260647680405930064", headers=headers) )

	#*****************************    KEEPING FOR EXAMPLES OF WTF TO DO!!!!!     **********************************
	""" 
	slash_command_json = {
		"name": "gex", "type": 1, "integration_types": [0, 1], "contexts": [0,1,2], "description": "Draw a GEX/DEX chart", "options": [ 
		{ "name": "ticker", "description": "Stock Ticker Symbol", "type": 3, "required": True }, 
		{ "name": "dte", "description": "Days to expiration", "type": 4, "required": False }, 
		{ "name": "count", "description": "Strike Count", "type": 4, "required": False }, 
		{ "name": "chart", "description": "R for roated chart", "type": 3, "required": False, "choices": [
			{ "name": "Normal", "value": "Normal"  }, 
			{ "name": "EGEX", "value": "E" }, 
			{ "name": "Volume", "value": "V" }, 
			{ "name": "COMBO", "value": "COMBO"  }, 
			{ "name": "HEATMAP", "value": "HEATMAP"  }
		]}   
	] }
	print( requests.post(url, headers=headers, json=slash_command_json) )

	slash_command_json = { "name": "8ball", "type": 1, "integration_types": [0, 1], "contexts": [0,1,2], "description": "Answers your question", "options": [ { "name": "question", "description": "Question you need answered?", "type": 3, "required": True }] }
	print( requests.post(url, headers=headers, json=slash_command_json) )

	slash_command_json = { "name": "pc", "type": 1, "integration_types": [0, 1], "contexts": [0,1,2], "description": "Have Smayxor display price charts", "options":[
		{ "name": "strike1", "description": "5560c", "type": 3, "required": True }, 
		{ "name": "strike2", "description": "5560p", "type": 3, "required": False }] }
	print( requests.post(url, headers=headers, json=slash_command_json) )

	slash_command_json = { "name": "news", "type": 1, "integration_types": [0, 1], "contexts": [0,1,2], "description": "Gets todays events", "options":[{ "name": "days", "description": "How many days", "type": 3, "required": False, "choices": [{"name": "today", "value": "TODAY"}, {"name": "week", "value": "WEEK"}, {"name": "all", "value": "ALL"}, {"name": "1", "value": "1"}, {"name": "2", "value": "2"}, {"name": "3", "value": "3"}, {"name": "4", "value": "4"}, {"name": "5", "value": "5"}] }] }
	print( requests.post(url, headers=headers, json=slash_command_json) )
	"""
	slash_command_json = { "name": "farm", "type": 1, "integration_types": [0, 1], "contexts": [0,1,2], "description": "Farm items from server" }
	print( requests.post(url, headers=headers, json=slash_command_json) )

	slash_command_json = { "name": "test2", "type": 2, "integration_types": [0, 1], "contexts": [0,1,2] }
	response = requests.post(url, headers=headers, json=slash_command_json)
	print( response.status_code )
	print(  response.content )
	#b'{"id":"XXXXXXXXXXXXXXX","application_id":"XXXXXXXXXXXXXX","version":"1263224564025131211","default_member_permissions":null,"type":2,"name":"test2","name_localizations":null,"description":"","description_localizations":null,"dm_permission":true,"contexts":[0,1,2],"integration_types":[0,1],"nsfw":false}\n'

	slash_command_json = { "name": "test3", "type": 3, "integration_types": [0, 1], "contexts": [0,1,2] }
	print( requests.post(url, headers=headers, json=slash_command_json) )
	
except Exception as er:
	print(f'SlashCommand Error - {er}')


