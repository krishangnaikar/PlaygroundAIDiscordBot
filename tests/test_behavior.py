import asyncio
import runpy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, AsyncMock, patch

def load():
    bot = SimpleNamespace(command=lambda:lambda fn:fn)
    discord = MagicMock()
    discord.ext.commands.Bot.return_value = bot
    selenium = MagicMock()
    dependencies = {'discord':discord,'discord.ext':discord.ext,'discord.ext.commands':discord.ext.commands,'Selenuim':selenium,'Selenuim.playgroundaiCom':selenium.playgroundaiCom}
    with patch.dict('sys.modules',dependencies):
        module = runpy.run_path(str(Path(__file__).resolve().parents[1] / 'Commands/commandBot.py'))
    return module, discord, selenium

def test_imagine_joins_prompt_uploads_file_and_removes_it():
    module, discord, selenium = load()
    selenium.playgroundaiCom.create_image.return_value = 'test-image.png'
    ctx = SimpleNamespace(send=AsyncMock())
    with patch('os.remove') as remove:
        asyncio.run(module['imagine'](ctx,'blue','sky'))
    selenium.playgroundaiCom.create_image.assert_called_once_with('blue sky')
    discord.File.assert_called_once_with('test-image.png')
    ctx.send.assert_awaited_once_with(file=discord.File.return_value)
    remove.assert_called_once_with('test-image.png')

def test_failed_generation_sends_error_without_deleting_file():
    module, discord, selenium = load()
    error = 'An Error Occured, Please try again'
    selenium.playgroundaiCom.create_image.return_value = error
    ctx = SimpleNamespace(send=AsyncMock())
    with patch('os.remove') as remove:
        asyncio.run(module['imagine'](ctx,'sky'))
    ctx.send.assert_awaited_once_with(error)
    remove.assert_not_called()
    discord.File.assert_not_called()
