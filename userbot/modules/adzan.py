import json

import requests

from userbot import CMD_HELP
from userbot.events import register

PLACE = ""


@register(pattern=r"^\.adzan(?: |$)(.*)")
async def get_adzan(adzan):
    if not adzan.pattern_match.group(1):
        LOCATION = PLACE
        if not LOCATION:
            await adzan.edit("Harap Tentukan Kota atau Negara Anda")
            return
    else:
        LOCATION = adzan.pattern_match.group(1)

    # url = f'http://muslimsalat.com/{LOCATION}.json?key=bd099c5825cbedb9aa934e255a81a5fc'
    url = f"https://api.pray.zone/v2/times/today.json?city={LOCATION}"
    request = requests.get(url)
    if request.status_code == 500:
        return await adzan.edit(f"**Kota Not Found** `{LOCATION}`")

    parsed = json.loads(request.text)

    city = parsed["results"]["location"]["city"]
    country = parsed["results"]["location"]["country"]
    timezone = parsed["results"]["location"]["timezone"]
    date = parsed["results"]["datetime"][0]["date"]["gregorian"]

    imsak = parsed["results"]["datetime"][0]["times"]["Imsak"]
    subuh = parsed["results"]["datetime"][0]["times"]["Fajr"]
    zuhur = parsed["results"]["datetime"][0]["times"]["Dhuhr"]
    ashar = parsed["results"]["datetime"][0]["times"]["Asr"]
    maghrib = parsed["results"]["datetime"][0]["times"]["Maghrib"]
    isya = parsed["results"]["datetime"][0]["times"]["Isha"]

    result = (
        f"**JADWAL SHOLAT**:\n"
        f"📅 {date} | {timezone}\n"
        f"🌏 {city} | {country}\n\n"
        f"**Imsak :** {imsak}\n"
        f"**Shubuh :** {subuh}\n"
        f"**Dzuhur :** {zuhur}\n"
        f"**Ashar :** {ashar}\n"
        f"**Maghrib :** {maghrib}\n"
        f"**Isya :** {isya}\n"
    )

    await adzan.edit(result)


CMD_HELP.update({"Adzan": "\n\n➢ .adzan kota"
                 "\nPenjelasan: Memberikan Informasi Waktu Sholat."})
