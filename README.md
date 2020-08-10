# stoltz_scottman


Build your app
```
docker build -t flask-heroku:latest .
```

Run your app
```
docker run -d -p 5000:5000 flask-heroku
```

Use Heroku (only need to login once if you save credentials)

Only use the following if you have a command line interface setup (requires homebrew)
```
heroku container:login

heroku create yourawesomeapp

heroku container:push web --app yourawesomeapp

heroku container:release web --app yourawesomeapp
```

Remove stop, remove, and wipe all Docker stuff from your machine. Note: This will clear everything and not just Docker images from the current directory.
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker system prune -a
```