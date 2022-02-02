from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram.ext import MessageHandler, Filters
import modules.Server as Server
from modules.Session import Session
import modules.video.video_actions as video_actions
#import modules.pics.pics_actions as pics_actions
import datetime


def start_session( update, context):
    Server.sessions[ update.effective_chat.id]= Session( update, context)

def controller_command( update, context):
    command= update.message.text
    out= ""


    if( command== '/teston'):
        Server.isTesting= True
        out= "Server Status : Off ( Testing )"

    elif( command== '/testoff'):
        Server.isTesting= False
        out= "Server Status : On ( not Testing )"

    elif( command== '/v'):
        out= "Numero Video Inviati: "+ str( Server.video_sent)+ "\nLast Reset: "+ str( Server.video_sent_resetDate) 
        
    elif( command== '/p'):
        out= "Numero Pics Inviate: "+ str( Server.pics_sent)+ "\nLast Reset: "+ str( Server.pics_sent_resetDate) 

    elif( command== '/sc'):
        out= "Numero Sessioni avviate: "+ str( Server.session_count())+ "\nLast Reset: "+ str( Server.session_reset_time) 

    elif( command== '/uc'):
        out= "Numero Utenti: "+ str( Server.user_count)+ "\nLast Reset: "+ str( Server.user_count_resetDate)

    elif( command== '/avr'):
        out= "List Ricerche:\n\n" 
        for i in Server.all_video_research:
            out= out+ str( i)+ "\n"
            for z in Server.all_video_research[ i]:
                out= out+ "   "+ str( z)+ '\n'
    
    elif( command== '/au'):
        out= "List Utenti:\n\n" 
        for i in Server.all_users:
            out= out+ str( i)+ "\n"

    elif( command== '/wl'):
        out= "WhiteList:\n\n" 
        for i in Server.whiteList:
            out= out+ str( i)+ "\n"

    elif( command== '/bl'):
        out= "BlackList:\n\n" 
        for i in Server.blackList:
            out= out+ str( i)+ "\n"

    elif( command== '/rv'):
        Server.video_sent= 0
        Server.video_sent_resetDate= datetime.datetime.now()
        out= "Video count resetted\nActual Date: "+ str( datetime.datetime.now())
    elif( command== '/rp'):
        Server.pics_sent= 0
        Server.pics_sent_resetDate= datetime.datetime.now()
        out= "Pics count resetted\nActual Date: "+ str( datetime.datetime.now()) 
    elif( command== '/ras'):
        Server.sessions= {}
        Server.session_reset_time= datetime.datetime.now()
        out= "All Sessions resetted\nActual Date: "+ str( datetime.datetime.now()) 
    elif( command== '/ravr'):
        Server.all_video_research= {}
        Server.all_video_research_resetDate= datetime.datetime.now()
        out= "All Video Research List resetted\nActual Date: "+ str( datetime.datetime.now()) 
    elif( command== '/rau'):
        Server.all_users= []
        Server.all_users_resetDate= datetime.datetime.now()
        out= "All User List resetted\nActual Date: "+ str( datetime.datetime.now()) 
    elif( command== '/ruc'):
        Server.user_count= 0
        Server.user_count_resetDate= datetime.datetime.now()
        out= "User Count resetted\nActual Date: "+ str( datetime.datetime.now())
    elif( command== '/rall'):
        Server.video_sent= 0
        Server.pics_sent= 0
        Server.all_video_research= {}
        Server.all_users= []
        Server.video_sent_resetDate= datetime.datetime.now()
        Server.pics_sent_resetDate= datetime.datetime.now()
        Server.all_video_research_resetDate= datetime.datetime.now()
        Server.all_users_resetDate= datetime.datetime.now()

        out= "Every Statistic resetted\nActual Date: "+ str( datetime.datetime.now()) 

    elif( command.split(' ', 1)[0]== '/addwl'):
        user_input= ( update.message.text).split(' ', 1)[1]
        Server.add_to_whiteList( user_input)

        out= user_input+ " aggiunto alla WhiteList"

    elif( command.split(' ', 1)[0]== '/addbl'):
        user_input= ( update.message.text).split(' ', 1)[1]
        Server.add_to_blackList( user_input)

        out= user_input+ " aggiunto alla BlackList"

    elif( command.split(' ', 1)[0]== '/rmwl'):
        user_input= ( update.message.text).split(' ', 1)[1]
        Server.remove_from_whiteList( user_input)

        out= user_input+ " rimosso dalla WhiteList"

    elif( command.split(' ', 1)[0]== '/rmbl'):
        user_input= ( update.message.text).split(' ', 1)[1]
        Server.remove_from_blackList( user_input)

        out= user_input+ " rimosso dalla BlackList"



    else:
        out= "Comando Errato Bro"


    context.bot.send_message(chat_id=update.effective_chat.id, text= out)

updater = Updater(token='***', use_context=True)
dispatcher = updater.dispatcher


controller_updater = Updater(token='***', use_context=True)
controller_dispatcher = controller_updater.dispatcher


controller_dispatcher.add_handler( CommandHandler('v', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('p', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('avr', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('uc', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('sc', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('au', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('rv', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('rp', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('ravr', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('rau', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('ruc', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('ras', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('rall', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('teston', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('testoff', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('addbl', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('addwl', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('rmbl', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('rmwl', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('wl', controller_command), 1)
controller_dispatcher.add_handler( CommandHandler('bl', controller_command), 1)



dispatcher.add_handler( CommandHandler('start', start_session), 1)

#VIDEOS COMMAND HANDLERS
dispatcher.add_handler( MessageHandler(Filters.text & (~Filters.command), video_actions.echo))

dispatcher.add_handler( CommandHandler('update', video_actions.update))
dispatcher.add_handler( CommandHandler('randomTest', video_actions.randomTest))
dispatcher.add_handler( CommandHandler('vid', video_actions.vid))
dispatcher.add_handler( CommandHandler('help', video_actions.help))

dispatcher.add_handler( CallbackQueryHandler( video_actions.next, pattern='^' + "/nextVideo" + '$'))
dispatcher.add_handler( CallbackQueryHandler( video_actions.nextCategories, pattern='^' + "/nextCategoriesVideo" + '$'))
dispatcher.add_handler( CallbackQueryHandler( video_actions.showCategory, pattern='^' + "/showCategoryVideo" + '$'))




#PICS COMMAND HANDLERS
# dispatcher.add_handler( MessageHandler(Filters.text & (~Filters.command), pics_actions.echo), 1)

# dispatcher.add_handler( CallbackQueryHandler( pics_actions.showPics, pattern='^' + "/showPics" + '$'))
# dispatcher.add_handler( CallbackQueryHandler( pics_actions.nextCategories, pattern='^' + "/nextCategoriesPics" + '$'))
# dispatcher.add_handler( CallbackQueryHandler( pics_actions.showCategory, pattern='^' + "/showCategoryPics" + '$'))



updater.start_polling()
controller_updater.start_polling()



