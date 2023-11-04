from flask import Flask, render_template, request, session
import discord
from discord.ext import commands

app = Flask(__name__)
app.secret_key = 'my_secret_key'  # Clave secreta para las sesiones

class Discord:
    @staticmethod
    @app.route('/')
    def home():
        return render_template('html_ds.html')

    @staticmethod
    @app.route('/saludar', methods=['POST'])
    def saludar():
        nombre = request.form['nombre']
        session['nombre'] = nombre  # Almacena el nombre en la sesión
        mensaje = "¡Rol asignado a {}!".format(nombre)
        return mensaje

    @classmethod
    @app.route('/automatizacion', methods=['POST'])
    def automatizacion(cls):
        nombre = session.get('nombre')  # Obtiene el nombre de la sesión
        if not nombre:
            return "No se ha ingresado un nombre previamente."

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
            if nombre:
                user = discord.utils.get(guild.members, name=nombre)

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

        mensaje = "¡Rol asignado a {}!".format(nombre)
        return mensaje

if __name__ == '__main__':
    app.run()
