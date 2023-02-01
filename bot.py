import discord

import requests

import asyncio

from json import loads

twitch_Client_ID = '928vov9eoo0ubrsxrkyb32lmc9tra4'

twitch_Client_secret = 'vz399viz84he91r3puxdppajk4lvmp'

discord_Token = 'MTA2OTQ4NzcxOTE3NDEyNzY0Nw.Gy0soD.8Jz9M237NxEoqOVdXz-BM_jmq53hRABnY8BilQ'



discord_channelID = 322768570175979520

discord_bot_state = '디스코드 봇이 하고 있는 것(ex 방송 알리미)'

twitchID = 'lckclglobal2023'
#알림 받고싶은 스트리머의 ID

onairMent = twitchID + '님이 방송중이네요. 방송을 보러 갈까요??.'

offairMent = "방송중이 아니네요. 조금만 더 기다려 주세요!"

onairState = False

client = discord.Client(intents=discord.Intents.default())

@client.event

async def on_ready():

    print("ready")

    # 디스코드 봇 상태 설정

    game = discord.Game(discord_bot_state)

    await client.change_presence(status=discord.Status.online, activity=game)



    # 채팅 채널 설정

    channel = client.get_channel(discord_channelID)
    # 현재 채널이 없다고 나온다.



    # 트위치 api 2차인증

    oauth_key = requests.post("https://id.twitch.tv/oauth2/token?client_id=" + twitch_Client_ID + "&client_secret=" + twitch_Client_secret + "&grant_type=client_credentials")

    access_token = loads(oauth_key.text)["access_token"]

    token_type = 'Bearer '

    authorization = token_type + access_token

    print(authorization)

    check = False     #여기 오류를 수정합니다



    while True:

        print("ready on Notification")

        # 트위치 api에게 방송 정보 요청

        headers = {'client-id': twitch_Client_ID, 'Authorization': authorization}

        response_channel = requests.get('https://api.twitch.tv/helix/streams?user_login=' + twitchID, headers=headers)

        print(response_channel.text)
        # 라이브 상태 체크

        try:

            # 방송 정보에서 'data'에서 'type' 값이 live 이고 체크상태가 false 이면 방송 알림(오프라인이면 방송정보가 공백으로 옴)

            if loads(response_channel.text)['data'][0]['type'] == 'live' and check is False:

                print("Online")

                await channel.send(onairMent + '\n https://www.twitch.tv/' + twitchID)

                check = True

        except:

            print("Offline")

            check = False



        await asyncio.sleep(30)



client.run(discord_Token)


