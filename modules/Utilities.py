
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove


#GENERAL UTILITIES

command_list_ita=[
    'Sta tutto nei bottoni in basso\nSe non li vedi, premi il bottoncino accanto alla tastiera che raffigura 4 quadratini.\n Cosi\' il menu\' apparira\'\n\n\n'
    'COMANDO SPECIALE\n\n/update - Rispondi ad un video inviato con questo comando per rinnovarne il link\n\n',
    'I Link dei video scadono dopo un ora, ma una volta scaduti, se riponderai al video invando il comando /update, il link ritornera\' a funzionare\n\n'


]

command_list_eng=[
    'Everything is on the buttons\nIf you can\'t see them, click the small button at the right of the keyboard showing 4 little squares\n So, the menu\' will appear\n\n\n'
    'SPECIAL COMMAND\n\n/update - Answer to video sent by the bot with this command to renew the link\n\n',
    'Video links last for 1 hour, but once expired, if you answer the video with the command /update, the link will work again\n\n'


]

#VIDEO UTILITIES

markup_default= ReplyKeyboardMarkup([
                [ KeyboardButton( text="Porn Video Categories")],
                # [ KeyboardButton( text="Categorie Hot Pics")],
                [ KeyboardButton( text="Search Video")],
                [ KeyboardButton( text="Search by Link")],
                [ KeyboardButton( text="Help")]

            ])

markup_video_menu= ReplyKeyboardMarkup([
                [ KeyboardButton( text="Main Menu")]

            ])


#PICS UTILITIES

markup_pics_menu= ReplyKeyboardMarkup([
                [ KeyboardButton( text="Next Pic")],
                [ KeyboardButton( text="Menu Principale")]

            ])

markup_null= InlineKeyboardMarkup([


])

markup_null_Keyboard= ReplyKeyboardRemove([

])