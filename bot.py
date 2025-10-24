import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from poker import PokerGame
from ocr import OCRSystem

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Owners - Discord IDs
OWNERS = ["429646883359817748"]  # replace/add other owner IDs here

# Hosts will be tracked dynamically
hosts = set()

# Active game instances
active_games = {}

# Helper: check if user is owner
def is_owner(ctx):
    return str(ctx.author.id) in OWNERS

# Helper: check if user is host
def is_host(ctx):
    return str(ctx.author.id) in hosts

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Owner commands
@bot.command()
@commands.check(is_owner)
async def add_host(ctx, member: discord.Member):
    hosts.add(str(member.id))
    await ctx.send(f"✅ {member.display_name} added as host.")

@bot.command()
@commands.check(is_owner)
async def del_host(ctx, member: discord.Member):
    hosts.discard(str(member.id))
    await ctx.send(f"✅ {member.display_name} removed from hosts.")

# Game selection
@bot.command()
async def games(ctx):
    msg = "🎮 Available games:\n"
    msg += "- Poker\n"
    await ctx.send(msg)

# Start a game
@bot.command()
@commands.check(is_host)
async def start_game(ctx, game_name: str):
    game_name = game_name.lower()
    if game_name == "poker":
        active_games[ctx.channel.id] = PokerGame()
        await ctx.send("🃏 Poker game started!")
    else:
        await ctx.send("❌ Unknown game.")

# Test/debug mode (owners only)
@bot.command()
@commands.check(is_owner)
async def test_mode(ctx, game_name: str):
    game_name = game_name.lower()
    if game_name == "poker":
        await ctx.send("🧪 Test mode active for Poker!")
        # Optional: call PokerGame.test_mode() here
    else:
        await ctx.send("❌ Unknown game.")

bot.run(TOKEN)
