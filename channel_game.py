import discord
from spellchecker import SpellChecker
import aiohttp
import urllib


class ChannelGame:
    def __init__(self):
        self.words = []
        self.spellchecker = SpellChecker()
        self.session = aiohttp.ClientSession()

    async def on_message(self, message: discord.Message):
        print(f"Message received: {message.content}")
        word = message.content.strip().lower()
        if not word:
            return
        if word.lower() in self.words:
            await message.add_reaction("🤥")
        elif await self.is_known_word(word):
            self.words.append(word.lower())
            await message.add_reaction("✅")
        else:
            await message.add_reaction("❌")

    async def is_known_word(self, word: str):
        return self.spellchecker.known([word]) or await self.is_in_wiktionary(word)

    async def is_in_wiktionary(self, word: str):
        url = f"https://en.wiktionary.org/w/index.php?search={urllib.parse.quote_plus(word)}&go=Go"
        response = await self.session.get(url)
        return str(response.url).startswith("https://en.wiktionary.org/wiki/")

    async def stop(self, message: discord.Message):
        await message.reply(self.get_finishing_reply())
        await self.session.close()

    def get_finishing_reply(self):
        result = f"Total words count is {len(self.words)}:"
        for word in self.words:
            result += f"\n• {word}"
        return result
