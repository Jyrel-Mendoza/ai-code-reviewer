import discord
from discord.ext import commands
from analyzer.code_analyzer import CodeAnalyzer
from llm.openai_review import OpenAIReviewer

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Logged in as {bot.user}")

@bot.command()
async def review(ctx):
    if not ctx.message.attachments:
        await ctx.send("📂 Please attach a Python file.")
        return

    attachment = ctx.message.attachments[0]
    file_content = await attachment.read()
    code = file_content.decode("utf-8")

    analyzer = CodeAnalyzer()
    lint_results = analyzer.analyze_file(attachment.filename)
    reviewer = OpenAIReviewer()

    feedback = reviewer.review(code, lint_results)
    await ctx.send(f"📋 **AI Feedback**\n```{feedback[:1900]}```")

bot.run("YOUR_DISCORD_TOKEN")
