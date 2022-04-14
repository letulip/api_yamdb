# api_yamdb
api_yamdb

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd 
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver

создаем приложение API и reviews с помощью команды:

python3 manage.py startapp [name app]

Чтобы Django-проект узнал о том, что в нем есть приложение, нужно это приложение зарегистрировать: добавить его конфиг в список установленных приложений INSTALLED_APPS в файле settings.py
Зарегистрировать приложение можно и иным способом: можно добавить в INSTALLED_APPS не конфиг, а имя приложения, [name app]. Но практичнее регистрировать через конфиг: ведь тогда в apps.py можно будет в любой момент добавить дополнительные настройки приложения. При регистрации через имя такой возможности не будет.

models.py создаем в приложении reviews

файлы serializer.py и permissions.py в приложении api
