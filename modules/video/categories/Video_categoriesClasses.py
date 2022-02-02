from modules.video.pageScrape.searchPage import getCategories, getCategoryPic
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo
import threading
import time         

class Categories:

    cats_titles= []
    #cats_thumbs= []
    cats_links= []

    cat_count= -1

    def __init__( self):
        cats= getCategories()

        self.cats_titles= cats['titles']
        #self.cats_thumbs= cats['thumbs']
        #self.cats_links= cats['links']


    def nextCategory(self, update, context):
        isNext= False
        out= "ok"

        for i in range(3):
            if( ( self.cat_count+ 1)< len( self.cats_titles)):

                if( i!= 2 and ( ( self.cat_count+ 1)< len( self.cats_titles)- 1)):
                    isNext= False
                else:
                    isNext= True

                self.cat_count= self.cat_count+ 1 
                #nextCategory= Category( self.cats_titles[ self.cat_count], self.cats_thumbs[ self.cat_count], self.cats_links[ self.cat_count], isNext)
                thumb= getCategoryPic( self.cats_titles[ self.cat_count])
                nextCategory= Category( self.cats_titles[ self.cat_count], thumb, isNext)
                nextCategory.sendCategory( update, context)

            else:
                out= "END"
        
        return out

    def getSelectedCategory( self, update, context):
        title= update.callback_query.message.reply_markup.inline_keyboard[0][0].text
        out= ""

        if( title!= None):
            count= 0
            for i in self.cats_titles:
                if( i== title): 
                    out= i.replace( " ", "+")

                count= count+ 1

        return out

    

class Category:

    cat_title= ""
    cat_thumb= ""
    #cat_link= ""

    isNext= False

    def __init__(self, cat_title, cat_thumb, isNext):
        
        self.cat_title= cat_title
        self.cat_thumb= cat_thumb
        #self.cat_link= cat_link
        self.isNext= isNext

    def sendCategory( self, update, context):
        
        if( not self.isNext):
            markup= InlineKeyboardMarkup([
                [ InlineKeyboardButton( text=self.cat_title, callback_data= "/showCategoryVideo")]

            ])
            
            print("Thumb fin:"+self.cat_thumb)

            temp= context.bot.send_photo(chat_id=update.effective_chat.id, photo=self.cat_thumb, reply_markup= markup)
            
        else:
            markup= InlineKeyboardMarkup([
                [ InlineKeyboardButton( text=self.cat_title, callback_data= "/showCategoryVideo")],
                [ InlineKeyboardButton( text="Next Categories", callback_data= "/nextCategoriesVideo")]

            ])
            
            temp= context.bot.send_photo(chat_id=update.effective_chat.id, photo=self.cat_thumb, reply_markup= markup)
