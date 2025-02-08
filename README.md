After cloning the repossitory cd into that folder and follow the steps below:
(should have python installed in the computer
1. create virtual environment by running "virtualenv .venv"
2. .venv\scripts\activate
3. pip install django djangorestframework djangorestframework-simplejwt django-cors-headers django-filters
4. python manage.py makemigrations
5. python manage.py migrate
6. python manage.py createsuperuser   (and create the admin user to use admin panel)
7. python manage.py runserver
8. Login to admin panel by using localhost:8000/admin
9. create some dummy data

End points details:
1. /api/token/refresh/   ( to get a new access token by providing the refresh token )
2. /api/login    ( login user with email and password )
3. /api/signup    ( signup user with email, name and password )
4. /api/change-pass/  ( to change the password user needs to logged in and also provide old password using fields old_password, new_password )
5. /api/posts/   ( authenticated users can view and search posts, create posts, update and delete theri posts )
6. /api/comments/ ( same as above )
   More details for posts and comments apis
   to get posts   /api/posts/?id=''   or /api/posts/?search=''    (here id is te post id and search is any keyword to search the post)
   to create posts /api/posts
   to update /api/posts/?id    (post id)
   to delete /api/posts/?id ( post id)
   to get comments api/comments/?id   (id = post id)
   to create comment api/comments/     ( post id should be given in body named post )
   to update and delete comment /api/comment/?id=''

User Table
username: CharField
email: EmailField (primary)
password: CharField
date_joined: DateTimeField

Post Table
id: Integer (Primary Key)
title: CharField
content: TextField
author: ForeignKey (User)
created_at: DateTimeField
updated_at: DateTimeField

Comment Table
id: Integer (Primary Key)
text: TextField
author: ForeignKey (User)
post: ForeignKey (Post)
created_at: DateTimeField
