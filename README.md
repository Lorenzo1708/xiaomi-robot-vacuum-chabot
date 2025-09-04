```
py -m venv .venv
py -m pip install --upgrade pip
py -m pip install -r ./requirements.txt
```

```
py ./scripts/create_index.py
py ./scripts/test_index.py
```

```
docker build -t chatbot .
docker run --env-file ./.env --name chatbot --publish 7860:7860 --rm chatbot
```
