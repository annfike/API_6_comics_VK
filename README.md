# Публикация комиксов в группе Вконтакте

Сервис для скачивания комиксов с сайта [xkcd.com](https://xkcd.com/) и публикации их в группе Вконтакте.

### Как установить

 - Для использования скрипта необходимо зарегистрироваться на сайте [Вконтакте](https://vk.com/), создать    группу, приложение и получить токен и id групппы.
 - Полученный токен и id присвоить переменным окружения в файле ".env":
```python
   VK_TOKEN=ВашТокен
   
   GROUP_ID=Ваш ID группы

```
 - Python3 должен быть уже установлен.
 - Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```python
   pip install -r requirements.txt
   ```
 - Для запуска скрипта используйте команду:
```python
   python main.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
