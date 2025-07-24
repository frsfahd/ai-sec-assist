from fileinput import filename
import logging
import os
import dotenv

from ai import RunAgent

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler

dotenv.load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

mediaList: dict[str, dict[int, dict[str, str]]] = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = await RunAgent((update.message.from_user.username, update.message.text))

    await context.bot.send_message(chat_id=update.effective_chat.id, text=str(response.content))

async def media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document


    mediaList[update.message.from_user.username] = {
        update.message.id: {
            "file_id": doc.file_id,
            "filename": doc.file_name
        }
    }

    response = f"""
    ID: {mediaList[update.message.from_user.username][update.message.id].get("file_id")}
    Filename: {mediaList[update.message.from_user.username][update.message.id].get("filename")}
    Type: {doc.mime_type}
    """

    await context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.id, text=response)
    

async def messageWithMedia(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Check if reply is to a document message
    replied_message = update.message.reply_to_message
    if not replied_message or not replied_message.document:
        return  # Skip if not replying to a document

    # get the file url and metadata to download from telegram server
    thread = mediaList[update.message.from_user.username][update.message.reply_to_message.id]
    file_id = thread["file_id"]
    filename = thread["filename"]
    file = await context.bot.get_file(file_id=file_id)

    # download file
    filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "tmp", filename))
    await file.download_to_drive(filepath)

    prompt = f"""filepath: {filepath}  
{update.message.text}
"""

    response = await RunAgent((update.message.from_user.username, prompt))

    await context.bot.send_message(chat_id=update.effective_chat.id, text=str(response.content))

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv("BOT_API_TOKEN")).build()
    
    start_handler = CommandHandler('start', start)
    chatHandler = MessageHandler(filters.TEXT & (~filters.COMMAND), message)
    mediaHandler = MessageHandler(filters.Document.ALL & (~filters.COMMAND), media)
    messageWithMediaHandler = MessageHandler(filters.TEXT & filters.REPLY &(~filters.COMMAND), messageWithMedia)

    application.add_handler(start_handler)
    application.add_handler(messageWithMediaHandler)  
    application.add_handler(chatHandler)
    application.add_handler(mediaHandler)
    
    application.run_polling()