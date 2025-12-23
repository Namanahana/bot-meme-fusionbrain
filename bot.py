import discord
from discord.ext import commands
import os
from ai import FusionBrain
from config import TOKEN

# setup bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

ai = FusionBrain()

@bot.event
async def on_ready():
    print(f"✅ Bot login sebagai {bot.user}")

def build_prompt(topic):
    return f"""
    funny cartoon meme illustration,
    exaggerated facial expression,
    simple background,
    humorous situation: {topic}
    """

@bot.command()
async def meme(ctx, *, topic: str):
    await ctx.send("🎨 Lagi bikin meme... sabar ya 😄")

    try:
        prompt = build_prompt(topic)
        img_base64 = ai.generate_image(prompt)

        os.makedirs("output", exist_ok=True)
        filename = "output/meme.png"

        ai.save_base64_image(img_base64, filename)

        await ctx.send(
            content=f"😂 **{topic.upper()}**",
            file=discord.File(filename)
        )

    except Exception as e:
        await ctx.send("❌ Gagal bikin meme 😭")
        print("ERROR:", e)

bot.run(TOKEN)
