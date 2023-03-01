import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import pandas as pd
import giphy_client
from giphy_client.rest import ApiException

# Pandas csv data
pd.set_option('display.max_colwidth', None)
df_beef = pd.read_csv('beef_recipes.csv')
df_chic = pd.read_csv('chicken_recipes.csv')
df_ins = pd.read_csv('insults.csv')

# discord client variable
client = commands.Bot(command_prefix=".", intents=discord.Intents.all())


# .env function for bot secrets.


def configure():
    load_dotenv()


configure()


@client.event
async def on_ready():
    print('I have logged in as {0.user}'.format(client))
    await client.tree.sync()


@client.tree.command(name="insult", description="Lets Gordon insult somebody")
async def insult(interaction: discord.Interaction, member: discord.Member = None):
    rint_i = random.randint(0, len(df_ins) - 1)
    if member == None:
        member = interaction.user
    await interaction.response.send_message(content=f"{member.mention} - {df_ins.iloc[rint_i]['insults']}")


@client.tree.command(name="beef_recipe", description="Gives a random Gordon Ramsey beef recipe.")
async def recipe(interaction: discord.Interaction):
    rint_b = random.randint(0, len(df_beef) - 1)
    embed = discord.Embed(title="Gordon Ramsay beef recipes",
                          description="recipe from chef Gordon Ramsay's official "
                                      "website. https://www.gordonramsay.com/", colour=discord.Colour.green())
    embed.set_image(url=df_beef.iloc[rint_b]['recipe_picture_url'])
    embed.add_field(name="Recipe Title", value=df_beef.iloc[rint_b]['recipe_name'])
    embed.add_field(name="Ingredients", value=df_beef.iloc[rint_b]['ingredients'])
    embed.add_field(name="VIEW FULL RECIPE HERE", value=df_beef.iloc[rint_b]['full_recipe_link'])
    await interaction.response.send_message(embed=embed)


@client.tree.command(name="chicken_recipe", description="Gives a random Gordon Ramsey chicken recipe.")
async def recipe(interaction: discord.Interaction):
    rint_c = random.randint(0, len(df_chic) - 1)
    embed = discord.Embed(title="Gordon Ramsay chicken recipes",
                          description="recipe from chef Gordon Ramsay's official "
                                      "website. https://www.gordonramsay.com/", colour=discord.Colour.green())
    embed.set_image(url=df_chic.iloc[rint_c]['recipe_picture_url'])
    embed.add_field(name="Recipe Title", value=df_chic.iloc[rint_c]['recipe_name'])
    embed.add_field(name="Ingredients", value=df_chic.iloc[rint_c]['ingredients'])
    embed.add_field(name="VIEW FULL RECIPE HERE", value=df_chic.iloc[rint_c]['full_recipe_link'])
    await interaction.response.send_message(embed=embed)


@client.tree.command(name="gif", description="Daddy Gordon sends you gifs")
async def gif(interaction: discord.Interaction, member: discord.Member = None):
    if member == None:
        member = interaction.user
    api_key = os.getenv('GIPHY_API')
    api_instance = giphy_client.DefaultApi()

    try:
        api_response = api_instance.gifs_search_get(api_key, "Gordon Ramsay insults funny", limit=30, rating="R")
        lst = list(api_response.data)
        giff = random.choice(lst)
        embed = discord.Embed(title="Gordon.gif", description="Daddy Gordon says: ")
        embed.set_image(url=f"https://media.giphy.com/media/{giff.id}/giphy.gif")
        await interaction.response.send_message(content=member.mention, embed=embed)

    except ApiException as e:
        print("Exception for the api.")


@client.tree.command(name="stop", description="Shuts down the bot")
async def stop(interaction: discord.Interaction):
    await interaction.response.send_message(content="Quitting bot")
    await client.close()


client.run(os.getenv('TOKEN'))
