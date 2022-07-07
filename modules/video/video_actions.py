
import modules.Server as Server
from modules.users.Users import Users
from modules.Utilities import *

from modules.video.VideoClasses import *
from modules.video.categories.Video_categoriesClasses import *
from modules.video.pageScrape.searchPage import getCategories

import threading
import time


def echo( update, context):
    if update.effective_chat.id in Server.sessions: 
        thread= threading.Thread( target= echo_thread, args=[ update, context])
        thread.start()
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text= "Session expired, click here to restart --> /start <--", reply_markup= markup_null)


def echo_thread(update, context):

    if ( Server.sessions[ update.effective_chat.id].end):
        Server.sessions[ update.effective_chat.id].end= False

        username= Server.sessions[ update.effective_chat.id].get_username()

        text= ( update.message.text).lower()

        users= Users()

        if( not text== "next video"):
            printText= username+" , "+ str( update.effective_chat.id)+"|  echo "+ update.message.text
            print(  printText)
            
            thread= threading.Thread( target= send_log_thread, args=[ context, printText])
            thread.start()

        if( users.check_user_permission( Server.isTesting, username)):

            if( not Server.sessions[ update.effective_chat.id].wait):
                if( text== "porn video categories"):
                    categories( update, context)

                elif( text== "next video"):
                    context.bot.delete_message( chat_id=update.effective_chat.id, message_id= ( update.message.message_id))
                    next( update, context)

                elif( text== "search video"):
                    Server.sessions[ update.effective_chat.id].input_type= "user_input"
                    Server.sessions[ update.effective_chat.id].wait= True

                    context.bot.send_message(chat_id=update.effective_chat.id, text= "Inserisci dei parametri di ricerca per trovare i porno che preferisci\nEsempio: Inserisci la parola 'Milf' per trovare video inerenti la parola inserit\nPuoi Inserire anche nomi di Attrici o di Utenti PornHub", reply_markup= markup_video_menu)
                    context.bot.send_message(chat_id=update.effective_chat.id, text= "👇 Scrivimi cosa stai cercando 👇", reply_markup= markup_video_menu)
                    context.bot.send_message(chat_id=update.effective_chat.id, text= "👇 Write me what u are looking for 👇", reply_markup= markup_video_menu)


                elif( text== "search by link"):
                    Server.sessions[ update.effective_chat.id].input_type= "link"
                    Server.sessions[ update.effective_chat.id].wait= True

                    context.bot.send_message(chat_id=update.effective_chat.id, text= "Inserisci il Link pornHub del video che stai cercando\nEsempio:\nInserisci \\https://it.pornhub.com/view_video.php?viewkey=ph5e40ef7fb74aa\\ per trovare il relativo video", reply_markup= markup_video_menu)
                    context.bot.send_message(chat_id=update.effective_chat.id, text= "👇 Inserisci il link qui sotto 👇", reply_markup= markup_video_menu)
                    context.bot.send_message(chat_id=update.effective_chat.id, text= "👇 Insert Link down Here 👇", reply_markup= markup_video_menu)


                elif( text== "main menu"):
                    context.bot.send_message(chat_id=update.effective_chat.id, text= "😈 Choose an Option 😈", reply_markup= markup_default)

                elif( text== "help"):
                    help( update, context)
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text= "Mhh, sembra che tu non abbia selezionato alcuna opzione\nSe ti trovi in difficolta con i comandi, usa /help\n\n😈 Altrimenti Scegli dal Menu 😈", reply_markup= markup_default)
                    context.bot.send_message(chat_id=update.effective_chat.id, text= "Mhh, it seems you didn't choose any option from the menu\nIf u need help, use /help\n\n😈 Or else, choose an Option 😈", reply_markup= markup_default)

            else:
                if( not text== "main menu"):
                    Server.sessions[ update.effective_chat.id].wait= False
                    if( username in Server.all_video_research):
                        Server.all_video_research[ username].append( text)
                    else:
                        Server.all_video_research[ username]= [ text]

                    if( Server.sessions[ update.effective_chat.id].input_type== "user_input"):
                        vid_not_command( update, context, text, "user_input")
                    elif( Server.sessions[ update.effective_chat.id].input_type== "link"):
                        context.bot.delete_message( chat_id=update.effective_chat.id, message_id= ( update.message.message_id))
                        checkLink = text[0:4]
                        if( checkLink!= "http"):
                            context.bot.send_message(chat_id=update.effective_chat.id, text= "Link Non Valido\n\nDeve essere nel formato: 'https...view_video.php?viewkey=...", reply_markup= markup_default)
                            context.bot.send_message(chat_id=update.effective_chat.id, text= "Link Not Valid\n\nIt has to be like this: 'https...view_video.php?viewkey=...", reply_markup= markup_default)
                        else:
                            vid_not_command( update, context, text, "link")
                            
                    
                else:
                    Server.sessions[ update.effective_chat.id].wait= False
                    context.bot.delete_message( chat_id=update.effective_chat.id, message_id= ( update.message.message_id- 1))
                    context.bot.send_message(chat_id=update.effective_chat.id, text= "😈 Choose an Option 😈", reply_markup= markup_default)
        
        else:
            if( Server.isTesting):
                context.bot.send_message(chat_id=update.effective_chat.id, text= "Bot in Manutenzione! Torna piu' tardi ;)", reply_markup= markup_video_menu)
                context.bot.send_message(chat_id=update.effective_chat.id, text= "Bot under maintenance! Come back later ;)", reply_markup= markup_video_menu)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text= "Sei sulla BlackList bro! Fottiti, tu non entri [ Sei Stato Bannato ]", reply_markup= markup_video_menu)
                context.bot.send_message(chat_id=update.effective_chat.id, text= "U are on BlackList bro! Fuck u motherfucker [ You have been banned ]", reply_markup= markup_video_menu)

        Server.sessions[ update.effective_chat.id].end= True


def vid( update, context):
    if update.effective_chat.id in Server.sessions: 
        thread= threading.Thread( target= vid_thread, args=[ update, context])
        thread.start()
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text= "Session expired, click here to restart --> /start <--", reply_markup= markup_null)

def vid_thread(update, context):

    username= Server.sessions[ update.effective_chat.id].get_username()

    users= Users()

    if( users.check_user_permission( Server.isTesting, username)):
        user_input= ( update.message.text).split(' ', 1)

        if len( user_input)== 2:
            printText= username+" , "+ str( update.effective_chat.id)+"|  /vid "+user_input[ 1]
            print( printText)
            thread= threading.Thread( target= send_log_thread, args=[ context, printText])
            thread.start()

            user_input = user_input[1].replace(" ", "+")

            videos= Videos( user_input, "user_input")
            
            Server.sessions[ update.effective_chat.id].set_videos( videos)

            nextVideo= ( Server.sessions[ update.effective_chat.id].get_videos()).nextVideo( update, context, "user_input")

            Server.video_sent= Server.video_sent+1

            if( username in Server.all_video_research):
                Server.all_video_research[ username].append( user_input)
            else:
                Server.all_video_research[ username]= [ user_input]

            time.sleep(0.5)

        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="comando incompleto, specifica cosa cercare\n\n/vid 'NOME ATTRICE oppure NOME VIDEO oppure CATEGORIA'")
            context.bot.send_message(chat_id=update.effective_chat.id, text="incomplete command, specify what u are looking for\n\n/vid 'PORNSTAR NAME or VIDEO NAME or CATEGORY'")

    else:
        if( Server.isTesting):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Bot in Manutenzione! Torna piu' tardi ;)", reply_markup= markup_video_menu)
            context.bot.send_message(chat_id=update.effective_chat.id, text= "Bot under maintenance! Come back later ;)", reply_markup= markup_video_menu)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Sei sulla BlackList bro! Fottiti, tu non entri [ Sei Stato Bannato ]", reply_markup= markup_video_menu)
            context.bot.send_message(chat_id=update.effective_chat.id, text= "U are on BlackList bro! Fuck u motherfucker [ You have been banned ]", reply_markup= markup_video_menu)

def next( update, context):

    if update.effective_chat.id in Server.sessions: 
        users= Users()
        username= Server.sessions[ update.effective_chat.id].get_username()

        if( users.check_user_permission( Server.isTesting, username)):

            if update.effective_chat.id in Server.sessions:
                thread= threading.Thread( target=nextThread, args=[ update, context])
                thread.start()
                Server.video_sent= Server.video_sent+1
                time.sleep(0.6)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text= "Session expired, click here to restart --> /start <--", reply_markup= markup_null)

        else:
            if( Server.isTesting):
                context.bot.send_message(chat_id=update.effective_chat.id, text= "Bot in Manutenzione! Torna piu' tardi ;)", reply_markup= markup_video_menu)
                context.bot.send_message(chat_id=update.effective_chat.id, text= "Bot under maintenance! Come back later ;)", reply_markup= markup_video_menu)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text= "Sei sulla BlackList bro! Fottiti, tu non entri [ Sei Stato Bannato ]", reply_markup= markup_video_menu)
                context.bot.send_message(chat_id=update.effective_chat.id, text= "U are on BlackList bro! Fuck u motherfucker [ You have been banned ]", reply_markup= markup_video_menu)

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text= "Session expired, click here to restart --> /start <--", reply_markup= markup_null)



def nextThread( update, context):

    username= Server.sessions[ update.effective_chat.id].get_username()


    printText= username+" , "+ str( update.effective_chat.id)+"|  /next"
    print( printText)

    thread= threading.Thread( target= send_log_thread, args=[ context, printText])
    thread.start()

    nextVideo= ( Server.sessions[ update.effective_chat.id].get_videos()).nextVideo( update, context, "user_input")

    

def update( update, context):
    try:
        reply_to= update.message.reply_to_message

        if( reply_to.reply_markup.inline_keyboard[0][0].text!= None and reply_to.reply_markup.inline_keyboard[0][0].text=="Porn Link"):
            updateLink( update, context)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Il comando /update serve per ricaricare link video scaduti. Invia questo comando come 'risposta' al video che devi ricaricare", reply_markup= markup_default)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Command /update is used to reload expired video links. Send this command as a 'response' to the video u want to reload", reply_markup= markup_default)
    except:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Il comando /update serve per ricaricare link video scaduti. Invia questo comando come 'risposta' al video che devi ricaricare", reply_markup= markup_default)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Command /update is used to reload expired video links. Send this command as a 'response' to the video u want to reload", reply_markup= markup_default)



def help(update, context):
    if update.effective_chat.id in Server.sessions: 
        username= Server.sessions[ update.effective_chat.id].get_username()

        printText= username+" , "+ str( update.effective_chat.id)+"|  /help"
        print( printText)

        thread= threading.Thread( target= send_log_thread, args=[ context, printText])
        thread.start()

        users= Users()

        if( users.check_user_permission( Server.isTesting, username)):
            txt= "NEED SOME HELP? WHAT YOU NEED TO KNOW IS HERE: \n"
            for c in command_list_eng:  
                txt= txt+ c+ "\n"

            context.bot.send_message(chat_id=update.effective_chat.id, text= txt)

            txt= "TI SERVE UNA MANO? ECCO COSA DEVI SAPERE: \n"
            for c in command_list_ita:  
                txt= txt+ c+ "\n"

            context.bot.send_message(chat_id=update.effective_chat.id, text= txt)

        else:
            if( Server.isTesting):
                context.bot.send_message(chat_id=update.effective_chat.id, text="Bot in Manutenzione! Torna piu' tardi ;)", reply_markup= markup_video_menu)
                context.bot.send_message(chat_id=update.effective_chat.id, text= "Bot under maintenance! Come back later ;)", reply_markup= markup_video_menu)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Sei sulla BlackList bro! Fottiti, tu non entri [ Sei Stato Bannato ]", reply_markup= markup_video_menu)
                context.bot.send_message(chat_id=update.effective_chat.id, text= "U are on BlackList bro! Fuck u motherfucker [ You have been banned ]", reply_markup= markup_video_menu)
    
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text= "Session expired, click here to restart --> /start <--", reply_markup= markup_null)
    



def categories( update, context):
    if update.effective_chat.id in Server.sessions: 
        username= Server.sessions[ update.effective_chat.id].get_username()

        printText= username+" , "+ str( update.effective_chat.id)+"|  /categories"
        print( printText)

        thread= threading.Thread( target= send_log_thread, args=[ context, printText])
        thread.start()

        categories= Categories()
        Server.sessions[ update.effective_chat.id].set_categories( categories)

        nextCategories= ( Server.sessions[ update.effective_chat.id].get_categories()).nextCategory( update, context)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text= "Session expired, click here to restart --> /start <--", reply_markup= markup_null)


def nextCategories( update, context):

    if update.effective_chat.id in Server.sessions:
        users= Users()
        username= Server.sessions[ update.effective_chat.id].get_username()
        
        if( users.check_user_permission( Server.isTesting, username)):
        
            username= Server.sessions[ update.effective_chat.id].get_username()

            printText= username+" , "+ str( update.effective_chat.id)+"|  /nextCategories"
            print( printText)

            thread= threading.Thread( target= send_log_thread, args=[ context, printText])
            thread.start()

            nextCategories= ( Server.sessions[ update.effective_chat.id].get_categories()).nextCategory( update, context)
            if( nextCategories== "END"):
                context.bot.send_message(chat_id=update.effective_chat.id, text="Fine Lista Categorie")
        
        else:
            if( Server.isTesting):
                context.bot.send_message(chat_id=update.effective_chat.id, text= "Bot in Manutenzione! Torna piu' tardi ;)", reply_markup= markup_video_menu)
                context.bot.send_message(chat_id=update.effective_chat.id, text= "Bot under maintenance! Come back later ;)", reply_markup= markup_video_menu)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text= "Sei sulla BlackList bro! Fottiti, tu non entri [ Sei Stato Bannato ]", reply_markup= markup_video_menu)
                context.bot.send_message(chat_id=update.effective_chat.id, text= "U are on BlackList bro! Fuck u motherfucker [ You have been banned ]", reply_markup= markup_video_menu)
    
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text= "Session expired, click here to restart --> /start <--", reply_markup= markup_null)

def showCategory( update, context):
    if update.effective_chat.id in Server.sessions: 
        username= Server.sessions[ update.effective_chat.id].get_username()

        printText= username+" , "+ str( update.effective_chat.id)+"|  /showCategory"
        print( printText)

        thread= threading.Thread( target= send_log_thread, args=[ context, printText])
        thread.start()

        vid_not_command( update, context, ( Server.sessions[ update.effective_chat.id].get_categories()).getSelectedCategory( update, context), "user_input")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text= "Session expired, click here to restart --> /start <--", reply_markup= markup_null)



def randomTest( update, context):
    markup= ReplyKeyboardMarkup([
                [ KeyboardButton( text="Video", callback_data= "/vid")],
                [ KeyboardButton( text="Categories", callback_data= "/categories")]

            ])
    
    context.bot.send_photo(chat_id=update.effective_chat.id, photo="https://di.phncdn.com/is-static/images/categories/(m=q6X556TbetZD8zjadOf)(mh=2MEkxOvC3Z6yb28c)roku_25.jpg", caption= "bella", reply_markup= markup)


def vid_not_command( update, context, url, input_type):
    thread= threading.Thread( target= vid_not_command_thread, args=[ update, context, url, input_type])
    thread.start()
    time.sleep( 0.6)

def vid_not_command_thread( update, context, url, input_type):

    username= Server.sessions[ update.effective_chat.id].get_username()

    users= Users()

    if( users.check_user_permission( Server.isTesting, username)):

        context.bot.send_message(chat_id=update.effective_chat.id, text="😈🥵 Enjoy 🥵😈", reply_markup= markup_video_menu)

        videos= Videos( url, input_type)

        Server.sessions[ update.effective_chat.id].set_videos( videos)

        if( videos.videosTitles== []):
            if ( url[0:4]=="http"):
                context.bot.send_message(chat_id=update.effective_chat.id, text="Video non Trovato :(\nControlla che il link sia corretto", reply_markup= markup_video_menu)
                context.bot.send_message(chat_id=update.effective_chat.id, text="Video not Found :(\nCheck if your link is correct", reply_markup= markup_video_menu)
            
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Nessun video Trovato :(\nAlcune parole o parametri di ricerca non sono consentiti da pornhub poiche potrebbero violare le leggi nazionali vigenti in materia di pornografia", reply_markup= markup_video_menu)
                context.bot.send_message(chat_id=update.effective_chat.id, text="We can't find any video :(\nSome words are not allowed by pornhub because they might not be legal in your country", reply_markup= markup_video_menu)
        
        else:
            nextVideo= ( Server.sessions[ update.effective_chat.id].get_videos()).nextVideo( update, context, input_type)

            Server.video_sent= Server.video_sent+1

        
    else:
        if( Server.isTesting):
            context.bot.send_message(chat_id=update.effective_chat.id, text="Bot in Manutenzione! Torna piu' tardi ;)", reply_markup= markup_video_menu)
            context.bot.send_message(chat_id=update.effective_chat.id, text= "Bot under maintenance! Come back later ;)", reply_markup= markup_video_menu)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Sei sulla BlackList bro! Fottiti, tu non entri [ Sei Stato Bannato ]", reply_markup= markup_video_menu)
            context.bot.send_message(chat_id=update.effective_chat.id, text= "U are on BlackList bro! Fuck u motherfucker [ You have been banned ]", reply_markup= markup_video_menu)



def send_log_thread( context, text):
    time.sleep(2)
    context.bot.send_message(chat_id=-1001493914748, text= text)
