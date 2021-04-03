import datetime

#SERVER STATUS ATTRIBUTES

isTesting= False

sessions= {}


whiteList= [ 
    'KarmaKunh'

]

blackList= [ 

]



#SERVER STATISTICS ATTRIBUTES

pics_sent= 0
video_sent= 0
user_count= 0
all_video_research= {}
all_users= []


session_reset_time= datetime.datetime.now()
user_count_resetDate= datetime.datetime.now()
video_sent_resetDate = datetime.datetime.now()
pics_sent_resetDate = datetime.datetime.now()
all_video_research_resetDate = datetime.datetime.now()
all_users_resetDate = datetime.datetime.now()


#SERVER STATISTICS METHODS

def session_count():
    return len( sessions)


def add_to_whiteList( username):
    whiteList.append( username)

def remove_from_whiteList( username):
    try:
        whiteList.remove( username)
    except:
        print("error")
        pass

def add_to_blackList( username):
    blackList.append( username)

def remove_from_blackList( username):
    try:
        blackList.remove( username)
    except:
        print("error")
        pass
    