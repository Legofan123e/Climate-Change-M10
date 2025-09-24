import discord
from discord.ext import commands
import requests
import pyttsx3  # Biblioteca para síntesis de voz
from googletrans import Translator
# Inicializar el sintetizador de voz
engine = pyttsx3.init()  # Crear un objeto para la síntesis de voz
# Inicializar el objeto del bot
intents = discord.Intents.default()  # Configurar permisos para el bot
intents.message_content = True  # Habilitar la capacidad de leer el contenido de los mensajes
class BasicInfo(commands.Cog):
    '''The usual info on climate change.'''
    # WARNING!!!: The following commands have a skill issue and their string messages are too long because Python won't let me press enter to start a new paragraph.
    @commands.command('causes')
    async def causes(self, ctx):
        '''Writes down the causes of climate change'''
        await ctx.send("Causes of the climate change include:\n **-Energy generation**: Burning through fossils to get energy generates C02, and that increases the temperature. There are other alternatives, like solar energy or hydroelectricity. \n **-Manufactured products:**Productions of goods also generates enormous amounts of C02. \n **-Forest clearing:** Reduces nature's capacity to recycle C02 and generates even more of it \n **Transportation:** This burns fossils for fuel, and as previously stated, that also makes more C02. \n **-Food production:** This requires energy to be done, and energy is mainly powered by fossils. \n **-Building's electrical supply:** They consume too much energy, which means more use of carbon, oil and natural gas as energy sources, producing a lot of C02. \n **-Excessive consumption:** The amount of resources that you use as well as the waste that you throw out also have significant impact on the environment.")
    
    @commands.command('consequences')
    async def consequences(self, ctx):
        '''Writes down the consequences of climate change'''
        await ctx.send("Consequences of the climate change include:\n __-Higher temperatures__ \n __-Increase of intense storms__ \n __-Increase of drought__ \n __-Increase of sea level and temperature__ \n __-Species extinction__ \n __-Shortage of food__ \n __Higher health risks__ \n __-Poverty and displacement__")
    
    @commands.command('mitigation')
    async def mitigation(self, ctx):
        '''Writes down mitigation measures of climate change'''
        await ctx.send("To tone down C02 emissions, we can help by being efficient with our energy usage, management of waste, correct consumption, sustainable transport and sharing vehicles. In a wider level, we have to start reforestation, take care of forests, do sustainable agriculture, use renewable energy sources, make climate policies and have a circular economy.")

bot = commands.Bot(command_prefix='!', intents=intents)  # Crear un bot con el prefijo de comando especificado
translator = Translator()
# Función para obtener el clima a través de la API wttr.in
def get_weather(city: str) -> str:
    '''
    Obtiene datos del clima para la ciudad especificada.
    
    Parámetros:
        city (str): Nombre de la ciudad

    Retorna:
        str: Información del clima o mensaje de error
    '''
    base_url = f'https://wttr.in/{city}?format=%C+%t'  # URL de solicitud con formato (descripción y temperatura)
    response = requests.get(base_url)  # Realizar una solicitud GET a la API
    if response.status_code == 200:  # Si la solicitud es exitosa (código 200)
        return response.text.strip()  # Retornar la respuesta en texto sin espacios extra
    else:
        return 'No se pudo obtener la información del clima. Por favor, inténtalo más tarde.'  # Retornar el mensaje de error

# Función para la síntesis de voz
def speak(text: str):
    '''
    Convierte el texto en voz usando pyttsx3.

    Parámetros:
        text (str): Texto a vocalizar
    '''
    engine.getProperty('rate')  # getting details of current speaking rate
    engine.setProperty('rate', 150)  # setting up new voice rate
    engine.say(text)  # Pasar el texto para la síntesis
    engine.runAndWait()  # Ejecutar la síntesis de voz y esperar a que termine

def get_fact() -> str:
    """
    Obtiene un dato curioso al azar.
    """
    base_url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m"  # URL de solicitud con formato (descripción y temperatura)
    response = requests.get(base_url)  # Realizar una solicitud GET a la API
    if response.status_code == 200:
        data = response.json()
        fact_en = data.get("latitude", "No se pudo obtener el dato.")

        try:
            # Traducir al español
            fact_es = translator.translate(fact_en, src="en", dest="es").text
            return fact_es
        except Exception as e:
            return f"No se pudo traducir el dato. Original: {fact_en}"

    else:
        return "No se pudo obtener la información. Por favor, inténtalo más tarde."

class APIStuff(commands.Cog):
    '''This uses external APIs and are more of a experimental feature.'''    
    @commands.command('fact')
    async def fact(self, ctx):
        '''Supposed to be a climate change facts command, shows latitude levels.'''
        result = get_fact()
        await ctx.send(f'Latitude: {result}')
        speak(result)
    # Comando para obtener el clima
    @commands.command()
    async def weather(self, ctx, *, city: str):
        '''
        Comando para obtener información del clima y vocalizarla.

        Parámetros:
            ctx: Contexto del comando (información sobre la ejecución del comando)
            city (str): Nombre de la ciudad
        '''
        weather_info = get_weather(city)  # Obtener los datos del clima para la ciudad especificada
        await ctx.send(f'Clima en {city}: {weather_info}')  # Enviar la información del clima al canal de Discord
        speak(weather_info)  # Vocalizar la información obtenida

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.add_cog(BasicInfo())
    await bot.add_cog(APIStuff())
@bot.command('info')
async def info(ctx):
    '''Shows a bit of info regarding the bot (not the same as help command)'''
    await ctx.send('M10 Final project, Discord bot that promotes actions against climate change.')
  
bot.run('token')
