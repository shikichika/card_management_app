# Cards Management App!
#### Video Demo:  <URL https://youtu.be/s8Of6RjEYG0 >
#### Description:
##### This is a simple cards managemet. Nowadays, we have more cards, such as points cards for shopping, patient registration cards, cards for hair solons, library cards, than we can manage them. This app helps you manage your cards! Functions are very simple, need to type the card name, genre and due date if it has. Also, you can make your original genre according to your cards. On the page of index, you can query cards and you don't have to worry about if you take a long time to reach your cards! 

## This app has 6 main fanction 
##### --login
##### --register
##### --index
##### --create recode
##### --update and delete recode
##### --create and delete genre 
##### --logout


## Framework Flask
##### Flask is used. 

## Database Server
##### This app uses RDBMS MySQL. So if you want to connect my app, please add yaml file like that
##### mysql_host : 'your host name'
##### mysql_user : 'your username'
##### mysql_password : 'your password'
##### mysql_db : 'database name'

## Login and Register
##### Python library hashlib is used. Please change hash type when you use it.
##### This app only accept alphanumber

## Index
##### You can search your purpose cards with query, you can reach your cards with partial match. 

## Create recode
##### Here you can make new recodes, then if not find purpose genre, you can create your genre with page "Create genre"

## Update and delete recode
##### In page index, you can choose recode you want to update and delete. Update and delete page consists dynamic url. Here, you can update and delete your recode, if you update recode, card name and genre are required.

## Create and delete genre
##### Here you can create and delete your original genres. If you want to create genre, need to type genre and push the create button, if you want delete genres, need to push the putton next to the genre you want delete. 

## Logout 
##### If you push it, you can logout.


## UI
##### For login and register form, I use free design made by designer Colorlib in "Mockplus" https://www.mockplus.com/blog/post/login-page-examples. In main page bootstrap is used. 

## Technical points
##### I use MySQL, because I've heared that it is most popular RDBMS. There is few documents in which explain how to use flask with MySQL server, but I've done it by myself. For security, I made few urls in HTML and use hash with salt. Name + typed Password. About UI I made responsible design with navber and UI never be broken!


