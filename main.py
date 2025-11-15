import discord
from discord.ext import commands
import re
import os


intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


scam_patterns = [
    r"free\s*krypton",
    r"krypton\s*crack", # most of the sentences are hidden to avoid bypasses. these are two examples and you will have to manually add more.
]


compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in scam_patterns]

def contains_scam_pattern(content):
    """Check if message contains any scam patterns"""
    return any(pattern.search(content) for pattern in compiled_patterns)



@bot.event
async def on_ready():
    activity = discord.Game(name="Made By Starrydev")
    await bot.change_presence(activity=activity)
    print(f"Bot logged in as {bot.user}")
    print(f"Monitoring for Krypton scam messages...")

@bot.event
async def on_message(message):

    if message.author.bot:
        return
    if contains_scam_pattern(message.content):
        print(f"Detected potential scam from {message.author}: {message.content}")
        
        try:

            embed = discord.Embed(
                title="Fake Krypton cracks are the oldest trick in the book.",
                description="If you find a \"free krypton\" that isn't from TwoNick (aka prestige) you've got yourself a rat.",
                color=0x00FF00  
            )
            embed.set_footer(text="powered by sakura developpment")
            

            view = discord.ui.View()
            view.add_item(discord.ui.Button(
                label="Download Safe Krypton Crack By TwoNick",
                url="https://web.archive.org/web/20250818192137/https://kryptonclient.com/",
                style=discord.ButtonStyle.link
            ))
            view.add_item(discord.ui.Button(
                label="Buy Krypton License",
                url="https://kryptonclient.sell.app/",
                style=discord.ButtonStyle.link
            ))

            await message.reply(embed=embed, view=view)
            print(f"Sent warning reply to {message.author}")
            
        except Exception as e:
            print(f"Error sending warning message: {e}")
    

    await bot.process_commands(message)

# Run the bot
TOKEN = os.getenv("DISCORD_BOT_TOKEN") or "Enter your discord bot token here"
bot.run(TOKEN)
