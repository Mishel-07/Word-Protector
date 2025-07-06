import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

warn = {}

TOKEN = ""

async def word_checker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = update.message
    if m.chat.type == "private":
        return

    member = await context.bot.get_chat_member(m.chat.id, m.from_user.id)
    if member.status in ("administrator", "creator"):
        return

    res = requests.get(f"https://api.mangoi.in/v1/words/{m.text.replace(' ', '+')}/accurate=80").json()

    if res.get("nosafe"):
        await m.delete()      
        warn[m.from_user.id]["warn"] += 1

        await m.reply_text(
            f"<b>Hey {m.from_user.mention_html()}</b>, you have been warned {warn[m.from_user.id]['warn']}/3 times.\n"
            f"Please avoid sending inappropriate content like:\n<code>{res.get('content')}</code>\n"
            f"If you reach 3 warnings, you will be banned.",
            parse_mode="HTML"
        )

        if warn[m.from_user.id]["warn"] >= 3:
            del warn[m.from_user.id]
            await m.chat.ban_member(m.from_user.id)
            await m.reply_text(
                f"{m.from_user.mention_html()} has been banned for reaching 3 warnings.",
                parse_mode="HTML"
            )

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, word_checker))
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
