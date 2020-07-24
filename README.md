# Quora-Clone
A quora type application where you can ask questions and add answers, upvote and downvote them.

# Setup
```
pip install -r requirements.txt
```

# Database
```
python manage.py makemigrations
python manage.py migrate
```
If want to run admin 
```
python manage.py createsuperuser
```

## Run django
```
python manage.py runserver
```

# Adding initial data
After setting up database, you might wanna add some initial data like creating users, asking questions, adding answers, etc..

# How to Use
Goto 127.0.0.1:8000. Now login or signup.
If you are already logged in, it will ask you to view feed.
Feed is designed in such a way that you only see answers from the people who you are following.
So first time login will ask you to follow people.
You can visit their profiles , view whom they are following and who are following them.
In feed you can check full question, where you can see all answers to that particular question and their upvoters and downvoters.
You can also see all users present in quora-clone

# Future Scope
I will be adding forms to ask questions and add answers.
And also the functionality to add comments.
And finally improving the UI.
