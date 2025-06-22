## Test The Speed Between `pip venv` and `uv venv`

1. Write a script that:
   - Installs dependencies and runs the Django server
   - Uses the `time` module to see the speed differences


```
cd testvenv/pipvenv && source venv/bin/activate
   && python manage.py runserver
```



```
source venv/bin/activate && django-admin
      startproject sampleproject .
```

```
uv run django-admin startproject sampleproject   │
│    .
```