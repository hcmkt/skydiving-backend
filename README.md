# skydiving-backend
Backend for [Skydiving LINE BOT](https://github.com/hcmkt/skydiving)

## Development
Copy `.env`
```
cp .env.example .env
```
Install packages
```
pipenv install -d
```
Upgrade database
```
pipenv run flask db upgrade
```
Start dev server
```
pipenv run flask run
```

### HTTP request
Get settings
```
task get
```
Update settings
```
task put -- <number>
```

## Rich menu
Set rich menu. It requires `LIFF_URL` in `.env`
```
python3 richmenu.py
```
