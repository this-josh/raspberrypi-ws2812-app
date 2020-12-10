echo activating env
source lights_app/bin/activate
echo starting server
waitress-serve --port=8080 app:application