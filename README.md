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

If you are using Heroku from the web interface. You'll simply connect it to your GitHub repository. You need to create `heroku.yml` in this case.

`heroku.yml` should be:

```
build:
  docker:
    web: Dockerfile
```



Steps: 

  - In the top left, "Create New App"
  - Give your app a name
  - Create App
  - Deployment Method: choose "GitHub"
  - Connect the appropriate repository
  - Decide on whether or not you want it to automatically deploy
  - Can choose a specific branch to deploy


Remove stop, remove, and wipe all Docker stuff from your machine. Note: This will clear everything and not just Docker images from the current directory.
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker system prune -a
```