import logging
import nextcord
from nextcord.ext import commands

# Logs to a file "nextcord.log" (Copied from docs)
logger = logging.getLogger('nextcord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Setting discord intents. The intent for members needs to be enabled in the developer page.
intents = nextcord.Intents.none()
intents.members = True
intents.guilds = True
intents.emojis = True
intents.guild_messages = True
intents.guild_reactions = True

# Setting up the bot
bot = commands.Bot(command_prefix="!", intents=intents)
token =  # Paste it here in quotes

# Generating the emoji list
emojilist = []

# 1-9 number keycap emoji are <number> + FE0F + 20E3
for i in range(0x31,0x3A):
    emojilist.append(f'{chr(i)}\uFE0F\u20E3')

# 10 keycap emoji is special
emojilist.append('\U0001F51F')

# A-Z letter regional indicator emoji are 1F1E6-1F1FF
for i in range(0x1F1E6, 0x1F200):
    emojilist.append(chr(i))

# Function to determine if someone is an admin
async def is_admin(ctx):
    roles = ctx.author.roles
    return "Game Administrator" in [str(x) for x in roles]

@bot.command()
@commands.check(is_admin) # Will not run if the person isn't an admin
async def pollusers(ctx, *args):
    # Find if a poll title is given
    if len(args) > 0: polltitle = ' '.join(args)
    else: polltitle = ""

    # Basic setup
    server = ctx.guild
    roles = server.roles

    # Get the role object for Player (Alive)
    for role in roles:
        if str(role) == "Player (Alive)":
            req_role = role
            break

    # Begin the message to be sent
    poll = polltitle + "\n"

    # List of alive players
    users = req_role.members

    # Generate the poll message
    reacts = 0
    for i in range(len(users)):
        poll += f"{emojilist[i]} **{users[i].display_name}** ({users[i].name}#{users[i].discriminator})\n"
        reacts += 1

    # Send it 
    msg = await ctx.send(poll)

    # Add the reactions that have been used to it. (NOTE: Maximum of 20 reactions on Discord!)
    for i in range(reacts):
        await msg.add_reaction(emojilist[i])


# Actually start the bot
bot.run(token)
