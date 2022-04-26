from __future__ import annotations
from disnake.ext import commands, tasks
import os
from dotenv import load_dotenv  # need to install python-dotenv for this
import disnake
from datetime import datetime, time
from dotenv import find_dotenv

TIMES = [
    time(4),
    time(10),
    time(1),
]

DAY_MESSAGE_MAPS = [
    {  # MON
        1: "Guild war has started!",  # index 1: 7 AM
    },
    {  # TUE
        0: "Guild war ends in 6 hours! <@&945164154862448672>",  # index 0: 1 AM
        1: "Guild war has ended!",  # index 1: 7 AM
    },
    {  # WED
        1: "Guild war has started!",  # index 1: 7 AM
        2: "Maintenance starts in 2 hours! Make sure to use your guild war attacks before then! <@&945164154862448672>",
        # Maintenance starts in 2 hours! Make sure to use your guild war attacks before then!(1)
        # Guild war ends in 9 hours!(No maintenance today) (1)
    },
    {  # THU
        1: "Guild war has ended!",  # index 1: 7 AM
    }, *
    {  # FRI
        1: "Guild war has started!",  # index 1: 7 AM
    },
    {  # SAT
        0: "Guild war ends in 6 hours! <@&945164154862448672>",  # index 0: 1 AM
        1: "Guild war has ended!",  # index 1: 7 AM
    },
    {}  # SUN, do nothing
]

print(find_dotenv())

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # start the task to run in the background
        self.myloop.start()

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("The bot is running")

    @tasks.loop(time=TIMES)
    async def myloop(self):
        weekday = datetime.now().weekday()
        next_time = self.myloop.next_iteration.time()
        current_index = (TIMES.index(next_time) - 1) % len(TIMES)

        msg = DAY_MESSAGE_MAPS[weekday].get(current_index)
        if msg is None:
            return

        await self.channel.send(msg)

    @myloop.before_loop
    async def before_myloop(self):
        await self.wait_until_ready()
        channel = await self.fetch_channel(652808067347513344)
        if not isinstance(channel, disnake.TextChannel):
            raise ValueError("Invalid channel")

        self.channel = channel


client = MyBot()

bot = MyBot(command_prefix=">", reload=True)


@bot.command(name="next")
async def nextloop(ctx: commands.Context):
    dt = bot.myloop.next_iteration
    await ctx.send(content=f"Next guild war warning time {dt.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(bot.myloop.next_iteration)

load_dotenv("C:/Users/user/PycharmProjects/untitled2/dot.env")
token = os.environ["MINT"]
bot.load_extension("somecommands")

bot.run(token)
