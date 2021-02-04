from flask import Flask , render_template , request , redirect , session , url_for
#from flask import session
#import flask
#import MySQLdb
#import requests
#from requests import *
from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector
from mysql import connector
from mysql.connector import Error
from datetime import date
import re
from bs4 import BeautifulSoup
import pandas as pd
from pytrends.request import TrendReq
import json
import csv
import requests
#from fake_useragent import UserAgent
import random

#==============================================
history = []

related_t = []
related_q = []
title = []
word_suggest = []
link = []
google_link = []
VLA = []

title_csv = []
keyword_csv = []
volume_csv = []
value_csv = []
page = 0
i = 0
seed = ['','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']




user_agent_list = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) \
                        Gecko/20100101 Firefox/61.0',
                       'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                        (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36',
                       'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) \
                        Gecko/20100101 Firefox/61.0',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/60.0.3112.113 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/63.0.3239.132 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/66.0.3359.117 Safari/537.36',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) \
                        AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 \
                        Safari/603.3.8',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 \
                        Safari/537.36',
                       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) \
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 \
                        Safari/537.36']

user_agent = random.choice(user_agent_list)

headers = {
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': user_agent,
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.google.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}
i = 0
page = 0




app = Flask(__name__)

#session = session()
app.secret_key = 'secret'
today = date.today()
#session = requests.Session()
#conn =MySQLdb.connect(host = 'sql5.freemysqlhosting.net' , user = 'sql5388820' , password = 'xdKJFsZvwz' , db = 'sql5388820')

#========================Index==================================================


@app.route('/' , methods = ['GET'])
def index():
    return render_template("search1.html")


@app.route('/logout' , methods = ['GET'])
def logout():
    session.pop('loggedin' , None)
    session.pop('username' , None)
    session.pop('id' , None)
    return redirect('/')
#===============================Registration============================================

@app.route('/register' , methods = ['GET' , 'POST'])
def register():
    if request.method == 'POST' :
        try:

                username_info = request.form['Username_register']
                password_info = request.form['Password_register']
                email_info = request.form['Email_register']

                print(username_info)
                print(password_info)
                print(email_info)

                regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

                connection = mysql.connector.connect(host='sql7.freemysqlhosting.net',
                                         database='sql7390049',
                                         user='sql7390049',
                                         password='N47YWSuRL8')

                find_email = 'SELECT * FROM User WHERE EMAIL = "'+email_info+'"'
                c = connection.cursor()
                c.execute(find_email)


                #cursor = conn.cursor()
               # cursor.execute("SELECT username FROM  User WHERE USERNAME='"+Username_register+"'")
              #  user = cursor.fetchone()
                if c.fetchall():
                    print ('User Already  Used')
                    return 'User Already  Used'

                elif len(username_info) < 4 or len(password_info) < 6 or not (re.search(regex,email_info)): 
                    print ('Username and Password Must be lenger than 6 character')
                    return 'Username and Password Must be lenger than 6 character'
                else:
                    print ('You Have Been Registred1')
                    d2 = today.strftime("%m")
                    print ('You Have Been Registred2')
                    d2 = int(d2)
                    print ('You Have Been Registred3')
                    insert = 'INSERT INTO User(USERNAME,PASSWORD,EMAIL,CREDIT , MOUNTH) VALUES(%s,%s,%s,%s,%s)'
                    print ('You Have Been Registred4')
                    
                    cursor = connection.cursor()
                    cursor.execute(insert,[username_info,password_info,email_info,100,d2])
                    connection.commit()
                    
                    return 'You Have Been Registred'
                    connection.close()
                    

                # except:
                
                #         cursor = conn.cursor()
                #         cursor.execute("INSERT INTO User (USERNAME,PASSWORD,EMAIL)VALUES(%s,%s,%s)",(Username_register,Password_register,Email_register))
                #         conn.commit()
                #         return 'You Have Been Registred'
        except:
            return render_template('register2.html')
    elif request.method == 'GET':
        return render_template('register2.html')
    else:
        return 'Method Not Alowed'


#=============================================================================================================================

#=======================================Login============================================================











@app.route('/login' , methods = ['GET' , 'POST'] )
def SignIn():
   # try:
   
    if request.method == 'POST' :

            connection = mysql.connector.connect(host='sql7.freemysqlhosting.net',
                                         database='sql7390049',
                                         user='sql7390049',
                                         password='N47YWSuRL8')
        
            email_info_login = request.form['email']
            password_info_login = request.form['password']







            find_email = 'SELECT * FROM User WHERE EMAIL = %s and PASSWORD = %s'
            d = connection.cursor()
            d.execute(find_email,(email_info_login , password_info_login))
            if d.fetchall() :
                d1 = today.strftime("%m")
                d1 = int(d1)
      
                d2 = today.strftime("%d")
                d2 = int(d1)
                print(d2)

                find_mounth = 'SELECT MOUNTH FROM User WHERE EMAIL = "'+email_info_login+'"'
                a = connection.cursor()
                a.execute(find_mounth)

                ff = a.fetchall()
                for xx in ff:
                    mounth  = int(xx[0])
                print (mounth)
                #return render_template('Search.html')




                if mounth != d1:
                    d1 = str(d1)

                    a.execute("UPDATE User SET CREDIT = 90  WHERE EMAIL ='"+email_info_login+"'")
                    connection.commit()

                    a.execute("UPDATE User SET MOUNTH = '"+d1+"'  WHERE EMAIL ='"+email_info_login+"'")
                    connection.commit()

                    credit_show = 'SELECT CREDIT FROM User  WHERE EMAIL = "'+email_info_login+'" '
                    t = connection.cursor()
                    t.execute(credit_show) 
                    f = t.fetchall()
                    #connection.close()
                    for x in f:
                        credit1  = int(x[0])

                else:
                    pass


                g = connection.cursor()


                g.execute("SELECT USERNAME FROM  User WHERE EMAIL='"+email_info_login+"'")
                account = g.fetchone()


                g.execute("SELECT PASSWORD FROM  User WHERE EMAIL='"+email_info_login+"'")
                account_password = g.fetchone()

                g.execute("SELECT EMAIL FROM  User WHERE EMAIL='"+email_info_login+"'")
                account_email = g.fetchone()
                print ('hoho1')

         
                if account:
                    print ('hoho')
                    session['loggedin'] = True
                    session['username'] = account[0]
                    session['password'] = account_password[0]
                    session['email'] = account_email[0]
                    print('/////////////////////////////////')
                    #return redirect('/HOME')
                    connection.close()


                    return render_template('result1.html' , username =session['username'] )

            else:
                    print('OK0')
                    return render_template('login1.html' , text = 'Password Or Username Incorrect')
                    connection.close()
                    pass


   # except:
     #   print('OK0')
     #   return render_template('login.html' , text = 'Password Or Username Incorrect')
       # connection.close() 
        #print('OK0')

   # except:
        #    return render_template('login.html')


    
    elif request.method == 'GET':
        try:
            if session['loggedin'] == True:
                print('OK1')
                return render_template("result1.html" , username = session['username']  , password = session['password'] , email = session['email'])
                print ("Search.html")
                print(session['username'])
                print(session['password'])
                print(session['email'])
                print('OK1s')
         #  
            else:
                print('OK2')

                return render_template('login1.html')
               # printresult
        except:
            return render_template('login1.html')
           # print('OK3')
            
           # return render_template('login.html')
          #  print('OK3')

    else:
        print('OK4')
        return render_template('login1.html')
       # print('OK4')



#=============================================================================
#================================HOME==========================================
    























#========================Index==================================================
@app.route('/HOME' , methods = ['GET'])
def INDEX():
        #try:
            if request.method == 'GET':

                d = 200
                pub_list = []

                #cursor = conn.cursor()
            
                while d > 0:
                    d = str(d)
                 #   set = cursor.execute("SELECT * FROM  publication WHERE  id = '"+d+"'" )
                    
                    
                   # try: 
                    if set ==1:
                        print ('ok')
                    #    cursor.execute("SELECT * FROM  publication WHERE  id = '"+d+"'" )
                     #   pub_list.append(cursor.fetchone())

                    else:
                        pass
                    d = int(d)
                    d -= 1


                    #cursor.execute("SELECT  commentaire FROM commentaires WHERE (publisherid , pubid , commentaire)VALUES(%s , %s , %s)",(publisherid , publicationID , commentaire))

#********************************

              #  print (pub_list)
               # username = session['username']



                return render_template('search1.html')#, pub_list = pub_list , username = username)

            else:
                return "Method Not Allowed"






#===============================================================================

@app.route('/post_publications' , methods = ['GET'])
def HOME():
    return render_template('post_publications.html')




#======================================================================================




@app.route('/post_publication' , methods = ['POST'])
def post_publication():
    if request.method == 'POST':

        if 'loggedin' in request.session:
            username_of_publication = str(request.session['username'])
            message_publication = str(request.form['message'])



        #    cursor = conn.cursor()
          #  cursor.execute("INSERT INTO publication (publisher,content)VALUES(%s,%s)",(username_of_publication , message_publication))
          #  conn.commit()
            return redirect(url_for('my_publications'))

    else:
        return redirect(url_for('/post_publications'))



@app.route('/testresult' , methods = ['GET' , 'POST'])
def testresult():
    return render_template("result.html")




@app.route('/result' , methods = ['GET' , 'POST'])
def result():
    global search
    global credit1
    connection = mysql.connector.connect(host='sql7.freemysqlhosting.net',
                                         database='sql7390049',
                                         user='sql7390049',
                                         password='N47YWSuRL8')
 
   # credit_set = 'UPDATE User SET CREDIT = CREDIT - 3  WHERE EMAIL = "'+email_info+'" '
    #d = connection.cursor()
   # d.execute(credit_set) 
   # connection.commit()

    # credit_show = 'SELECT CREDIT FROM User  WHERE EMAIL = "'+email_info+'"'
    # t = connection.cursor()
    # t.execute(credit_show) 
    # f = t.fetchall()
   # global credit
   # credit = []
   # for x in f:
       # print (x[0])
       # credit1  = int(x[0])






    connection.close()
    search1 = request.form['search']

    word_list = []
    global screen
    global screen5

    global screen6
    global search2

    page = 0


    #==================

    if len(search1) < 1:
        return "error"
        #showerror(title = "warning", message = "Please Type Word Search")
  #  elif  credit1 < 1:
       # return "error"
       # showerror(title = "warning", message = "You Have Not Credit")
    else:
      #  search1 = 
        # root = Tk() 
        # root.title("Please Wait... It Take Few Moment")

        # label11 = Label(root)# , font = "arial 15 bold")
        # label11.pack(padx=5 , pady = 5)

        # progress = Progressbar(root ,  orient = HORIZONTAL, length = 500, mode = 'determinate') 

        # progress.pack(padx=10 , pady = 10)
 
        # progress['value'] = 5
        # label11.config(text = str(progress['value'])+"%", bg = "white")
        # root.update_idletasks()
        # progress.pack(padx=10 , pady = 10)  

        print (search1)
        keyword = search1
        keyword.replace(" ", "+")

        result = []
        total_rows = len(result) 
        word_list = []
       
        title = []
        link = []
        google_link = []
        u = 0
        i = 0
        d = 0
        page = 0
        while page < 10:
        #  progress['value'] = page/2
        #  label11.config(text = "Google Search , intitle:"+str(progress['value'])+"%", bg = "white")
         # root.update_idletasks()
         # progress.pack(padx=10 , pady = 10) 

          try:
                page = str(page)
                url = ("https://www.google.com/search?q=intitle:{}&client=firefox-b-e&sxsrf=ALeKk03YXhFY_OtDNkERg5RI9JE_4G870A:1609745137110&ei=8cLyX7ycBoy5gwevmJSABg&start={}&sa=N&ved=2ahUKEwj82M3434HuAhWM3OAKHS8MBWAQ8tMDegQIERA8&biw=1525&bih=718".format(search1 , page))
                url = str(url)
                r =requests.get(url , headers = headers , verify=False)
                soup = BeautifulSoup(r.content , "html.parser")

                h3 = soup.findAll("h3")
                for x in h3:
                    print ((x).get_text())
                    title.append((x).get_text())

                page = int(page)
                


                page += 10
          except:

            page = int(page)
            page += 10
            pass


        i = 0
        while i <1:# len(seed):
          try:
            url = "http://suggestqueries.google.com/complete/search?output=firefox&q=" + keyword+seed[i]
            response = requests.get(url, headers = headers , verify=False)
            suggestions = json.loads(response.text)
            for word in suggestions[1]:
              word_list.append(word)
          #  progress['value'] = 50+i
          #  label11.config(text = "Keyword suggestions From Google Trends:"+str(progress['value'])+"%" , bg = "white")
          #  root.update_idletasks()
        #    progress.pack(padx=10 , pady = 10) 



            i += 1
          except:
          #  progress['value'] = 50+i
          #  label11.config(text = "Keyword suggestions From Google Trends:"+str(progress['value'])+"%" , bg = "white")
          #  root.update_idletasks()
          #  progress.pack(padx=10 , pady = 10) 

            i += 1
            pass


        print (word_list)

        lenth = len(word_list)
        file  = open("data.json" , "w")
        file.close()
        i = 0 
        try:

            file = open("data.json" , "w")
            file.close()

            my_data = {
              'country': 'us',
              'currency': 'USD',
              'dataSource': 'gkp',
             'kw[]': word_list
            }
            my_headers = {
             'Accept': 'application/json',
              'Authorization': 'Bearer e3ffd4fff36a2b68be27'
            }
            response = requests.post('https://api.keywordseverywhere.com/v1/get_keyword_data', data=my_data, headers=my_headers , verify=False)
            t = response.json()
            with open('data.json', 'a') as outfile:
                json.dump(t, outfile)
            with open('data.json') as json_file:
                 data = json.load(json_file)
            try:

                print ("volume is : "+str(data['data'][0]['vol']))
                print ("value is : "+str(data['data'][0]['cpc']['value']))
            except:
              #  Not_creditFromKW = True
                pass

        except:
            pass

        return render_template('result1.html' , title = title , word_list = word_list)




#========================================================


@app.route('/delete' , methods = ['POST'])
def delete():
    if request.method == 'POST':
        id_delete = request.form['id']
        id_delete = str(id_delete)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM publication WHERE id = '"+id_delete+"' ")
        conn.commit()
        return render_template('delete_publication.html')
    else:
        return "Method Not Allowed"









@app.route('/commentaire' , methods = ['GET' , 'POST'])
def commentaire():
    if request.method == 'POST':
        publishername = session['username']
        publicationID = request.form['publicationID']
        commentaire = str(request.form['commentaire'])
        publisherid =  session['id']
        publisherid = str(publisherid)
        publicationID = str(publicationID)

       # cursor.execute("SELECT id FROM  publication WHERE publisher =%s AND id = %s",(session['username'] , i))


        cursor = conn.cursor()
        cursor.execute("INSERT INTO commentaires (publishername , publisherid , pubid , commentaire)VALUES(%s , %s , %s , %s)",(publishername , publisherid , publicationID , commentaire))
        conn.commit()

        return (publishername)
    else:
        return 'OK'







@app.route('/publication' , methods = ['GET' , 'POST'])
def publication():

    if 'loggedin' in request.session:
        if request.method == 'POST':
        
    #try:
      
            pb = []
            pbid = []

            x = [] 
            n = []
            i = 0

            cursor = conn.cursor()
            publicationID = request.form['publicationID']
            name = request.form['name']
            content = request.form['content']


            #cursor.execute("SELECT * FROM  commentaires WHERE  pubid = '"+publicationID+"'" )
            while i < 100:
                i = str(i)

                set = cursor.execute("SELECT * FROM  commentaires WHERE pubid =%s AND id = %s",(publicationID , i))
                if set == 1:

                    pb.append(cursor.fetchone())
                    i = int(i)
                    i += 1
                else:
                    i = int(i)
                    i += 1

            publisherid = pb
            print (publisherid) 
            
            for item in pb:
                  x.append(item)



            cursor.execute("SELECT publisher FROM  publication WHERE  id = '"+publicationID+"'" )
            pbid.append(cursor.fetchone())
            for items in pbid:
                n.append(items)


            return render_template('publication.html' ,  n = n , x = x , name = name , content = content , publicationID = publicationID )

    #except:
        #return "aucun commentaire"

        elif  request.method == 'GET':
            return redirect('HOME')
    else: 
        return redirect('login')








@app.route('/add_image' , methods = ['GET' , 'POST'])
def add_image():
    if request.method == 'POST':
        username = flask.request.session['username']
        image1 = request.form['image1']
        cursor = conn.cursor()
        #cursor.execute("INSERT %s INTO user (image) WHERE username = %s ", (  image1, username))

        cursor.execute("UPDATE user SET image = %s WHERE username = %s" , (image1 , username))

        conn.commit()
        return 'ok'
    elif request.method == 'GET':
        return render_template('add_image.html')

    else:
        return "Method Not Allowed"



@app.route('/profile' , methods = ['GET'])
def profile():
    return render_template('/home_plateform.html')


















# url = "https://www.dzmeteo.com/meteo-tizi-ouzou.dz"

# page = requests.get(url)

# soup = BeautifulSoup(page.content , 'html.parser')

# #tenday = soup.find(id = "left")
# day = soup.find(summary="prévisions 10 jours")

# jour = day.find_all("tr" , {"class" : "noalt"})
# nuit = day.find_all("tr" , {"class" : "alt"})

# les_journees = []
# les_mois = []
# jj = []
# disj = []
# tempj = []

# les_nuits = []
# nn = []
# disn = []
# tempn = []

# i = 0
# while True:
#     if i < len(jour):
#         j = jour[i].findAll( "td")
#         n = nuit[i].findAll( "td")

#         les_journees.append((j[0].find('span' , {"class" : "day"})).get_text())
#         les_mois.append((j[0].find('span' , {"class" : "month"})).get_text())

#         jj.append((j[1]).get_text())
#         disj.append((j[2].b).get_text())
#         tempj.append((j[2].span).get_text())

# #====================================
#         les_nuits.append((n[0]).get_text())
#         nn.append((n[1].br).get_text())
#         disn.append((n[1].b).get_text())
#         tempn.append((n[1].span).get_text())



#         i += 1

#     else:
#         break




# @app.route('/yy' , methods = ['GET'])
# def yy():
#     return render_template('yy.html' ,les_journees = les_journees ,les_mois = les_mois,jj = jj, disj = disj ,tempj  = tempj , les_nuits= les_nuits , nn = nn ,disn = disn , tempn = tempn)





# #=================================scrap==news====================================================







# url = "https://www.depechedekabylie.com/"

# page = requests.get(url)

# soup = BeautifulSoup(page.content , 'html.parser')
# news = soup.find(class_= "td-big-grid-wrapper")
# n = news.findAll( "div" , { "class" :"td_module_mx6"})
# first_news = soup.findAll(class_= "td_module_mx5")

# img1 = first_news[0].find('img')
# new1 = img1['title']
# new1img =  img1['data-img-url']
# src1 = first_news[0].find('a')
# link1  = src1['href']


# #print ('==========================================================================')





# list_of_news = []
# links = []
# image_link = []
# i = 0
# while i < len(n):
#     img = n[i].find('img')
#     src = n[i].find('a')

#     list_of_news.append(img['title'])
#     links.append(img['data-img-url'])
#     image_link.append(src['href'])

#     i += 1



# # o = 0

# # while o < len(n):
# #     print (list_of_news[o])
# #     print (links[o])
# #     print (image_link[o])
# #     print ('==========================================================================')
# #     o += 1


# @app.route('/news' , methods = ['GET'])
# def news():
#     return render_template('news.html' , new1 = new1 , link1= link1  , new1img= new1img, list_of_news = list_of_news , links = links , image_link = image_link)













#============================================END=======================================
app.run(debug = True)
#============================================END==========================================
