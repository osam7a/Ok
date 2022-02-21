from disnake import File, Member
from disnake import Colour
from disnake import Embed

import requests
color = Colour.blue()

class aobject(object):
    """Inheriting this class allows you to define an async __init__.

    So you can create objects by doing something like `await MyClass(params)`
    """
    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self):
        pass

def get(host, endpoint, params: dict):
    knownHosts = {'sra': 'some-random-api.ml'}
    request = requests.get(f"https://{knownHosts[host] if knownHosts[host] else host}{endpoint}", params = params)
    return request
        
async def emb(ctx, message, user = None, colorarg = None, **kwargs):
        user = user or ctx.author
        emb = Embed(
            description=message,
            color=colorarg or color,
        ).set_footer(text = f"{user}", icon_url = user.avatar.url)
        return await ctx.send(embed = emb)

async def sendOverlay(ctx, endpoint, params: dict, user: Member):
    user = user or ctx.author
    prms = ""
    for _i, v in enumerate(params):
        if len(params) > 0:
            prms += f"{'?' if _i == 0 else '&'}{v}={params[v].replace(' ', '+')}"
    url = f"https://some-random-api.ml{endpoint}{prms}"
    await ctx.send(embed = Embed(color = color).set_author(name = user, icon_url = user.avatar.url).set_image(url = url))