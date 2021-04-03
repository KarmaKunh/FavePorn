from modules.users.Users import User, Users
import modules.Server as Server
from modules.Utilities import *
import threading
import time

class Session:

    user= None


    #GENERAL ATTRIBUTES

    lastText= "none"

    #VIDEO ATTRIBUTES

    videos= None     #videos_per_user={}
    wait= False      #wait_for_input=[]
    categories= None #categories_per_user= {}
    end= True        #session_ended={ }

    #PICS ATTRIBUTES

    pics= None



    #__INIT__ METHOD

    def __init__( self, update, context):
        self.start( update, context)




    #START METHOD


    def send_log_thread( self, context, text):
        time.sleep(2)
        context.bot.send_message(chat_id=-1001493914748, text= text)
        

    def start(self, update, context):

        users= Users()

        username= ""
        if( update.effective_message.from_user.username!= None):
            username= update.effective_message.from_user.username
        else:
            username= str( update.effective_chat.id)


        if( users.check_user_permission( Server.isTesting, username)):
            
            printText= username+" , "+str( update.effective_chat.id)+" Started the BOT"
            print(  printText)
            thread= threading.Thread( target= self.send_log_thread, args=[ context, printText])
            thread.start()

            Server.all_users.append( username)
            Server.user_count= Server.user_count+ 1

            self.user= User( update.effective_chat.id, username)
            #Pics.per_user_nextOk[ update.effective_chat.id]= True

            context.bot.send_message(chat_id=update.effective_chat.id, text="BOT AGGIORANTO ALLA VERSIONE 2.1.4\n\nNovita':\nCorretto un bug che impediva di usare la funzione Search Video Correttamente\n\n\n", reply_markup= markup_default)

            context.bot.send_message(chat_id=update.effective_chat.id, text="Hi "+username+"!\nWellcome to FavePorn!\n\nHere you can find and download all the porn videos u desire from the site PornHub\n\nTo prevent PornHub from blocking our bot, Every link last for 1 hour, but don't panic ;) All you have to do is answer the expired video with the command /update, and that's it, the link is back to work\n\nYOUR FAP IS OUR PRIORITY\n\n", reply_markup= markup_default)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Hi "+username+"!\nBenvenuto in FavePorn!\n\nQui hai la possibilita di cercare e scaricare tutti i porno che desideri dal sito PornHub\n\nPer evitare che PornHub blocchi il bot, tutti i link hanno la durata di 1 ora, ma non preoccuparti ;) Basta inviare al bot, come risposta al video scaduto, il comando /update ed il gioco e' fatto\n\nLE VOSTRE SEGHE SONO LA NOSTRA PRIORITA'\n\n", reply_markup= markup_default)
            

        

        else:
            if( Server.isTesting):
                printText= username+" , "+ str( update.effective_chat.id)+" not in WhiteList"
                print(  printText)
                thread= threading.Thread( target= Video.send_log_thread, args=[ context, printText])
                thread.start()

                context.bot.send_message(chat_id=update.effective_chat.id, text="Bot in Manutenzione! Torna piu' tardi ;)")
                context.bot.send_message(chat_id=update.effective_chat.id, text= "Bot under maintenance! Come back later ;)")
            else:
                printText= username+" , "+ str( update.effective_chat.id)+" user in BlackList"
                print(  printText)
                thread= threading.Thread( target= Video.send_log_thread, args=[ context, printText])
                thread.start()

                context.bot.send_message(chat_id=update.effective_chat.id, text="Sei sulla BlackList bro! Fottiti, tu non entri [ Sei Stato Bannato ]")
                context.bot.send_message(chat_id=update.effective_chat.id, text= "U are on BlackList bro! Fuck u motherfucker [ You have been banned ]")

    
    #USER METHODS

    def get_username( self):
        return self.user.username


    #VIDEO METHODS

    def set_videos( self, videos):
        self.videos= videos

    def set_categories( self, categories):
        self.categories= categories

    def get_videos( self):
        return self.videos

    def get_categories( self):
        return self.categories

    #PICS METHODS

    def set_pics( self, pics):
        self.pics= pics

    def get_pics( self):
        return self.pics