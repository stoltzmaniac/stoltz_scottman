# stoltz_scottman

```
docker build -t flask-heroku:latest .

docker run -d -p 5000:5000 flask-heroku

docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker system prune -a
```