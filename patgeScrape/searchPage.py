import requests
import re
from random import randint
import tempfile


def getPage( input, typeOf):

        if( typeOf== "user_input"):
            url= "https://it.pornhub.com/video/search?search="+ input


            page= get_url( url)

            result= []
            titles= []
            pages_array= []
            videoprev_array= []

            result= re.findall(r'href="(.*)"\s{17}data-webm="(.*)" data-poster=', page)
            titles= re.findall(r'alt="(.*)"\n\t{7}data-path="', page)
            thumbs= re.findall(r'data-poster="(.*)" >', page)

            for i in result:
                    pages_array.append( i[0])

            for i in result:
                    videoprev_array.append( i[1])
            
            res= { 'pages_array': pages_array, 'videoprev_array': videoprev_array, 'titles': titles, 'thumbs': thumbs}


        elif( typeOf== "link"):
            url= input
            page= get_url( url)

            title= []
            thumb= []

            title= re.findall(r'<meta property="og:title" content="(.*)" \/>', page)
            thumb= re.findall(r'<meta property="og:image" content="(.*)" \/>', page)


            res= { 'pages_array': [ url], 'titles': title, 'thumbs': thumb}
        

        return res





def getVideo( url):

        #video gnocca: 'https://it.pornhub.com/view_video.php?viewkey=ph5e40ef7fb74aa'

        checkLink = url[0:4]

        page= None

        print( "checkLink: "+ checkLink)

        if( checkLink== "http"):
            page= get_url( url)
        else:
            page= get_url( "https://it.pornhub.com"+ url)

        

        
    
        result= []
    
        result= re.findall(r'get_media\?s\=eyJrIjoi(.*)\=0","quality"', page)
    
        page= '[]'
        
        #print( 'https://it.pornhub.com/video/get_media?s=eyJrIjoi'+result[0]+'=0')
        if( checkLink== "http"):
            while( page== '[]'):
                page= get_url( url)
                result= re.findall(r'get_media\?s\=eyJrIjoi(.*)\=0","quality"', page)
                page= get_url('https://it.pornhub.com/video/get_media?s=eyJrIjoi'+result[0]+'=0')
        else:
            while( page== '[]'):
                page= get_url( "https://it.pornhub.com"+ url)
                result= re.findall(r'get_media\?s\=eyJrIjoi(.*)\=0","quality"', page)
                page= get_url('https://it.pornhub.com/video/get_media?s=eyJrIjoi'+result[0]+'=0')
    
        #print( page)
        
    
        video_link= []
        video_link_def= ""
    
        if( page!= "[]" ):
            
            video_link= re.findall(r'"720"},.*"videoUrl":"(.*)","quality":"1080"}', page) #cercare video link 1080p
    
            if( len( video_link)== 0):
                video_link= re.findall(r'"480"},.*"videoUrl":"(.*)","quality":"720"}', page) #cercare video link 720p
    
                if( len( video_link)== 0):
                    video_link= re.findall(r'"240"},.*"videoUrl":"(.*)","quality":"480"}', page) #cercare video link 480p
    
                    if( len( video_link)== 0):
                        video_link= re.findall(r'"videoUrl":"(.*)","quality":"240"}', page) #cercare video link 240p
                        
        else:
            #CERCA VIDEO LINK DIRETTAMENTE NELLA PAGINA DEL VIDEO
    
            video_link= re.findall() #cercare video link 1080p
            
            if( video_link== ""):
                video_link= re.findall() #cercare video link 720p
    
                if( video_link== ""):
                    video_link= re.findall() #cercare video link 480p
    
                    if( video_link== ""):
                        video_link= re.findall() #cercare video link 240p
    
            
        
    
        if( len( video_link)==0):
            #video non trovato
            video_link_def= "Video Non Trovato"
    
        else:
            video_link_def= video_link[0].replace( '\\', '') #Rimove caratteri inutili dal link
    
        
    
        #print( video_link_def)
        
        return video_link_def
    

def getVideoThumb( chat_id, url):
    page= get_pics_url( url)
    #print( page)
    print( url)
    
    url= url.replace( "/", "")
    url= url.replace( "https:", "")
    url= url.replace( ".", "")

    path= "users_files/"+str( chat_id)+"_"+url
    f = open( path, "wb")
    f.write( page)

    f.close()

    return path
    

def getCategories():
    
    r = get_url_desktop( "https://it.pornhub.com/categories")

    titles= []
    links= []

    categories= re.findall(r'<a href=".*" alt=".*" class="js-mxp" data-mxptype="Category" data-mxptext="(.*)">', r)
    #thumbs= re.findall(r'src=".*"\n\t{8}data-thumb_url="(.*)"', r)

    # for i in categories:
    #     links.append( i[0])

    # for i in categories:
    #     titles.append( i[1])

    #res= { 'titles' : titles, 'thumbs' : thumbs, 'links' : links}
    try:
        categories.remove("Gay")
    except:
        pass
    try:
        categories.remove("Maschi Bisessuali")
    except:
        pass
    try:
        categories.remove("Autoerotismo Maschile")
    except:
        pass
    try:
        categories.remove("Uomini Muscolosi")
    except:
        pass

    res= { 'titles' : categories}

    return res


def getCategoryPic( name):
    name= name.replace( " ", "+")
    url= "https://it.pornhub.com/video/search?search="+ name

    page= get_url( url)

    thumbs= re.findall(r'data-poster="(.*)" >', page)

    return thumbs[ randint(0, 6)]









def get_url_desktop( url):

    r = requests.get( url)

    return r.text


def get_pics_url( url):

    r = requests.get( url)

    return r.content
    



def get_url( url):

        # timeout= 5

        headers= {
            'Accept' : '*/*',
            'accept-language' : 'it-IT,it;q=0.9,en-IT;q=0.8,en;q=0.7,en-US;q=0.6',
            'cache-control' : 'max-age=0',
            'connection' : 'keep-alive',
            'cookie' : 'ua=915ae7563fe10e1c33345a2bce511386; platform_cookie_reset=mobile; platform=mobile; bs=wxjmgzglt7b9tol36qa9upnv6b2qe35g; ss=813363832411742815; fg_9d12f2b2865de2f8c67706feaa332230=54876.100000; atatusScript=hide; _ga=GA1.2.404420222.1614187370; _gid=GA1.2.25666935.1614187370; d_uidb=dd444781-83c9-4b21-9367-3382fd9ccebe; d_uid=dd444781-83c9-4b21-9367-3382fd9ccebe; local_storage=1; views=6',
            'host' : 'it.pornhub.com',
            'if-modified-since' : 'Wed, 24 Feb 2021 16:26:08 GMT',
            'if-none-match' : '"60367e20-2ab"',
            'sec-fetch-mode' : 'same-origin',
            'sec-fetch-site' : 'same-origin',
            'service-worker' : 'script',
            'user-agent' : 'Mozilla/5.0 (Linux; Android 9; LLD-L31) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.116 Mobile Safari/537.36'

        }

        r = requests.get(url, headers=headers)

        return r.text
    


    