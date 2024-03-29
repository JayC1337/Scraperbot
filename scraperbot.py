import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import discord
import time

# Discord-Bot-Token
DISCORD_TOKEN = ""
CHANNEL_ID =   # ID des Discord-Kanals

# URL der Website
url = "https://www.partyamt.de/"

# Aktuelles Datum ermitteln
today = date.today()

# HTTP-Anfrage senden und HTML-Seite herunterladen
response = requests.get(url)
html_content = response.content

# HTML-Seite parsen
soup = BeautifulSoup(html_content, "lxml")

# Alle Termine extrahieren
events = soup.find_all("div", class_="event")

# Discord-Bot initialisieren
intents = discord.Intents.default()
bot = discord.Client(intents=intents)

async def send_events_to_discord():
    channel = bot.get_channel(CHANNEL_ID)
    for event in events:
        subject_div = event.find("div", class_="subject")
        title_link = subject_div.find("a", class_="event_title")
        title = title_link.find("div", class_="title_short").text.strip()
        link = "https://www.partyamt.de" + title_link["href"]
        location = subject_div.find("div", class_="location").a.text.strip()
        time = subject_div.find("div", class_="time").text.strip()

        # Datum aus dem Link extrahieren
        link_parts = link.split("/")
        event_date_str = link_parts[-1]
        event_date = datetime.strptime(event_date_str, "%Y-%m-%d").date()

        # Nur Events für den heutigen Tag ausgeben
        if event_date == today:
            event_date_formatted = event_date.strftime("%d.%m.%Y")
            event_info = f"Titel: {title}\nOrt: {location}\nDatum: {event_date_formatted}\nZeit: {time}\nLink: {link}"
            await channel.send(event_info)
    # Bot beenden
    await bot.close()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await send_events_to_discord()

# Bot starten
bot.run(DISCORD_TOKEN)
