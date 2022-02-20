import disnake
from disnake.ext import commands
import contextlib
import io
import textwrap
from traceback import format_exception

def clean_code(content:str):
    if content.startswith("```py"):
        content = content[5:-3]
    return content


async def run_eval(ctx, code, **kwargs):
    _eval = kwargs.get('_eval')
    msg = ''
    local_variables = {
        "disnake": disnake,
        "commands": commands, 
        "bot": ctx.bot, 
        "client": ctx.bot,
        "ctx": ctx, 
        "channel": ctx.channel, 
        "author": ctx.author,
        "guild": ctx.guild,
        "message": ctx.message

    }
    
    code = clean_code(code)
    stdout = io.StringIO()

    pref = ctx.prefix
    message = clean_code(ctx.message.content[len(pref) -1:])

    if _eval == 'dir':
        code = f"print(dir({code}))"
            
    elif _eval == 'return':
        code = f"return {code}"
    
        
    try:
        with contextlib.redirect_stdout(stdout):
            exec(
                f"async def func():\n{textwrap.indent(code, '    ')}",  local_variables, 
            )
            obj = await local_variables["func"]()
        
            result = f"{stdout.getvalue()}{obj}\n"
    except Exception as e:
        result = "".join(format_exception(e, e, e.__traceback__))
        pass
   
    result = result.replace('`', '')
    message = message.replace('`', '')
    if result.replace('\n', '').endswith('None') and result != "None":
        result = result[:-5]
    if len(result) < 2000:
        status = '200' if not result.startswith('Traceback') else '400'
        msg = f"Evaluation ended with status code: {status}```ini\n[in]``````py\n{message}``````{'diff' if status == '400' else 'ini'}\n{'- ' if status == '400' else ''}[out]``````yaml\n{result}\n```"
    return msg    