from flask import Flask, render_template, request
import discord
from discord.ext import commands

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/start_bot', methods=['POST'])
def start_bot():
   # Coloca aquí tu código de Discord
   import discord
   from discord.ext import commands

   intents = discord.Intents.default()
   intents.typing = False
   intents.presences = False

   bot = commands.Bot(command_prefix='!', intents=intents)

   invite_url = None  # Inicializa la variable invite_url

   @bot.event
   async def on_ready():
       print(f'Bot está listo como {bot.user.name}')
       nonlocal invite_url  # Permite modificar la variable invite_url del ámbito externo
       for guild in bot.guilds:
           invite = await guild.text_channels[0].create_invite(max_uses=1, unique=True)
           invite_url = invite.url
           print(f'Aquí tienes un enlace de invitación único: {invite_url}')
           break  # Detiene el bucle después de crear una invitación en el primer canal de texto
       await bot.close()

   bot.run('MTE2NTcxNTk3NDAyMDkyNzY0OA.GYGknZ.5t9Yes0Pkwu7a6CQFVC5sBpt9t4k9hRuw_Khyo')

   return render_template('index.html', invite_url=invite_url)

if __name__ == '__main__':
   app.run()























"""
#OBTENGO LOS NOMBRES DE DISCORD DE CADA MIEMBRO DE CIRCLE
url = "https://app.circle.so/api/v1/community_members?sort=latest&per_page=100&page=1"

payload = {}
headers = {
    'Authorization': 'Token ZRdd6TUwzw4s41fT1YWoaQvY'
}

response = requests.request("GET", url, headers=headers, data=payload)
data = response.json()

filtered_data = []
lista = []

for item in data:
    filtered_item = {
        'id': item['id'],
        'name': item.get('name', ''),  # Usamos get para manejar campos opcionales
        'bio': item.get('bio', ''),
    }
    filtered_data.append(filtered_item)

for i in filtered_data:
    lista.append(i["id"])
#HASTA ACA


#AUTOMATIZACION
# Introduce tu token de bot aquí
TOKEN = 'MTE2NTcxNTk3NDAyMDkyNzY0OA.GYGknZ.5t9Yes0Pkwu7a6CQFVC5sBpt9t4k9hRuw_Khyo'

# Define las intenciones requeridas
intents = discord.Intents.default()
intents.members = True  # Necesario para acceder a la lista de miembros
intents.message_content = True  # Habilita las intenciones de contenido de mensajes

# Crea una instancia del bot con las intenciones
bot = commands.Bot(command_prefix='!', intents=intents)

diccionario_usuarios_id = {}

@bot.event
async def on_ready():
    print(f'Bot está conectado como {bot.user.name}')

    # Obtiene el servidor actual
    guild = bot.guilds[0]  # Utiliza el primer servidor en la lista

    # Obtiene la ID de un usuario por su nombre de usuario
    for nombre in lista:
        print(nombre)
        user = discord.utils.get(guild.members, name=nombre)
        print("user", user)

        if user is not None:
            diccionario_usuarios_id[nombre] = user.id
            print(f'La ID de {nombre} es {user.id}')
        else:
            print(f'No se encontró al usuario {nombre}')

    # Obtiene el rol que deseas asignar (reemplaza 'ID_DEL_ROL' con la ID del rol)
    rol_a_asignar = discord.utils.get(guild.roles, id=1165397972822020268)

    if rol_a_asignar is None:
        print("El rol especificado no existe en el servidor.")
        await bot.close()

    # Itera a través de las IDs de usuario y asigna el rol a cada uno
    for nombre, usuario_id in diccionario_usuarios_id.items():
        usuario = guild.get_member(usuario_id)
        if usuario is not None:
            await usuario.add_roles(rol_a_asignar)
            print(f"Se ha asignado el rol '{rol_a_asignar.name}' a {usuario.name}.")

    # Cierra la conexión del bot después de asignar los roles
    await bot.close()


bot.run(TOKEN)



D:\PycharmProjects\venv\Scripts\python.exe D:\PycharmProjects\pythonProject3\discord_rama.py 
[2023-11-04 13:03:11] [INFO    ] discord.client: logging in using static token
[2023-11-04 13:03:12] [INFO    ] discord.gateway: Shard ID None has connected to Gateway (Session ID: b407144b0c3e90ea6f68bc3ee262671b).
Bot está conectado como CircleDiscBot
16132279
No se encontró al usuario 16132279
16128275
No se encontró al usuario 16128275
16048983
No se encontró al usuario 16048983
"""