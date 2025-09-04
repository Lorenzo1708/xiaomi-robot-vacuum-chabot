```
py -m venv .venv
py -m pip install -r ./requirements.txt
```

```
docker build -t chatbot .
docker run --env-file ./.env --name chatbot --publish 7860:7860 --rm chatbot
```
