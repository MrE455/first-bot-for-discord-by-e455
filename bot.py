import discord
from discord.ext import commands
import os

PREFIX = '!'
token = os.environ.get('TOKEN')
ID_Channel = os.environ.get('IDCHANNEL')
ID_ROLE = os.environ.get('IDROLE')

client = commands.Bot(command_prefix = PREFIX)
# Бот будет реагировать на комманды начинающиеся с "!".
@client.remove_command('help')
# Удаляет стандартную команду 'help'.

@client.event

async def on_ready():
	print('[LOG]BOT was connected.')
	await client.change_presence(status = discord.Status.online, activity = discord.Game('симулятор интеллекта'))
# Пишет в консоль, что БОТ был подключен.
# Показывает статус БОТа.

@client.event

async def on_command_error(ctx, error):
	pass
# Возможность работать с ошибками.

@client.event

async def on_member_join(member):
	channel = client.get_channel(int(ID_Channel))
	role = discord.utils.get(member.guild.roles, id = int(ID_ROLE))
	await member.add_roles(role)
	await channel.send(embed = discord.Embed(description = f'Пользователь ``{member.name}`` присоединился к нам!', color = 0xFFD966))
# Получение роли "User".

@client.command()
@commands.has_permissions(kick_members = True)

async def clear(ctx, amount = 50):
	await ctx.channel.purge(limit = amount)
# Если есть права администратора, то удаляет сообщения (по стандарту 50) но с учётом комманды, то есть для удаления уже существующих двух сообщений, необходимо прописать: "!clear 3".

@client.command()
@commands.has_permissions(kick_members = True)

async def kick(ctx, member: discord.Member, *, reason = ''):
	await ctx.message.delete()
	await member.kick(reason = reason)
	await ctx.send(f'{member.mention} был кикнут по причине: ' + reason)
# Если есть права администратора, то кикает определённого пользователя и выводит текст об этом в чат.

@client.command()
@commands.has_permissions(administrator = True)

async def ban(ctx, member: discord.Member, *, reason = ''):
	await ctx.message.delete()
	await member.ban(reason = reason)
	await ctx.send(f'{member.mention} был забанен по причине: ' + reason)
# Если есть права администраторо, то банет определённого пользователя и выводит текст об этом в чат.

@client.command()

async def help (ctx):
	await ctx.message.delete()
	emb = discord.Embed(title = 'Список комманд данного сервера:', colour = discord.Color.dark_gold())
	emb.add_field(name = '{}clear'.format(PREFIX), value = '(ВНИМАНИЕ только для MODER и выше) Удаляет указанное пользователем число сообщений (по стандарту 50), с учётом сообщения с командой. Пример: !clear 12')
	emb.add_field(name = '{}kick'.format(PREFIX), value = '(ВНИМАНИЕ только для MODER и выше) Кикакет определённого пользователя с сервера. Пример: !kick @LOX')
	emb.add_field(name = '{}ban'.format(PREFIX), value = '(ВНИМАНИЕ только для ADMINISTRATOR) Банет определённого пользователя на сервере. Пример: !ban @LOX')
	emb.add_field(name = '{}vk'.format(PREFIX), value = 'Ссылка на ВК автора.')
	emb.add_field(name = '{}telegram'.format(PREFIX), value = 'Ссылка на телеграм автора.')
	emb.add_field(name = '{}get_message'.format(PREFIX), value = 'Получить сообщение от бота.')
	emb.add_field(name = '{}send_to'.format(PREFIX), value = '(ВНИМАНИЕ только для MODER и выше) Поприветствовать пользователя через бота. Пример: !send_to @LOX')
	await ctx.send(embed = emb)
# Список команд сервера.

@client.command()

async def vk (ctx):
	await ctx.message.delete()
	emb = discord.Embed(title = 'Vk:', colour = discord.Color.red())
	emb.set_footer(text = client.user.name, icon_url = client.user.avatar_url)
	emb.set_thumbnail(url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/VK.com-logo.svg/250px-VK.com-logo.svg.png')
	emb.add_field(name = "Ссылка:", value = "https://vk.com/mr_e455")
	await ctx.send(embed = emb)
# Ссылка на Вконтакте.

@client.command()

async def telegram (ctx):
	await ctx.message.delete()
	emb = discord.Embed(title = 'Telegram', colour = discord.Color.dark_red())
	emb.set_footer(text = client.user.name, icon_url = client.user.avatar_url)
	emb.set_thumbnail(url = 'https://upload.wikimedia.org/wikipedia/commons/5/5c/Telegram_Messenger.png')
	emb.add_field(name = "Имя:", value = "@mr_e455")
	await ctx.send(embed = emb)
# Ссылка на Телеграм.

@client.command()

async def get_message(ctx):
	await ctx.message.delete()
	await ctx.author.send('Лучший код автора: BRFF')
# Отправляет текст пользователю который ввёл команду.

@client.command()
@commands.has_permissions(kick_members = True)

async def send_to(ctx, member: discord.Member):
	await ctx.message.delete()
	await member.send(f'{member.name}, привет от {ctx.author.name}')
#Приветствует через БОТа.

@clear.error

async def clear_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.message.delete()
		await ctx.send(f'{ctx.author.name}, у вас не достаточно прав для использования данной команды.')
# Говорит пользователю что у него недостаточно прав.

@kick.error

async def kick_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.message.delete()
		await ctx.send(f'{ctx.author.name}, у вас не достаточно прав для использования данной команды.')
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.message.delete()
		await ctx.send(f'{ctx.author.name}, необходимо ввести пользователя. Пример: !kick @LOX')
# Говорит пользователю что у него недостаточно прав.
# Говорит что необходимо ввести пользователя.

@ban.error

async def ban_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.message.delete()
		await ctx.send(f'{ctx.author.name}, у вас не достаточно прав для использования данной команды.')
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.message.delete()
		await ctx.send(f'{ctx.author.name}, необходимо ввести пользователя. Пример: !ban @LOX')
# Говорит пользователю что у него недостаточно прав.
# Говорит что необходимо ввести пользователя.

@send_to.error

async def send_to_error(ctx, error):
	if isinstance(error, commands.MissingPermissions):
		await ctx.message.delete()
		await ctx.send(f'{ctx.author.name}, у вас не достаточно прав для использования данной команды.')
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.message.delete()
		await ctx.send(f'{ctx.author.name}, необходимо ввести пользователя. Пример: !send_to @LOX')
# Говорит пользователю что у него недостаточно прав.
# Говорит что необходимо ввести пользователя.

client.run(str(token))
# Подключение БОТа.