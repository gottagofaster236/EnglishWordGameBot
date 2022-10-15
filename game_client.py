import discord
from channel_game import ChannelGame


START_COMMAND = "!start_game"
END_COMMAND = "!end_game"


class GameClient(discord.Client):
    def __init__(self, managing_roles: list[str]):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.members = True
        super(GameClient, self).__init__(intents=intents)

        self.managing_roles = managing_roles
        self.channel_games = {}

    async def on_ready(self):
        print(f'{self.user} connected.')

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if await self.check_start_stop(message):
            return
        channel_game = self.channel_games.get(message.channel)
        if channel_game:
            await channel_game.on_message(message)

    async def check_start_stop(self, message: discord.Message):
        content = message.content.replace(" ", "").lower()
        is_start = content == START_COMMAND
        is_stop = content == END_COMMAND
        if not is_start and not is_stop:
            return False
        if not self.is_managing_member(message.author):
            await message.reply(f"Have to have one of the following roles "
                                f"to manage the bot: {', '.join(self.managing_roles)}")
            return True

        if is_start:
            if message.channel in self.channel_games:
                await message.reply(f"Game already started. End it with {END_COMMAND}")
                return True
            self.channel_games[message.channel] = ChannelGame()
            await message.reply("Game started!")
        elif is_stop:
            if message.channel not in self.channel_games:
                await message.reply(f"Game has not been started. Start it with {START_COMMAND}")
                return True
            await self.channel_games[message.channel].stop(message)
            del self.channel_games[message.channel]
        return True

    def is_managing_member(self, member: discord.Member):
        for role in member.roles:
            if role.name in self.managing_roles:
                return True
        return False

    async def handle_start_or_stop(self, message: discord.Message):
        pass
