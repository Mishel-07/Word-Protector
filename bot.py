import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters, CommandHandler

warn = {}

TOKEN = ""

API_KEY = "" # hey dm @beesons in telegram for api key

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Add Me To Group", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [InlineKeyboardButton("Source Code", url="https://github.com/Mishel-07/Word-Protector")]
    ])
    await update.message.reply_text(
        "I'm a word protection bot.\n"
        "I automatically delete unsafe messages and warn users.\n"
        "Add me to a group and make me admin to get started.",
        reply_markup=keyboard
    )

async def word_checker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = update.message
    if m.chat.type == "private":
        return

    member = await context.bot.get_chat_member(m.chat.id, m.from_user.id)
    if member.status in ("administrator", "creator"):
        return

    res = requests.get(f"https://api.mangoi.in/v1/words/{m.text.replace(' ', '+')}/accurate=80/api_key={API_KEY}").json()

    if res.get("nosafe"):
        await m.delete()    
        if not warn.get(m.from_user.id):
            warn[m.from_user.id] = 0
        warn[m.from_user.id] += 1
            
        if warn[m.from_user.id] >= 3:
            del warn[m.from_user.id]
            await m.chat.ban_member(m.from_user.id)
            await context.bot.send_message(
                chat_id=m.chat.id,
                text=f"{m.from_user.mention_html()} has been banned for reaching 3 warnings.",
                parse_mode="HTML"
            )
            return
        await context.bot.send_message(
            chat_id=m.chat.id,
            text=(
                f"Dear {m.from_user.mention_html()},\n\n"
                f"You have received a warning ({warn[m.from_user.id]}/3) for sharing inappropriate content.\n\n"
                f"<b>Detected content:</b> <code>{res['content']}</code>\n\n"
                f"Please refrain from sending such messages. Reaching 3 warnings will result in a ban."
            ),
            parse_mode="HTML"
        )

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, word_checker))
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
