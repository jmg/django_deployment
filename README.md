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

    "postgres_user": "testuser",
    "postgres_password": "testpassword",
}
```


#### Deploy

Django deployment have never been so easy!

```bash
python deploy.py --name=testproject --dir=testproject --remote_dir=testproject_remote_dir
```

#### Provision and deploy

Provision your server and resolve the dependencies automatically. Then deploy!

```bash
python deploy.py --name=testproject --dir=testproject --remote_dir=testproject_remote_dir --full=True
```
