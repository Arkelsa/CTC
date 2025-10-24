import os
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Bot setup
intents = commands.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Import game(s)
from games.poker import PokerGame
poker = PokerGame()

# Command: List games
@bot.command()
async def games(ctx):
    await ctx.send("🎮 Available games:\n- Poker")

# Command: Start game
@bot.command()
async def start(ctx, game_name: str):
    if game_name.lower() == "poker":
        await poker.start(ctx)
    else:
        await ctx.send("❌ Game not found.")

# Command: Test mode (owners only)
@bot.command()
async def test(ctx, game_name: str):
    owners = [429646883359817748]  # Add more Discord IDs as needed
    if ctx.author.id not in owners:
        await ctx.send("❌ You do not have permission to use test mode.")
        return
    if game_name.lower() == "poker":
        await poker.test_mode(ctx)
    else:
        await ctx.send("❌ Game not found for test mode.")

# Run bot
bot.run(TOKEN)
