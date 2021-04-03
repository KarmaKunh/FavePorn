from modules.Server import blackList, whiteList

class Users:


    def checkWhiteList( self, username):
        out= False
        for i in whiteList:
            if( i== username):
                out= True

        return out

    def checkBlackList( self, username):
        out= True
        for i in blackList:
            if( i== username):
                out= False

        return out

    def check_user_permission( self, isTesting, username):
        out= False
        if( isTesting):
            out= self.checkWhiteList( username)
        else:
            out= self.checkBlackList( username)

        return out


class User:

    chat_id= 0
    username= ""

    def __init__( self, chat_id, username):
        self.chat_id= chat_id
        self.username= username
        
    
