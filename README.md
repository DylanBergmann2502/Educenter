# Educenter

Educenter is a university web application built for the ease of use for admins, teachers, and students. Written Django and Django Rest Framework, it offers various functionalities such as looking and applying for online courses, enrolling in interesting upcoming events, staying tune with the newest blog posts, etc. 


## 1. Demo Pictures
Below are some of the demo pictures of Educenter. For more, please visit [here]! 

- Demo 1 - [Home Page]
- Demo 2 - [Course List]
- Demo 3 - [Blog List]
- Demo 4 - [Event List]
- Demo 5 - [Teacher List]
- Demo 6 - [Login]
- Demo 7 - [Unit and Integration Tests] 


## 2. Try out Educenter
Some prequisites before you can explore Educenter: 
1. Make sure that you have Python and Redis installed on your machine. If not, you can find the links down here
- [Python]  
- [Redis]
2. After having both available on your machine, go to your terminal and execute this command to make sure the redis server is running (if you are on Windows, there is no need, since it is auto enabled on startup by the MSI installer)
    ```sh
    redis-server
    ```
3. Clone the project to your desired folder. Go to the command line, navigate inside that folder where you put the project. Install all the dependencies for our project by running in the terminal the command 
    ```sh
    pip install -r requirements.txt
    ```
4. Spin up the development server by running 
    ```sh
    py manage.py runserver
    ```
5. Start your favorite web browser, go to 
    ```sh
    http://127.0.0.1:8000/
    ```
6. Go check it out !!! 


## 3. Testing

There are two types of tests that you can perform with Educenter: "Unit & Integration Tests" and "Functional Tests".

To run "Unit & Integration Tests", run the command: 
```sh
py manage.py test
```
>Note: For Unit and Integration Tests, some tests may fail due to the implementation of caching.

To run "Functional Tests", run the command:
```sh
py manage.py test test_functional
```
>Note: For "Functional Tests", you must make sure that the development server is running because these are live server tests. And also, they can take a lot of time to complete (40mins to 1h).  

## 4. Navigate through the app directories

All directories with the prefix "api_" are Django Rest Framework-related. The following directories are Django-related: academics, postings, users and main (main holds everything related to the home page, about page, and contact page). Inside each of these directories, you will find a "tests" directory that hold all the unit and integration tests.

"Media" is for static files, "static" for front end files (CSS/Javscript), and "template" for HTML files.  

## 5. Some other notes

1. For ease of installation, I will dockerize everything in the future (this is currently underway).
2. Usually in a professional setting, the database(db.sqlite3) and static files(media) should not be committed to Github. But since this is a demo project, I think it is acceptable to do so. Please, don't hold this against me :'>.
3. Disclaimer: While the backend is entirely my work, the frontend belongs to [Themefisher](https://themefisher.com/). I used one of their free templates (with some modification to their codes) to create this website. 

## 6. My Contact
1. Email: dylanbergmann2502@gmail.com OR locducnguyen2001@gmail.com
2. Tel: + 84 767 170 477
3. Facebook: https://www.facebook.com/profile.fine
## Thank you !!!



[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
    
   [here]: <https://github.com/DylanBergmann2502/Web-Development/tree/main/python_django/projects/django_educenter/demo_pictures>
   [Home Page]: <https://github.com/DylanBergmann2502/Web-Development/blob/main/python_django/projects/django_educenter/demo_pictures/Demo%201%20-%20Home.png>
   [Course List]: <https://github.com/DylanBergmann2502/Web-Development/blob/main/python_django/projects/django_educenter/demo_pictures/Demo%203%20-%20Course%20List.png>
   [Blog List]: <https://github.com/DylanBergmann2502/Web-Development/blob/main/python_django/projects/django_educenter/demo_pictures/Demo%205%20-%20Blog%20List.png>
   [Event List]: <https://github.com/DylanBergmann2502/Web-Development/blob/main/python_django/projects/django_educenter/demo_pictures/Demo%207%20-%20Event%20List.png>
   [Teacher List]: <https://github.com/DylanBergmann2502/Web-Development/blob/main/python_django/projects/django_educenter/demo_pictures/Demo%209%20-%20Teacher%20List.png>
   [Login]: <https://github.com/DylanBergmann2502/Web-Development/blob/main/python_django/projects/django_educenter/demo_pictures/Demo%2013%20-%20Login.png>
   [Unit and Integration Tests]: <https://github.com/DylanBergmann2502/Web-Development/blob/main/python_django/projects/django_educenter/demo_pictures/unit%2C%20integration%20testing.jpg>
   [Python]: <https://www.python.org/downloads/>
   [Redis]: <https://redis.io/download/>
 