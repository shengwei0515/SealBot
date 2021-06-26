# Seal Bot
This is a chat bot for twitch

# Requirement
* python >= 3.6
* pip3

# Setup
1. install python plugins
```
$ pip3 install -r requirements.txt
```

2. 在此層目錄新增一個 .env 檔案並包含以下資訊，特別注意這個檔案內都是敏感資料，不要外流或 commit
```
TMI_TOKEN=oauth:<auth_token>
CLIENT_ID=<app_client_id>
BOT_NICK=<the_name_of_this_bot_in_chat_room>
BOT_PREFIX=!
CHANNEL=<which_channel_to_connect>
```

* TMI_TOKEN: 驗證需要用到的 OAuth Token，可以在[這個網頁](https://twitchapps.com/tmi/)申請
* CLIENT_ID: 需要去 twitch 的 developer console 註冊一個應用程式，並且拿到 clentid，請到[這個網頁](https://dev.twitch.tv/console/apps)申請。
    * 點進去後點選授權
    * 看到主控台下面有三個選項，選擇應用程式
    * 點選註冊您的應用程式
        * 名稱：隨便給
        * OAuth 重導向網址：這個這邊好像用不到所以沒差
        * 分類： Chat Bot
        * 下面有一個用戶端ID就是這裡要用的 CLIENT_ID
        * 點選新密碼產生一個密碼，不過這邊好像沒用到
* BOT_NICK: 你的帳號在聊天室裡的英文名稱，並且用全小寫表示
* BOT_PREFIX: 用來設定指令的 predix，目前比較常見就是驚嘆號
* CHANNEL：啟動 bot 之後會連線到哪個頻道，假如你的平到網址是 https://www.twitch.tv/sealseal，這邊就填sealseal

3. 透過以下指令啟動 bot
```
$ python3 main.py
```


# reference
* [Let's make a Twitch bot with Python!](https://dev.to/ninjabunny9000/let-s-make-a-twitch-bot-with-python-2nd8)
* [TwitchIO - github](https://github.com/TwitchIO/TwitchIO)
* [TwitchIO - doc](https://twitchio.readthedocs.io/en/latest/)
* [SQLAlchemy](https://www.compose.com/articles/using-postgresql-through-sqlalchemy/)


# db migrate
* new alembic 
```
pythom3 -m alembic init myAlembic
```

* new migrate
```
python3 -m alembic revision -m "create seal_coin table"       
```

* run
```
python3 -m alembic  upgrade head
```