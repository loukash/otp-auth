# OTP-AUTH #

Простое приложение, которое позволяет совместно с nginx реализовать авторизацию по одноразовому паролю.


* Установить nginx >= 1.5.4 с поддержкой с модуля ngx_http_auth_request_module
Проверить можно командой
```
nginx -V 2>&1 | grep -qF -- --with-http_auth_request_module && echo "OK" || echo "FAIL"
```
В Ubuntu/Debian:
```
sudo aptitude update && sudo aptitude install nginx-extras
```

* Клонировать репозитарий
```
git clone git@github.com:loukash/otp-auth.git
```

* Установить все зависимости для python2.7
```
pip install -r requirements.txt
```

* Создать базу данных
```
python manage.py initdb
```

* Добавить пользователя
```
python manage.py useradd -l test
```

* Добавить в Google Authentificator, или другой OTP генератор,  новый аккаунт на основе данных, полученных на предыдущем шаге ([Справка от Google](https://support.google.com/accounts/answer/1066447?hl=ru) ).

* Запустить ОТП-прокси
```
python manage.py runserver
```

* Изменить конфиг nginx
```
# Защищаемый location
location /admin {
  auth_request /auth;
  error_page 401 /login;
  root /var/www/html;
}

# Служебные locations
location = /auth {
  internal;
  proxy_pass_request_body off;
  proxy_set_header Content-Length "";
  proxy_pass http://127.0.0.1:5000;
}

location = /login {
  proxy_pass http://127.0.0.1:5000;
}
```

* Рестартовать nginx
```
sudo service nginx reload
```

Теперь при открытии защищённого урла http://site.name/admin вы должны увидеть такую форму

![login.png](https://bitbucket.org/repo/Lzk76e/images/3920401730-login.png)

###
Управление базой пользователей

python manage.py (initdb|useradd|userdel|userlist|renew)


| Назначение            | Команда |
| --------------------- | ------------- |
| Создать базу | initdb |
| Добавить пользователя | python manage.py useradd -l test |
| Удалить пользователя  |python manage.py userdel -l test |
| Список пользователей  | python manage.py userlist |
| Генерация новых резервных кодов | python manage.py renew -l test -с 5|

Если ключи не указаны явно, то они будут запрошены.

### Использование reCaptcha

* Получить Ключ и Секретный ключ
https://www.google.com/recaptcha/admin

* Прописать их в config.py и разрешить reCAPTCHA опцией RECAPTCHA_ENABLED = True
