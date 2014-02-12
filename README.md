Django Deployment
=================

Dead simple deployment for your django apps.

#### Config

```python
config = {
    "hosts": ["@example.org"],
    "user": "root",
    "password": "root_password",

    "gunicorn_workers": 4,
    "gunicorn_port": 9001,

    "postgres_user": "testuser",
    "postgres_password": "testpassword",
    
    "server_port": 80,
    "server_name": "example.org www.example.org",
}
```


#### Deploy

Django deployment has never been so easy!

```bash
python deploy.py --dir=testproject
```

#### Provision and deploy

Provision your server and resolve the dependencies automatically. Then deploy!

```bash
python deploy.py --dir=testproject --full=True
```
