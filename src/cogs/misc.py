import asyncio
import random
import aiohttp
from disnake import Color, Embed, Member
from disnake.ext.commands import Cog, command, Context
import requests
from ..utils.utils import emb, get
from art import text2art

class Misc(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @staticmethod
    def get_lang(code):
        if code.startswith("```py"):
            return "python"
        elif code.startswith("```js"):
            return "javascript"
        elif code.startswith("```cs"):
            return "csharp"
        elif code.startswith("```c"):
            return "c"
        elif code.startswith("```cpp"):
            return "cpp"
        elif code.startswith("```java"):
            return "java"
        else:
            return "invalid"
    
    @staticmethod
    def clean_code(code):
        if code.startswith("```py") or code.startswith("```js") or code.startswith("```cs"):
            code = code[5:-3]
        elif code.startswith("```c"):
            code = code[4:-3]
        elif code.startswith("```java"):
            code = code[7:-3]
        elif code.startswith("```cpp"):
            code = code[6:-3]
        return code


    @command()
    async def execute(self, ctx, *, code):
        lang = self.get_lang(code)
        if lang == "invalid":
            await ctx.send(embed = Embed(description = f"Available languages:\n- python\n- javascript\n- csharp (c#)\n- c\n- java\n- cpp\nDM osam7a#1017 for language suggestions", color = Color.red()))
            await ctx.send(embed = Embed(description = f"How to use:\nUse codeblocks, three back ticks (`) at the beginning, then write the name of the language you want, then new line and type your code, then new line at the last part, type another three backticks but without the language", color = Color.red()))
            return
        cleaned_code = self.clean_code(code)
        request = requests.post("https://emkc.org/api/v1/piston/execute", json = {"language": lang, "source": cleaned_code})
        try:
            await emb(ctx, f"```\n{request.json()['output']}\n```")
        except:
            await ctx.send("something went wrong...")

    @command()
    async def textart(self, ctx: Context, *, message):
        if len(ctx.message.mentions) >= 1:
            return await ctx.send("Mentions are not allowed. Only ASCII characters ([A-Z0-9!@#$%^&*(){}[]/])")
        await ctx.send(f"```\n{'shortened text (less than 15)' if len(message) > 15 else ''}\n{text2art(message if len(message) < 15 else message[:15])}\n```")

    @command()
    async def binary(self, ctx, encodeordecode, *, message):
        if encodeordecode.lower() == "encode":
            result = get('sra', '/binary', {"encode": message}).json()['binary']
        elif encodeordecode.lower() == "decode":
            result = get('sra', '/binary', {"decode": message}).json()['text']
        return await emb(ctx, f"```\n{result}\n```")
    
    @command()
    async def roast(self, ctx, *, user: Member = None):
        user = user or ctx.author
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://evilinsult.com/generate_insult.php?lang=en&type=json") as resp:
                _json = await resp.json()
                return await emb(ctx, _json['insult'])

    @command()
    async def hack(self, ctx, *, user: Member = None):
        user = user or ctx.author
        async with aiohttp.ClientSession() as cs:
          async with cs.get(f"https://randomuser.me/api/", headers = {"Content-Type":"application/json"}) as resp:
            _user = await resp.json()
            _user = _user['results'][0]
          async with cs.get("https://www.themealdb.com/api/json/v1/1/random.php") as resp:
              _food = await resp.json()
              _food = _food['meals'][0]

        nouns = ["bird", "clock", "boy", "plastic", "duck", "teacher", "old lady", "professor", "hamster", "dog"];
        verbs = ["kicked", "ran", "flew", "dodged", "sliced", "rolled", "died", "breathed", "slept", "killed"];
        adjectives = ["beautiful", "lazy", "professional", "lovely", "dumb", "rough", "soft", "hot", "vibrating", "slimy"];
        adverbs = ["slowly", "elegantly", "precisely", "quickly", "sadly", "humbly", "proudly", "shockingly", "calmly", "passionately"];
        preposition = ["down", "into", "up", "on", "upon", "below", "above", "through", "across", "towards"]
    
        sentence = f"The {random.choice(adjectives)} {random.choice(nouns)} {random.choice(adverbs)} {random.choice(verbs)} {random.choice(preposition)} the {random.choice(nouns)}"
        name = _user['name']['first'] + " " + _user['name']['last']
        sentences = {
            "Name: ": name,
            "Instagram User: ": _user['login']['username'],
            "Instagram Password: ": _user['login']['password'],
            "Phone Number: ": _user['phone'],
            "Age: ": _user['dob']['age'],
            "Finding Country.... ": _user['location']['country'],
            "Likes turtles? ": random.choice(['Yes', 'No']),
            "Broken Table? ": random.choice(['Yes', 'No']),
            f"`{user}.fetch_last_dm()` ": sentence,
            "Favorite food: ": _food['strMeal'],
            f"`{user}.is_racist()` ": random.choice(['Yes', 'No']),
            "is hot? ": random.choice(['Yes', 'No']),
            "Gay? ": random.choice(['Yes', 'No']),
            "Favorite Sport: ": random.choice(['football', 'soccer', 'basketball', 'volleyball', 'tennis'])
        }
    
        msg = await emb(ctx, f"Hacking {user.mention}...")
        await asyncio.sleep(1.5)
        for k, v in sentences.items():
            await msg.edit(embed = Embed(title = f"{k}", color = self.bot.color))
            await asyncio.sleep(1.25)
            await msg.edit(embed = Embed(title = f"{k}", description = v, color = self.bot.color))
            await asyncio.sleep(1.25)
        await msg.edit(content = f"The totally real hack just finished...")

def setup(bot):
    bot.add_cog(Misc(bot))