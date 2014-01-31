Django Deployment
=================

Dead simple deployment for your django apps.

#### Config

```python
config = {
    "hosts": ["root@example.org"],
    "password": "root_password",

    "gunicorn_workers": 4,
    "gunicorn_port": 9001,

    "postgres_user": "bootstrap",
    "postgres_password": "Bootstrap999",
}
```


#### Deploy

Django deployment have never been so easy!

```bash
python deploy.py [app_dir] [remote_app_dir]
```

#### Provision and deploy

Provision your server and resolve the dependencies automatically. Then deploy!

```bash
python deploy.py [app_dir] [remote_app_dir] --full=True
```
