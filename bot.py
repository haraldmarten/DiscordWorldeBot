import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

WORDLE_WORD = ""
WORDLE_GUESSES = 0


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def wordle(ctx):
    with open("words.txt") as wordlist:
        global WORDLE_WORD
        WORDLE_WORD = (wordlist.read().splitlines())[random.randrange(0, 2315)]
        await ctx.send(f"{ctx.author} has started a wordle. You have 6 guesses")

@bot.command()
async def guess(ctx, word):
    global WORDLE_WORD
    if WORDLE_WORD == "":
        return
    if len(word) != 5 or word.isalpha() == False:
        await ctx.send("Invalid input. The word must conain 5 characters and only letters (A-Z)")
        return
    with open("words.txt") as wordlist:
        if word not in wordlist.read().splitlines():
            await ctx.send("Invlaid input. The word is not in the english dictionary.")
            return
    global WORDLE_GUESSES
    score = ""
    for index, char in enumerate(word):
        if char == WORDLE_WORD[index]:
            score += ":green_square: "
        elif char in WORDLE_WORD:
            score += ":yellow_square: "
        else:
            score += ":red_square: "
    WORDLE_GUESSES += 1
    await ctx.send(score)
    if score == ":green_square: :green_square: :green_square: :green_square: :green_square: ":
        await ctx.send(f"You win. The word was {WORDLE_WORD}")
        WORDLE_WORD = ""
        return
    if WORDLE_GUESSES >= 6:
        await ctx.send(f"You lose. The word was {WORDLE_WORD}")
        WORDLE_WORD = ""
        return
    await ctx.send(f"Guesses left: {6 - WORDLE_GUESSES}")

bot.run(TOKEN)