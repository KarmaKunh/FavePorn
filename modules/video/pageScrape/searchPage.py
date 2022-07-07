
import requests
import re
from random import randint
import tempfile
import modules.Server as Server
import urllib.request


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
        print("url: "+url)

        #video gnocca: 'https://it.pornhub.com/view_video.php?viewkey=ph5e40ef7fb74aa'

        checkLink = url[0:4]

        print( "checkLink: "+ checkLink)
    
        result= []

    
        page= '[]'
        
        #print( 'https://it.pornhub.com/video/get_media?s=eyJrIjoi'+result[0]+'=0')
        #if( checkLink== "http"):

        #    page= get_url( url)
        #    result= re.findall(r'qualityItems(.*)\n', page)
        #    #page= get_url('https://it.pornhub.com/video/get_media?s=eyJrIjoi'+result[0])
        #else:
            
        #    page= get_url( "https://it.pornhub.com"+ url)
        #    result= re.findall(r'qualityItems(.*)\n', page)
        #    #page= get_url('https://it.pornhub.com/video/get_media?s=eyJrIjoi'+result[0])

        if( checkLink== "http"):
                page= get_url( url)
                result= re.findall(r'"videoUrl":"https:.*get_media\?s=eyJrIjoi(.*)=p","quality"', page)
                page= get_url_vid('https://it.pornhub.com/video/get_media?s=eyJrIjoi'+result[0]+'=p')
        else:
                page= get_url( "https://it.pornhub.com"+ url)
                result= re.findall(r'"videoUrl":"https:.*get_media\?s=eyJrIjoi(.*)=p","quality"', page)
                page= get_url_vid('https://it.pornhub.com/video/get_media?s=eyJrIjoi'+result[0]+'=p')
                
    
        print( "Donwloading page")
        f = open( "modules/video/pageScrape/page_check.txt", "w", encoding="utf-8")
        f.write( page)

        f.close()
 
    
        video_link= []
        video_link_def= ""

        #print(result);
    
        if( page!= "[]"):
            #print("\n"+result[ 1])
            
            video_link= re.findall(r'"quality":"720"},.*"videoUrl":"(.*)","quality":"1080"}', page) #cercare video link 1080p
    
            if( len( video_link)== 0 or video_link[ 0]== ""):
                video_link= re.findall(r'"quality":"480"},.*"videoUrl":"(.*)","quality":"720"}', page) #cercare video link 720p
    
                if( len( video_link)== 0 or video_link[ 0]== ""):
                    video_link= re.findall(r'"quality":"240"},.*"videoUrl":"(.*)","quality":"480"}', page) #cercare video link 480p
    
                    if( len( video_link)== 0 or video_link[ 0]== ""):
                        video_link= re.findall(r'.*"videoUrl":"(.*)","quality":"240"}', page) #cercare video link 240p
        else:
                print("Page Link Vuota")
            
        
    
        if( len( video_link)==0):
            #video non trovato
            video_link_def= "Video Non Trovato"
    
        else:
            video_link_def= video_link[0].replace( '\\', '') #Rimove caratteri inutili dal link
    
        
    
        #print( video_link_def)
        
        return video_link_def
    

def getVideoThumb( chat_id, url):
    #page= get_pics_url( url)
    #print( page)
    print( url)
    
    #newUrl= url.replace( "/", "")
    #newUrl= url.replace( "https:", "")
    #newUrl= url.replace( ".", "")
    
    newUrl= re.findall(r'(.*)" onclick', url)[0]
    #path= "users_files/"+str( chat_id)+"_"+url
    #f = open( path, "wb")
    #f.write( page)

    #f.close()
    
    print("url fotoo: "+newUrl)

    return newUrl
    

def getCategories():
    
    r = get_url_desktop( "https://it.pornhub.com/categories")

    titles= []
    links= []

    categories= re.findall(r'<a href=".*" alt=".*" class="js-mxp" data-mxptype="Category" data-mxptext="(.*)">', r)
    print(categories)
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

    res= { 'titles' : categories }

    print(res['titles'])

    return res


def getCategoryPic( name):
    name= name.replace( " ", "+")
    url= "https://it.pornhub.com/video/search?search="+ name

    page= get_url( url)

    thumbs= re.findall(r'data-poster="(.*)" >', page)
        
    #print("Thuuumbs")
    #print(thumbs)

    return thumbs[ randint(0, 6)]






def get_url_vid( url):
        
    headers= {
                'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-encoding' : 'gzip, deflate, br',
                'accept-language' : 'it-IT,it;q=0.9',
                'connection' : 'keep-alive',
                'host' : 'em.phncdn.com',
                'if-modified-since' : 'Sat, 04 Jun 2022 21:24:13 GMT',
                'range' : 'bytes=0-6529755',
                'sec-ch-ua' : '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"',
                'sec-ch-ua-mobile' : '?1',
                'sec-ch-ua-platform' : '"Android"',
                'sec-fetch-dest' : 'document',
                'sec-fetch-mode' : 'navigate',
                'sec-fetch-site' : 'none',
                'sec-fetch-user' : '?1',
                'upgrade-insecure-requests' : '1',
                'user-agent' : 'Mozilla/5.0 (Linux; Android 9; LLD-L31) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Mobile Safari/537.36',
        }
    r = requests.get(url, headers=headers)
    #print( "result="+r.text)
    return r.text


def get_url_desktop( url):
        
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
    r = requests.get(url)
    #print( "result="+r.text)
    return r.text


def get_pics_url( url):
    session = requests.session()
    session.proxies = {}
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
    #print( "result="+r.text)
    return r.text
    



def get_url( url):

        # timeout= 5
        

        headers= {
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language' : 'it-IT,it;q=0.9',
            'connection' : 'keep-alive',
            'cookie' : 'ua=3316012ff19a157bc3b9bafd92915ed7; platform=mobile; bs=t6uvw6jmmp0kg0nsgxmm2otwq40c6bp4; ss=428179870315510892; fg_fcf2e67d6468e8e1072596aead761f2b=65367.100000; atatusScript=hide; _ga=GA1.2.954014431.1643759895; _gid=GA1.2.28735198.1643759895; d_fs=1; local_storage=1; views=6; d_uidb=48323292-0f40-a01a-0a00-4aedd1625981; d_uid=48323292-0f40-a01a-0a00-4aedd1625981',
            'host' : 'it.pornhub.com',
            'if-modified-since' : 'Wed, 24 Feb 2021 16:26:08 GMT',
            'if-none-match' : '"60367e20-2ab"',
            #'sec-ch-ua' : ' Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97',
            'sec-ch-ua-mobile' : '?1',
            'sec-ch-ua-platform' : 'Android',
            'sec-fetch-dest' : 'document',
            'sec-fetch-mode' : 'navigate',
            'sec-fetch-site' : 'none',
            'sec-fetch-user' : '?1',
            'upgrade-insecure-requests' : '1',
            'user-agent' : 'Mozilla/5.0 (Linux; Android 9; LLD-L31) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.98 Mobile Safari/537.36'

        }


        # req = urllib.request.Request( url)

        # req.add_header( 'Accept', '*/*')
        # req.add_header( 'accept-language' , 'it-IT,it;q=0.9,en-IT;q=0.8,en;q=0.7,en-US;q=0.6')
        # req.add_header( 'cache-control' , 'max-age=0')
        # req.add_header( 'connection' , 'keep-alive')
        # req.add_header( 'cookie' , 'ua=915ae7563fe10e1c33345a2bce511386; platform_cookie_reset=mobile; platform=mobile; bs=wxjmgzglt7b9tol36qa9upnv6b2qe35g; ss=813363832411742815; fg_9d12f2b2865de2f8c67706feaa332230=54876.100000; atatusScript=hide; _ga=GA1.2.404420222.1614187370; _gid=GA1.2.25666935.1614187370; d_uidb=dd444781-83c9-4b21-9367-3382fd9ccebe; d_uid=dd444781-83c9-4b21-9367-3382fd9ccebe; local_storage=1; views=6')
        # req.add_header( 'host' , 'it.pornhub.com')
        # req.add_header( 'if-modified-since' , 'Wed, 24 Feb 2021 16:26:08 GMT')
        # req.add_header( 'if-none-match' , '"60367e20-2ab"')
        # req.add_header( 'sec-fetch-mode' , 'same-origin')
        # req.add_header( 'sec-fetch-site' , 'same-origin')
        # req.add_header( 'service-worker' , 'script')
        # req.add_header( 'user-agent' , 'Mozilla/5.0 (Linux; Android 9; LLD-L31) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.116 Mobile Safari/537.36')

        # resp = urllib.request.urlopen(req)
        # content = resp.read().decode('utf-8')

        #print( content)
        r = requests.get(url, headers=headers)

        #print( "result="+r.text)

        return r.text
    
        #return content


    
