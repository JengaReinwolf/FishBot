import json
import re
import unicodedata

import discord

BWEE_RE = re.compile(r"b+[b*|~\n ]*w+[w*|~\n ]*e+[e*|~\n ]*e+", re.IGNORECASE | re.MULTILINE)
SQUEE_RE = re.compile(r"s+[s*|~\n ]*[q+[q*|~\n ]+[uw]+[uw*|~\n ]*e+[e*|~\n ]*e+", re.IGNORECASE | re.MULTILINE)

client = discord.Client()
with open("config.json", "rb") as f:
    config = json.loads(f.read())


@client.event
async def on_message(message):
    # Give fish for bwees
    if re.search(BWEE_RE, clean_message(message.content)) or re.search(SQUEE_RE, clean_message(message.content)):
        try:
            await message.add_reaction("🐟")
        except discord.errors.NotFound:
            pass  # Caused by message being deleted before we can properly react. Ignorable.


def clean_message(msg):
    return text_script_normalize(strip_accents(msg))


def strip_accents(msg):
    return "".join(c for c in unicodedata.normalize("NFD", msg) if unicodedata.category(c) != "Mn")


# Based upon https://stackoverflow.com/a/58612677
def text_script_normalize(msg):
    TRANSLATOR = str.maketrans("ˢₛǫᵠᵩᴮ₈ᴱₑᵂ𝓌ʙᵇᵦ♭ᴇᵉₑʷᴡ𝓌", "ssQqqBBEEWWbbbbeeewww")
    return msg.translate(TRANSLATOR)


client.run(config["token"])
