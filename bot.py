import os
from telegram import update
from telegram.ext.filters import MessageFilter
PORT = int(os.environ.get('PORT', 8443))
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, messagehandler

chat_id_gp_principal="-1001150565069"
bot_token="" #Token para acessar o bot
chat_id_alvo=chat_id_gp_principal
estaDesligado=0
msgsApagadas={}

def start(update, context):
    global chat_id_alvo
    global chat_id_gp_principal
    global estaDesligado

    if (update.message.chat.type == 'private') or (update.message.chat.id == -1001150565069):
        update.message.reply_text('Bot em execução')
    elif update.message.from_user.id==411689167:
        if chat_id_alvo == chat_id_gp_principal:
            chat_id_alvo=update.message.chat.id
            update.message.reply_text('enviando msgs aqui agora')
            estaDesligado=1
        else:
            chat_id_alvo=chat_id_gp_principal
            update.message.reply_text('enviando msgs no grupo principal agora')
            estaDesligado=0
    else:
        update.message.reply_text("Apenas Olavo pode mudar o chat👍")

def delete(update, context):
    global msgsApagadas
    if (not (update.message.from_user.id in msgsApagadas)):
        update.message.reply_text("Você não tem nenhuma mensage recente")
        return
    if (len(msgsApagadas[update.message.from_user.id])<=0):
        update.message.reply_text("Você não tem nenhuma mensage recente")
        return
    
    msgApagada=(msgsApagadas[update.message.from_user.id]).pop()
    context.bot.deleteMessage(msgApagada[0],msgApagada[1])

def echo(update, context):
    """Echo the user message."""
    return context.bot.sendMessage(chat_id_alvo, update.message.text)

def foto(update, context):
    return context.bot.sendPhoto(chat_id_alvo, update.message.photo[0].file_id,caption=update.message.caption)

def video(update, context):
    return context.bot.sendVideo(chat_id_alvo,update.message.video,caption=update.message.caption)

def msg_video(update, context):
    return context.bot.send_video_note(chat_id_alvo,update.message.video_note)

def arq_audio(update, context):
    return context.bot.sendAudio(chat_id_alvo,update.message.audio)

def audio(update, context):
    return context.bot.sendVoice(chat_id_alvo,update.message.voice)

def dado(update, context):
    return context.bot.sendDice(chat_id_alvo,update.message.dice.file_id)

def documento(update, context):
    return context.bot.sendDocument(chat_id_alvo,update.message.document)

def localizacao(update, context):
    return context.bot.sendLocation(chat_id_alvo,update.message.location.latitude,update.message.location.longitude)

def votacao(update, context):
    a={'question': update.message.poll.question, 'options':[]}
    for opcao in update.message.poll.options:
        a['options'].append(opcao.text)
    if hasattr(update.message.poll,"is_anonymous"):
        a['is_anonymous']=update.message.poll.is_anonymous
    if hasattr(update.message.poll,"type"):
        a['type']=update.message.poll.type
    if hasattr(update.message.poll,"allows_multiple_answers"):
        a['allows_multiple_answers']=update.message.poll.allows_multiple_answers
    if hasattr(update.message.poll,"correct_option_id"):
        a['correct_option_id']=update.message.poll.correct_option_id
    if hasattr(update.message.poll,"explanation"):
        a['explanation']=update.message.poll.explanation
    if hasattr(update.message.poll,"explanation_entities"):
        a['explanation_entities']=update.message.poll.explanation_entities
    if hasattr(update.message.poll,"open_period"):
        a['open_period']=update.message.poll.open_period
    if hasattr(update.message.poll,"close_date"):
        a['close_date']=update.message.poll.close_date
    if hasattr(update.message.poll,"is_closed"):
        a['is_closed']=update.message.poll.is_closed
    return context.bot.sendPoll(chat_id_alvo, **a)

def contato(update, context):
    a={ 'phone_number':update.message.contact.phone_number,'first_name':update.message.contact.first_name}
    if hasattr(update.message.contact,"last_name"):
        a['last_name']=update.message.contact.last_name
    if hasattr(update.message.contact,"vcard"):
        a['vcard']=update.message.contact.vcard
    return context.bot.sendContact(chat_id_alvo,**a)

def figurinha(update, context):
    return context.bot.sendSticker(chat_id_alvo,update.message.sticker.file_id)

def jogo(update, context):
    return context.bot.sendGame(chat_id_alvo,update.message.game.game_short_name)

def encaminhar(update,context):
    return context.bot.forwardMessage(chat_id_alvo,update.message.chat.id,update.message.message_id)

def enviarMsg(update, context):
    global estaDesligado
    global msgEnviada

    print(update)

    if update.message.chat.type=='private':
        context.bot.forwardMessage("411689167",update.message.chat.id,update.message.message_id)
        
        if (estaDesligado==1) & (update.message.from_user.id!=411689167):
            update.message.reply_text("Bot está em manutenção")
            return
        
        if ((hasattr(update.message,"forward_from_chat")) & (update.message.forward_from_chat!=None)) or ((hasattr(update.message,"forward_from")) & (update.message.forward_from!=None)) or ((hasattr(update.message,"forward_from_message_id")) & (update.message.forward_from_message_id!=None)):
            msgEnviada=encaminhar(update,context)
        elif (hasattr(update.message,"text")) & (update.message.text!=None):
            msgEnviada=echo(update,context)
        elif (hasattr(update.message,"photo")) & (update.message.photo!=None) & (len(update.message.photo)>0):
            print("enviando fto")
            msgEnviada=foto(update,context)
        elif (hasattr(update.message,"video")) & (update.message.video!=None):
            msgEnviada=video(update,context)
        elif (hasattr(update.message,"video_note")) & (update.message.video_note!=None):
            msgEnviada=msg_video(update,context)
        elif (hasattr(update.message,"audio")) & (update.message.audio!=None):
            msgEnviada=arq_audio(update,context)
        elif (hasattr(update.message,"voice")) & (update.message.voice!=None):
            msgEnviada=audio(update,context)
        elif (hasattr(update.message,"dice")) & (update.message.dice!=None):
            msgEnviada=dado(update,context)
        elif (hasattr(update.message,"document")) & (update.message.document!=None):
            msgEnviada=documento(update,context)
        elif (hasattr(update.message,"location")) & (update.message.location!=None):
            msgEnviada=localizacao(update,context)
        elif (hasattr(update.message,"poll")) & (update.message.poll!=None):
            msgEnviada=votacao(update,context)
        elif (hasattr(update.message,"contact")) & (update.message.contact!=None):
            msgEnviada=contato(update,context)
        elif (hasattr(update.message,"sticker")) & (update.message.sticker!=None):
            msgEnviada=figurinha(update,context)
        elif (hasattr(update.message,"game")) & (update.message.game!=None):
            msgEnviada=jogo(update,context)
        else:
            return

        if not (update.message.chat.id in msgsApagadas):
            msgsApagadas[update.message.chat.id]=[]
        (msgsApagadas[update.message.chat.id]).append([msgEnviada.chat.id,msgEnviada.message_id])
        print(msgsApagadas)
    else:
        print(type(chat_id_gp_principal))
        print(type(update.message.chat.id))
        if update.message.chat.id==int(chat_id_gp_principal):
            context.bot.forwardMessage("-1001537212213",update.message.chat.id,update.message.message_id)
            print("alguem enviou uma msg no grupo")

    

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(bot_token, use_context=True)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("delete",delete))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.all,enviarMsg))

    '''
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_handler(MessageHandler(Filters.photo,foto))
    dp.add_handler(MessageHandler(Filters.video,video))
    dp.add_handler(MessageHandler(Filters.audio,arq_audio))
    dp.add_handler(MessageHandler(Filters.voice,audio))
    dp.add_handler(MessageHandler(Filters.contact,contato))
    dp.add_handler(MessageHandler(Filters.dice,dado))
    dp.add_handler(MessageHandler(Filters.document,documento))
    dp.add_handler(MessageHandler(Filters.location,localizacao))
    dp.add_handler(MessageHandler(Filters.poll,votacao))
    dp.add_handler(MessageHandler(Filters.sticker,figurinha))
    dp.add_handler(MessageHandler(Filters.game,jogo))
    dp.add_handler(MessageHandler(Filters.video_note,msg_video))
    '''
    
    # Start the Bot
    #pdater.start_polling()
    updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=bot_token,webhook_url="https://mysterious-beach-24024.herokuapp.com/"+bot_token)
    #updater.bot.setWebhook("https://protected-beach-94373.herokuapp.com/" + bot_token)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()