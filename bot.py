import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHALLENGE_CHANNEL = 1192740543042682890
ADMIN = 885074776467578900

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# cateva poze cu iele
poze_cu_iele = [
    "https://www.fanatik.ro/wp-content/thumbnails/yfKwS-Gk2jg7ZnW7Z7qj7nXQuXY=/1200x0/smart/filters:contrast(5):format(jpeg):quality(80)/wp-content/uploads/2023/06/iele.jpg",
    "https://i.pinimg.com/originals/3e/dd/d2/3eddd2d60457b71887d96a4bec8b59ac.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTBkKYBAAlnLVtpdaU7hTBDXbiF_h0GxOWTHw&s",
    "https://miro.medium.com/v2/resize:fit:1200/1*zlHUbLwIRnBkPPDCG_9cUQ.jpeg",
    "https://i.ytimg.com/vi/tItT6uyE4lU/maxresdefault.jpg",
    "https://miro.medium.com/v2/resize:fit:1400/1*hVhsJ8ZhOGQn3idWpoFt2w.jpeg"
]

# Lista de întrebări și răspunsuri pentru trivia
trivia_data = [
    {"question": "Care este capitala Franței?", "answer": "Paris"},
    {"question": "Cine a scris 'Romeo și Julieta'?", "answer": "William Shakespeare"},
    {"question": "Care este simbolul chimic pentru apa?", "answer": "H2O"},
    {"question": "Care este cea mai înaltă mamiferă?", "answer": "Girafa"},
    {"question": "În ce an s-a scufundat Titanicul?", "answer": "1912"}
]

correct_answer = ""

@bot.command(name="iele", help="Îți arată niște iele")
async def iele(ctx):
    await ctx.send(random.choice(poze_cu_iele))

@bot.command(name="challenge", help="Face un challenge")
async def challenge(ctx, query, ans):
    if ctx.author.id != ADMIN:
        return
    global correct_answer
    correct_answer = str(ans)
    channel = bot.get_channel(CHALLENGE_CHANNEL)
    await channel.send(query)

@bot.command(name="answer", help="Să dai răspunsul la challenge")
async def answer(ctx, ans):
    global correct_answer
    if ans != correct_answer:
        await ctx.send("WA")
    else:
        await ctx.send("AC")

@bot.command(name="trivia", help="Începe un joc de trivia")
async def trivia(ctx):
    # Alegem o întrebare aleatorie
    trivia_question = random.choice(trivia_data)
    question = trivia_question["question"]
    global correct_answer
    correct_answer = trivia_question["answer"]
    
    await ctx.send(f"Întrebare: {question}")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        response = await bot.wait_for("message", check=check, timeout=15.0)
    except asyncio.TimeoutError:
        await ctx.send("Timpul a expirat! Răspunsul corect era: " + correct_answer)
    else:
        if response.content.strip().lower() == correct_answer.lower():
            await ctx.send("Răspuns corect!")
        else:
            await ctx.send("Răspuns incorect. Răspunsul corect era: " + correct_answer)

bot.run(TOKEN)
