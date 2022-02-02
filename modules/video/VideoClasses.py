from modules.video.pageScrape.searchPage import getPage, getVideo, getVideoThumb
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo
import threading
import time
import os

def updateLink( update, context):
    message_id= update.message.reply_to_message.message_id
    print( message_id)
    pageKey= ""

    f = open( "users_files/"+ str( update.effective_chat.id)+".txt", "r")
    for line in f:
        lineSplit= line.split( " ")
        if( lineSplit[ 0]== str( message_id)):
            pageKey= lineSplit[ 1]

    pageKey= pageKey.split( "\n")[0]
    pageKey= pageKey.replace( ' ', '')

    newLink= getVideo( pageKey)

    markup= InlineKeyboardMarkup([
            [ InlineKeyboardButton( text="Porn Link", url= newLink)]
            #[ InlineKeyboardButton( text="Next Video", callback_data= "/next")]

        ])

    context.bot.edit_message_reply_markup( chat_id= update.effective_chat.id, message_id= message_id, reply_markup= markup)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Video Link Updated")

    # thread= threading.Thread( target=updateLink_thread, args=[ update, context, pageKey, message_id])
    # thread.start()

    
    
    

def updateLink_thread( update, context, pageKey, message_id):
    
    newLink= ""

    out= False
    
    while( not out):
        try:
            newLink= getVideo( pageKey)
            out= True

        except:
            out= False
            time.sleep( 0.3)

    markup= InlineKeyboardMarkup([
            [ InlineKeyboardButton( text="Porn Link", url= newLink)],
            [ InlineKeyboardButton( text="Next Video", callback_data= "/nextVideo")]

        ])

    context.bot.edit_message_reply_markup( chat_id= update.effective_chat.id, message_id= message_id, reply_markup= markup)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Video Link Updated")
            

class Videos:

    videosPages= ['None']
    videosPrevs= ['None']
    videosTitles= ['None']
    videosThumbs= ['None']

    user_input= ""
    page_count= 1

    videoCount= -1 #videoSelected

    def __init__(self, user_input, typeOf):
        self.user_input= user_input
        res= getPage( user_input, typeOf)

        if( typeOf== "user_input"):
            self.videosPages= res['pages_array']
            self.videosPrevs= res['videoprev_array']
            self.videosTitles= res['titles']
            self.videosThumbs= res['thumbs']
            self.videoCount= -1
        elif( typeOf== "link"):
            self.videosPages= res['pages_array']
            self.videosTitles= res['titles']
            self.videosThumbs= res['thumbs']
            self.videoCount= -1
        
        

    def nextVideo(self, update, context, typeOf):
        if( ( self.videoCount+ 1)< len( self.videosPages)):
            context.bot.send_chat_action(chat_id=update.effective_chat.id, action= "upload_video")

            self.videoCount= self.videoCount+ 1 
            nextVideo= Video( self.videosPages[ self.videoCount], self.videosPrevs[ self.videoCount], self.videosTitles[ self.videoCount], self.videosThumbs[ self.videoCount])
            nextVideo.sendVideo( update, context, typeOf)

            return nextVideo

        else:
            self.page_count= self.page_count+ 1
            res= getPage( self.user_input+ "&page="+ str( self.page_count), "user_input")

            self.videosPages= res['pages_array']
            self.videosPrevs= res['videoprev_array']
            self.videosTitles= res['titles']
            self.videosThumbs= res['thumbs']
            self.videoCount= -1

    

class Video:

    video_title= ""
    video_thumb= ""
    video_prev= ""
    video_page= ""
    video_link= ""

    def __init__(self, video_page, video_prev, video_title, video_thumb):
        
        self.video_page= video_page
        self.video_prev= video_prev
        self.video_title= video_title
        self.video_thumb= video_thumb
        self.video_link= getVideo( video_page)
        print( self.video_thumb)

    def sendVideo( self, update, context, typeOf):

        markup= None

        if( typeOf== "user_input"):
            markup= InlineKeyboardMarkup([
                [ InlineKeyboardButton( text="Porn Link", url= self.video_link)],
                [ InlineKeyboardButton( text="Next Video", callback_data= "/nextVideo")]

            ])

            thumb= getVideoThumb( update.effective_chat.id, self.video_thumb)
        
            temp= context.bot.send_photo(chat_id=update.effective_chat.id, photo=thumb, caption= self.video_title, reply_markup= markup)

            os.remove( thumb)
            
            thread= threading.Thread( target=self.videoThread, args=[ temp, markup, update, context])
            thread.start()

        elif( typeOf== "link"):
            markup= InlineKeyboardMarkup([
                [ InlineKeyboardButton( text="Porn Link", url= self.video_link)]

            ])
        
            temp= context.bot.send_photo(chat_id=update.effective_chat.id, photo= self.video_thumb, caption= self.video_title, reply_markup= markup)

        

        f = open( "users_files/"+ str( update.effective_chat.id)+".txt", "a")
        f.write( str( temp.message_id)+ " "+ self.video_page+"\n")
        f.close()


    def videoThread( self, temp, markup, update, context):
        try:
            context.bot.edit_message_media( chat_id=update.effective_chat.id, message_id= temp.message_id, media=InputMediaVideo( media= self.video_prev, caption= self.video_title), reply_markup= markup)
        except:
            pass
