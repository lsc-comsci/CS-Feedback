from discord import Client, ChannelType
from collections import defaultdict

client = Client()

# SNOWFLAKES
feedback_channel_id = 972582248798904352

class Names:
	index = 0

with open("names.txt", "r") as f:
	Names.names = f.read().split()

def next_fake_name():
	Names.index += 1
	return Names.names[Names.index - 1]

fake_names = defaultdict(next_fake_name)

def ignore_message(message):
	"""Ignore self and all messages except DMs"""
	return message.author == client.user or message.channel.type != ChannelType.private

def retrieve_fake_name(author):
	return fake_names[author.id]

@client.event
async def on_ready():
	print(f"We have logged in as {client.user}")
	client.feedback_channel = await client.fetch_channel(feedback_channel_id)

@client.event
async def on_message(message):
	if ignore_message(message):
		return
	
	fake_name = retrieve_fake_name(message.author)

	await client.feedback_channel.send(f"{fake_name} said: {message.content}")
	await message.reply("Your feedback has been received ✅")

with open("token.txt", "r") as file:
	token = file.read()

client.run(token)
