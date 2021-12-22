from discord.ext import tasks
import discord

intents = discord.Intents.all()
intents.presences = True


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print("------")

    @tasks.loop(minutes=5.0)
    async def activity_task(self, message):
        mentions = message.mentions
        if len(mentions) == 0:
            await message.reply("Quem você quer saber que está jogando Google Chrome?!")
        else:
            activ = mentions[0].activity
            if activ == None:
                await message.reply(
                    message.mentions[0].mention
                    + " Não está jogando Google Chrome no momento"
                )
            elif activ.name == "Google Chrome":
                await message.reply("Sim")
            else:
                await message.reply("Não")

    @activity_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()

    async def on_message(self, message):
        if message.content.startswith("!chrome"):
            self.activity_task.start(message)


client = MyClient(intents=intents)
client.run("OTIzMDU4NDI4MTUzMzExMjUz.YcKfJg.IhQIC89h6Z7bKaxtP8aVfATLMxI")
