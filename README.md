# Публикация комиксов в группе Вконтакте

Сервис для скачивания комиксов с сайта [xkcd.com](https://xkcd.com/) и публикации их в группе Вконтакте.

### Как установить

 - Для использования скрипта необходимо:
    - зарегистрироваться на сайте [Вконтакте](https://vk.com/)
    - создать группу в разделе [Управление группами](https://vk.com/groups?tab=admin)
    - создать приложение в разделе [Мои приложения](https://vk.com/dev) на странице для разработчиков (тип приложения - standalone)
    - сохранить client_id приложения (если нажать на кнопку “Редактировать” для нового приложения, в    адресной  строке вы увидите его client_id)
    - получить токен по [инструкции](https://vk.com/dev/implicit_flow_user), вам потребуются следующие права:  photos, groups, wall и offline
    
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
