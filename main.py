import discord
from discord.ext import commands
import json, os
import asyncio

class util:
    @staticmethod
    def get_config():
        with open("config.json") as f:
            return json.load(f)

    @staticmethod
    def load():
        os.system("cls")
        os.system("title github.com/githubdontbanmeagain")

config = util.get_config()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = commands.Bot(command_prefix=config["bot prefix"], intents=intents, help_command=None)

async def dmall(ctx, guild_id, emoji, max_members=100):
    guild = bot.get_guild(guild_id)
    if guild is None:
        await ctx.send(f"Guild with ID {guild_id} not found")
        return

    log_channel = bot.get_channel(int(config["log channel id"]))
    if log_channel is None:
        print(f"Log channel with ID {config['log channel id']} not found")
        return

    sent_count = 0
    total_members = sum(1 for member in guild.members if not member.bot and member.status != discord.Status.offline)
    print(f"/ | {total_members} members fetched")

    for i, member in enumerate(guild.members):
        if not member.bot and member.status != discord.Status.offline:
            message = config["dm message"]
            if config["mention in dm"].lower() == "yes":
                message += f" {member.mention}. To Claim The Nitro Click ON That Claim Button And Join The Server And Wait 5 - 10Hrs."

            view = discord.ui.View()
            view.add_item(item=discord.ui.Button(style=discord.ButtonStyle.gray, label=config["button text"], url=config["site link"], emoji=emoji))
            try:
                await member.send(content=message, file=discord.File(config["image path"]), view=view)
                sent_count += 1
                if sent_count >= max_members:
                    break
                if sent_count % 10 == 0:  # Her 10 mesajda bir log gönder
                    await log_channel.send(f"Sent message to {sent_count} of {max_members} members")
                print(f"+ | {member.name}")
            except discord.HTTPException:
                print(f"- | {member.name}")

            if sent_count >= max_members:
                break

            if (i + 1) % 10 == 0:  # Her 5 mesajdan sonra 1 saniye bekle
                await asyncio.sleep(1)

    # Tüm mesajlar gönderildikten sonra toplam sayı ile log gönder
    await log_channel.send(f"Finished sending messages to {sent_count} members out of {max_members} requested members.")

@bot.command()
async def setup(ctx, key):
    await ctx.message.delete()
    if key == config["command key"]:
        with open(config["emoji path"], "rb") as f:
            emoji_bytes = f.read()
        await ctx.guild.create_custom_emoji(name="nitro0emoji", image=emoji_bytes)

@bot.command()
async def start(ctx, key, guild_id: int):
    await ctx.message.delete()
    if key == config["command key"]:
        for emoji in ctx.guild.emojis:
            if emoji.name == "nitro0emoji":
                print("/ | Starting...")
                await dmall(ctx, guild_id, emoji)
                return
        print(f"/ | Run {config['bot prefix']}setup {config['command key']} first")

@bot.listen("on_connect")
async def ready():
    util.load()
    print("Bot is online, commands:")
    for command in bot.commands:
        print(f"    {config['bot prefix']}{command.name} {config['command key']}")

if __name__ == "__main__":
    bot.run(os.getenv('BOT_TOKEN'))
