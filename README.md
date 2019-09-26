# Morbido API

per installare:
```bash
pyvenv venv

source venv/bin/activate

pip3 install --trusted-host pypi.python.org -r requirements.txt
```

per spegnere il virtual env:
```bash
deactivate venv/bin/activate
```
PS: il virual env in generale si puo chiamare come si vuole, quindi in caso di nome diverso bisogna aggiungere il nome della cartella nel .gitignore

per usare flask:
```bash
python3 app.py
```
per aggiornare le dipendenze:
```bash
pip3 freeze > requirements.txt
```

per eseguire i test:
```bash
python3 -m unittest discover test/
```