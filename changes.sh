pkill -f python
git pull origin master
nohup python pubsub.py &


nohup python app/manage.py runserver 8000 &


