import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Discord intents
intents = discord.Intents.default()
intents.message_content = True  # Required for command content
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Owners and Hosts
OWNERS = {429646883359817748}  # Your Discord ID
hosts = set()

# Available games
GAMES = ["poker"]

# --- Utility Functions ---
def is_owner(user_id):
    return user_id in OWNERS

def is_host(user_id):
    return user_id in hosts or is_owner(user_id)

# --- Bot Events ---
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# --- Commands ---
@bot.command()
async def games(ctx):
    """List available games"""
    await ctx.send("🎮 Available games:\n" + "\n".join(GAMES))

@bot.command()
async def start_game(ctx, game_name: str):
    """Start a game if user is host"""
    if not is_host(ctx.author.id):
        await ctx.send("❌ Only hosts can start games!")
        return
    if game_name.lower() not in GAMES:
        await ctx.send(f"❌ Game `{game_name}` not found!")
        return
    await ctx.send(f"✅ Starting game: {game_name}")

@bot.command()
async def add_host(ctx, member: discord.Member):
    if not is_owner(ctx.author.id):
        await ctx.send("❌ Only owners can add hosts.")
        return
    hosts.add(member.id)
    await ctx.send(f"✅ {member.display_name} is now a host.")

@bot.command()
async def del_host(ctx, member: discord.Member):
    if not is_owner(ctx.author.id):
        await ctx.send("❌ Only owners can remove hosts.")
        return
    hosts.discard(member.id)
    await ctx.send(f"✅ {member.display_name} is no longer a host.")

# Test Mode (owners only)
@bot.command()
async def test_mode(ctx):
    if not is_owner(ctx.author.id):
        await ctx.send("❌ Test mode is restricted to owners.")
        return
    await ctx.send("🔧 Test mode active. Debugging enabled for games.")

bot.run(TOKEN)
