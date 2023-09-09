import discord
from discord.ext import commands
import random
import asyncio
intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)
default_intents = discord.Intents.default()
default_intents.members = True
client = discord.Client(intents = default_intents)
@bot.event
async def on_ready():
    print(f'{bot.user.name} est connecté à Discord!')

@bot.event
async def on_ready():
    await bot.change_presence (activity=discord.Game(name= "BY MOMO92i"))


@bot.command()
async def hello(ctx):
    await ctx.send('Salut! Je suis un bot Discord.')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong! Je suis là.')

@bot.command()
async def roll(ctx, dice):
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format de dés incorrect. Utilisez le format NdN, par exemple 2d6.')
        return
    
    results = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
    await ctx.send(f'Résultats des dés: {results}')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear_user_messages(ctx, user: discord.Member):
    def is_user_message(message):
        return message.author == user

    deleted_messages = await ctx.channel.purge(limit=None, check=is_user_message)
    await ctx.send(f"{len(deleted_messages)} messages ont été supprimés pour l'utilisateur {user.mention}.")

@clear_user_messages.error
async def clear_user_messages_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour supprimer des messages.")
        

@bot.command()
async def create_embed(ctx):
    embed = discord.Embed()
    await ctx.send("Embed créé. Utilisez les commandes suivantes pour le modifier :")
    await ctx.send("pour définir le titre de l'embed")
    await ctx.send("pour définir la description de l'embed")
    await ctx.send(" pour ajouter un champ à l'embed")
    await ctx.send("pour définir la couleur de l'embed")
    await ctx.send("pour définir le texte du pied de page de l'embed")

    def check(message):
        return message.author == ctx.author and message.channel == ctx.channel

    while True:
        try:
            message = await bot.wait_for('message', check=check, timeout=60)

            if message.content.startswith('!set_title'):
                title = message.content.split('!set_title ')[1]
                embed.title = title
                await ctx.send(f"Titre défini : {title}")

            elif message.content.startswith('!set_description'):
                description = message.content.split('!set_description ')[1]
                embed.description = description
                await ctx.send(f"Description définie : {description}")

            elif message.content.startswith('!add_field'):
                field = message.content.split('!add_field ')[1]
                name, value = field.split(' | ')
                embed.add_field(name=name, value=value)
                await ctx.send(f"Champ ajouté : {name} - {value}")

            elif message.content.startswith('!set_color'):
                color = message.content.split('!set_color ')[1]
                embed.color = discord.Color(int(color, 16))
                await ctx.send(f"Couleur définie : {color}")

            elif message.content.startswith('!set_footer'):
                footer = message.content.split('!set_footer ')[1]
                embed.set_footer(text=footer)
                await ctx.send(f"Pied de page défini : {footer}")

            elif message.content.startswith('!done'):
                await ctx.send("Embed finalisé.")
                await ctx.send(embed=embed)
                break

        except asyncio.TimeoutError:
            await ctx.send("Temps écoulé. Embed non finalisé.")
            break


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    ban_channel = discord.utils.get(guild.channels, name="logs-ban")  # Remplacez "logs" par le nom du salon de logs

    await member.ban(reason=reason)
    await ban_channel.send(f"{member.mention} a été banni par {ctx.author.mention}. Raison : {reason}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour bannir des membres.")
        
@bot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    guild = ctx.guild
    ban_channel = discord.utils.get(guild.channels, name="logs-unban")  # Remplacez "logs" par le nom du salon de logs

    banned_users = await guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if user.name == member:
            await guild.unban(user)
            await ban_channel.send(f"{user.name} a été débanni par {ctx.author.mention}.")
            return

    await ctx.send(f"L'utilisateur {member} n'est pas banni.")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Vous n'avez pas les permissions nécessaires pour débannir des membres.")
        

@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.channels, name="『➡』arrivant")  # Remplacez "bienvenue" par le nom du salon de bienvenue

    welcome_message = f"Bienvenue à {member.mention} sur notre serveur ! Nous sommes ravis de t'accueillir ici."

    await welcome_channel.send(welcome_message)
    
@bot.event
async def on_message(message):
    if message.author != bot.user:  # Exclure les messages du bot
        log_channel = discord.utils.get(message.guild.channels, name="logs-messages")  # Remplacez "logs" par le nom du salon de logs

        log_embed = discord.Embed(title="Message Log", description=f"Message envoyé dans {message.channel.mention}", color=discord.Color.blue())
        log_embed.add_field(name="Auteur", value=message.author.mention, inline=False)
        log_embed.add_field(name="Contenu", value=message.content, inline=False)

        await log_channel.send(embed=log_embed)

    await bot.process_commands(message)
    
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="✨ 🄲🄸🅃🄾🅈🄴🄽🅂 ✨")  # Remplacez "Nom du rôle" par le nom du rôle que vous souhaitez attribuer automatiquement

    await member.add_roles(role)

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='nom_du_salon')
    if channel:
        await channel.send(f'Bienvenue {member.mention} sur notre serveur !')
    else:
        print('Le salon spécifié n\'a pas été trouvé.')

@bot.command()
async def rank_test(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='『T』Test vigneron')
    if role:
        await member.add_roles(role)
        await ctx.send(f"Le rôle {role.name} a été ajouté à {member.mention}.")
    else:
        await ctx.send("Le rôle spécifié n'a pas été trouvé.")

@bot.command()
async def refuser(ctx):
    message = "Désolé mais votre candidature n'a pas été retenue. Veuillez réessayer une prochaine fois."
    await ctx.send(message)

@bot.command()
async def accepter(ctx):
    message = "Bienvenue parmi les vignerons. Merci de te renommer avec ton NOM+PRENOM (RP) et TON UUID."
    await ctx.send(message)

@bot.command()
async def rank_employer(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Employer Test')
    if role:
        await member.add_roles(role)
        await ctx.send(f"Le rôle {role.name} a été ajouté à {member.mention}.")
    else:
        await ctx.send("Le rôle spécifié n'a pas été trouvé.")

@bot.command()
async def rank_vigneron(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='『V』Vigneron')
    if role:
        await member.add_roles(role)
        await ctx.send(f"Le rôle {role.name} a été ajouté à {member.mention}.")
    else:
        await ctx.send("Le rôle spécifié n'a pas été trouvé.")

@bot.command()
async def momo(ctx):
    message = "MoMoshow le meilleur et le J c'est sa soumise."
    await ctx.send(message)

@client.event
async def on_message(message):
    if message.content.lower() == "quoi":
        await message.channel.send("Feur")
    if message.content.lower()== "méchant":
        await message.delete()

@client.event
async def on_member_join(member):
    general_channel: discord.TextChannel = client.get_channel(1135847736537776197)
    general_channel.send(content=f"Bienvenue sur le serveur Vigneron | DynastyRp{member.display_name} !")

@bot.command()
async def monstre(ctx):
    message = "TRIPLE MONSTTTTTRRRRRREEEEEEE BROZZZZZEEERRRRR"
    await ctx.send(message)


bot.run("MTE0MjQ5Mzc0NzM2MDMxNzU2MQ.GP0JU_.bm-09slToRYSYitOrpz6hmVqYz8D-q9XgJmDZs")