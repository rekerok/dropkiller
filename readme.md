```bash
docker build -t my_flask_app:0.1 .
docker run -p 8080:8080 --name my-running-app my_flask_app
```