# Telegram Word Protector Bot

A Telegram group moderation bot that automatically filters inappropriate or unsafe messages using the [Mango API](https://api.mangoi.in). Users are warned when violations are detected, and after 3 warnings, the bot will ban them. Built using `python-telegram-bot v20+`.

---

## Features

- Filters NSFW or unsafe messages  
- Works only in group chats  
- Skips group admins and owner  
- Gives 3 warnings per user  
- Bans user after 3rd warning  
- Uses MangoI API for accurate filtering  

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Mishel-07/Word-Protector.git
cd Word-Protector
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Your Bot Token

Edit **line 7 of `bot.py`** and replace `TOKEN` with your bot token from [@BotFather](https://t.me/BotFather):

## License

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute this software.
