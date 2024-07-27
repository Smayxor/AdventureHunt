import datetime
import time
import ujson as json
import math
import threading
import sys
import random
from discord.ext import tasks
import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
import requests
import os
from typing import Union

init = json.load(open('apikey.json'))
BOT_TOKEN = init['APP_TOKEN']
BOT_APP_ID = init['APP_ID']

class MyNewHelp(commands.MinimalHelpCommand):
	async def send_pages(self):
		strHelp = """}help for commands for Smayxor
/gex ticker dte strike-count charttype
/8ball followed by a question, ending in ?
/news days <- Displays upcoming events

The blue bars on left are OI.
The Red/Green bars left of the strikes are Total Gamma Exposure.
To the right of the strikes is Call Put GEX individually

}gm }tits }ass }pump }dump also exist"""
		destination = self.get_destination()
		for page in self.paginator.pages:
			await destination.send(strHelp)
bot = commands.Bot(command_prefix='}', intents=discord.Intents.all(), help_command=MyNewHelp(), sync_commands=True)

@bot.event
async def on_message(message):  #Triggered during interactions
	#print( f'Message Event?!?!? {message}' )
	pass
	
StoredIntr = []

@tasks.loop(seconds=10)
async def your_loop():
	for intr in StoredIntr :

		message = await intr.original_response()
		
		await message.edit(content=f'{intr.created_at}')


@bot.event
async def on_ready():
	your_loop.start()
	
class AddUserButton(ui.Button):
	def __init__(self):
		super().__init__(label="Buy Call!", style=discord.ButtonStyle.green)

	async def callback(self, intr: discord.Interaction):
		# Get the role you want to add the user to
		#role_id = 1234567890  # Replace with the actual role ID
		#role = intr.guild.get_role(role_id)

		await intr.response.send_message(f"{intr.user.global_name} bought a call")#, ephemeral=True)

class AddUserButton2(ui.Button):
	def __init__(self):
		super().__init__(label="Buy Put!", style=discord.ButtonStyle.green)

	async def callback(self, intr: discord.Interaction):
		# Get the role you want to add the user to
		#role_id = 1234567890  # Replace with the actual role ID
		#role = intr.guild.get_role(role_id)

		await intr.response.send_message(f"{intr.user.global_name} bought a put")#, ephemeral=True)

SERVER_IP = "http://192.168.1.254:8080" #init.get('SERVER_IP', 'http://127.0.0.1:8080')
def grabLastData():
	urlLast = f'{SERVER_IP}/last-datalog.json'
	tmp = requests.get(urlLast).json()
	
@bot.tree.command(name="farm", description="Answers your question?")
async def slash_command_farm(intr: discord.Interaction):
	perms = await checkInteractionPermissions( intr )
	await intr.response.defer(thinking=True)#, ephemeral=perms[3]==False)	
	
	#print( val )
	view = ui.View()
	view.add_item(AddUserButton())
	view.add_item(AddUserButton2())

	#do stuff
	#await intr.response.send_message(response)
	await intr.followup.send(f'{perms[0]} is buying options.', view=view)
	StoredIntr.append( intr )
#	await intr.message.add_reaction("🤩")

@bot.tree.context_menu(name='test2')
async def test2(intr: discord.Interaction, user: Union[discord.Member, discord.User] ):
	DEV_LIST = (208903205982044161, 154497072148643840, 218773382617890828)
	user = bot.get_user(DEV_LIST[0])
	print( user.name )
	await intr.response.send_message( user.name )


monsters = json.load(open('as_monsters.json'))
attribs = json.load(open('attribs.json'))	
@bot.tree.context_menu(name='test3')
async def test3(intr: discord.Interaction, msg: discord.Message):
	global monsters, attribs

	prefix = "This monster is **a"
	txt = ""
	txtDesc = ""
	for t in msg.embeds :
		
		#'author', 'clear_fields', 'color', 'colour', 'copy', 'description', 'fields', 'footer', 'from_dict', 'image', 'insert_field_at', 'provider', 'remove_author', 'remove_field', 'remove_footer', 'set_author', 'set_field_at', 'set_footer', 'set_image', 'set_thumbnail', 'thumbnail', 'timestamp', 'title', 'to_dict', 'type', 'url', 'video'
		#EmbedProxy(width=960, url='https://cdn.pixabay.com/photo/2013/10/27/14/17/demon-201422_960_720.jpg', proxy_url='https://images-ext-1.discordapp.net/external/uyIbR0GYjCNSIEEjRGYw_ZcsmfMQuJAMJQ8wlAAKGcM/https/cdn.pixabay.com/photo/2013/10/27/14/17/demon-201422_960_720.jpg', height=640)
		monsterImage = t.thumbnail.url
		
		
		txtDesc = f'```fix\n{t.description}```\n'.replace("  ",  "*** Transcended ***" )
		
		tmp = t.description.split("**")[1]
		
		q = tmp.split(" ")
		words = []
		for l in q :
			if len(l) > 2 : words.append(l)
		
		a = None
		for attr in attribs :
			if words[0] in attr:
				a = attribs[attr]
				txt += f'{attr} - HP {a[0]} TP {a[1]}'
			
		for mons in monsters : #Search by image is easier to figure out then search by X word(s) in a string
			if monsterImage in monsters[mons]["image"] :
				#print( f'Found { mons}' )
				monster = monsters[mons]
				hp = monster['hp']
				tp = monster['dipl']
				
				pd = monster['pdef']
				md = monster['mdef']
				if not a is None :
					hp *= a[0]
					tp *= a[1]
				txt += f'\n{mons} HP : {hp} / TP : {tp} - Pdef : {pd} Mdef : {md}'

	await intr.response.send_message(txtDesc + txt)#, ephemeral=True)

def getToday():
	dateAndtime = str(datetime.datetime.now()).split(" ")
	tmp = dateAndtime[1].split(".")[0].split(":")
	minute = (float(tmp[0]) * 10000) + (float(tmp[1]) * 100) + float(tmp[2])
	return (dateAndtime[0], minute)

TodaysUsers = {}
TodaysUsers['today'] = getToday()[0]
def confirmUser(userID):
	global TodaysUsers
	tday = getToday()
	if not tday[0] in TodaysUsers['today'] : #The cooldown Time doesnt include date, so.......reset it on new day
		#TodaysUsers = {}
		TodaysUsers['today'] = tday[0]
		for user in TodaysUsers :
			if user == "today" : continue
			TodaysUsers[user] = tday[1] - 10  #Reset cooldowns on new day or else!!!
	if userID in TodaysUsers :
		userCooldown = tday[1]-TodaysUsers[userID]
		if userCooldown > 10 :
			TodaysUsers[userID] = tday[1]
			return 0
		else :
			return 10 - userCooldown
	else :
		TodaysUsers[userID] = tday[1]
		return 0

#@app_commands.checks.has_permissions(moderate_members=True)
async def checkInteractionPermissions(intr: discord.Interaction):
	userID = intr.user.id
	coolDown = confirmUser(f'{intr.user.global_name}#{userID}')
	#intr in a Channel = 'app_permissions', 'application_id', 'channel', 'channel_id', 'client', 'command', 'command_failed', 'context', 'created_at', 'data', 'delete_original_response', 'edit_original_response', 'entitlement_sku_ids', 'entitlements', 'expires_at', 'extras', 'followup', 'guild', 'guild_id', 'guild_locale', 'id', 'is_expired', 'is_guild_integration', 'is_user_integration', 'locale', 'message', 'namespace', 'original_response', 'permissions', 'response', 'token', 'translate', 'type', 'user', 'version'
	
	if intr.guild_id is None : return (userID, coolDown, True, True)  #We are in a DM and can do anything we want
	permissions = intr.permissions
	textable = permissions.send_messages == True
	imageable = permissions.attach_files == True
	return ( userID, coolDown, textable, imageable )

bot.run(BOT_TOKEN)