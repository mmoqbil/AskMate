source venv/bin/activate
app_name=server.py
app=$(pwd)/$app_name

export FLASK_APP=$app
export FLASK_ENV=development
flask run
