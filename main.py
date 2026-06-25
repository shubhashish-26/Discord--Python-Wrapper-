import mylib
import datetime
import random

client = mylib.Bot(command_prefix='-')

@client.event
def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
def on_message(message):
    if message.content == 'hi':
        client.send(message.channel_id, 'hey there')

@client.slash_command(
    name='info',
    description='Gives user information.'
)
def hello(interaction):  
    colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4, 0x006400, 0x808080, 0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]

    user_timestamp = interaction.user.created_at
    user_created = user_timestamp.strftime("%m/%d/%Y, %H:%M:%S")

    em = mylib.Embed(title='User Info', color=random.choice(colors))
    em.add_field(name='User', value=f'{interaction.user}', inline=False)
    em.add_field(name='Display Name', value=f'{interaction.user.display_name}', inline=False)
    em.add_field(name='User ID', value=f'{interaction.user.id}', inline=False)
    em.add_field(name='Created at', value=f'{user_created}', inline=False)
    em.set_thumbnail(url=interaction.user.avatar_url)
    em.set_footer(text=f'{client.user.name}', icon_url=client.user.avatar_url)

    interaction.respond(embed=em)


@client.slash_command(
    description='Show\'s you your/friends avatar.'
)
def avatar(interaction):
    em = mylib.Embed()
    em.set_author(name=f'Avatar for {interaction.user}')
    em.add_field(name='Link', value=f'[Link]({interaction.user.avatar_url})', inline=False)
    em.set_image(url=interaction.user.avatar_url)

    interaction.respond(embed=em)

@client.slash_command(
    description = 'Get or edit permissions for a user or a role',
    options = [
        mylib.SubcommandGroup(name='user', description='Get or edit permissions for a user', options=[
            mylib.Subcommand(name='get', description='get permissions for a user', options=[
                mylib.CommandOptions(name='user', description='the user whom you want information', type=mylib.OptionsType.USER, required=True),
                mylib.CommandOptions(name='channel', description='channel', type=mylib.OptionsType.CHANNEL),
            ]),
            mylib.Subcommand(name='edit', description='edit permissions for a user', options=[
                mylib.CommandOptions(name='user', description='the user to edit', type=mylib.OptionsType.USER, required=True),
                mylib.CommandOptions(name='channel', description='role description', type=mylib.OptionsType.CHANNEL),
            ])
        ]),
        mylib.SubcommandGroup(name='role', description='Get or edit permissions for a role', options=[
            mylib.Subcommand(name='get', description='get permissions for a role', options=[
                mylib.CommandOptions(name='role', description='the role whom you want information', type=mylib.OptionsType.ROLE, required=True),
                mylib.CommandOptions(name='channel', description='channel', type=mylib.OptionsType.CHANNEL),
            ]),
            mylib.Subcommand(name='edit', description='edit permissions for a role', options=[
                mylib.CommandOptions(name='role', description='the role to edit', type=mylib.OptionsType.ROLE, required=True),
                mylib.CommandOptions(name='channel', description='role description', type=mylib.OptionsType.CHANNEL),
            ])
        ])
    ]
)
def permissions(interaction):
    interaction.respond('hii')


@client.slash_command(
    description = 'checks/edit user permissions',
    options = [
        mylib.Subcommand(name='check', description='checks user permissions', options=[
            mylib.CommandOptions(name='user', description='the user to check for', type=mylib.OptionsType.USER, required=True)
        ]),
        mylib.Subcommand(name='edit', description='edits user permissions', options=[
            mylib.CommandOptions(name='user', description='the user to edit for', type=mylib.OptionsType.USER, required=True)
        ])
    ]
)
def user(interaction):
    interaction.respond('hii')


@client.slash_command(
    description = 'gives you a desired photo.',
    options = [
        mylib.CommandOptions(name='choice', description='user choice', required=True, type=mylib.OptionsType.STRING, choices=[
            mylib.Choices(name='Dog', value='Gives you a dog image.'),
            mylib.Choices(name='Cat', value='Gives you a cat image.'),
            mylib.Choices(name='Parrot', value='Gives you a parrot image.')
        ])
    ]
)
def get(interaction):
    interaction.respond('ayo!!')

client.run('token')