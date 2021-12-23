import discord
import json
import commands
import util

bot_config = None
runtimes = None
client = None

class config:
    def __init__(self, t, p, bdr, sar, rc, rr):
        self.token = t
        self.prefix = p
        self.bot_dev_role = bdr
        self.server_admin_role = sar
        self.reminder_channel = rc
        self.reminder_role = rr

class bot_user(discord.Client):
    async def on_ready(self):
        print(f'Now logged in as {self.user}')
    async def on_message(self, message):
        if message.content.startswith(bot_config.prefix):
            command = message.content[1:].split(' ')
            args = command[1:]
            sender_allowed_elevated_commands = bot_config.bot_dev_role.lower() in [r.name.lower() for r in message.author.roles] or bot_config.server_admin_role.lower() in [r.name.lower() for r in message.author.roles]
            if command[0] == 'runtimes':
                await message.channel.send(commands.get_runtimes.get_runtimes_api())
            elif command[0] == "help":
                await message.channel.send(commands.get_help.send_help())
            elif command[0] == "run":
                await message.channel.send(commands.run_code.run_code(args, runtimes))
            elif command[0] == "inspiration" or command[0] == "inspire" or command[0] == "motivation":
                await message.channel.send(commands.inspiration.inspire())
            elif command[0] == "remind" and sender_allowed_elevated_commands:
                chan = discord.utils.get(message.guild.channels, name=bot_config.reminder_channel)
                await message.channel.send(await commands.remind.remind_users(chan, bot_config.reminder_role, args[0], args[1], args[2]))
            else:
                await message.channel.send("Unknown command.")
                print(f'Unhandled command: {command[0]} - args: {args}')



def reminder_loop():
    print('remind')


def main():
    global bot_config
    global runtimes
    global client

    print('Omenbot V2')
    print('Parsing Configuration')
    config_file = open('config.json', 'r')
    c = json.load(config_file)
    bot_config = config(c['token'], c['prefix'], c['bot_dev_role'], c['admin_role'], c['reminder_channel_name'], c['reminder_role'])
    print('Getting available command runtimes')
    runtimes = util.get_runtimes.create_classes()
    discord_client = bot_user()
    discord_client.run(bot_config.token)
    client = discord_client

if __name__ == "__main__":
    main()
