# geranos

## Installation

## Install geranos
```
  $ sudo apt install python-dev libffi-dev
  $ cd /srv
  $ git clone http://github.com/saxtouri/geranos.git
  $ cd geranos.git
  $ python setup.py install
```

### Configuration files

Create two yaml files: **nodes.yaml** and **credentials.yaml**
Make sure to edit them before running anything, otherwise geranos will
fail.

Edit `nodes.yaml` to add some docker enables hosts.
Edut `credentials.yaml` to set the x-api-key which will be used by clients to connect to geranos API.

### Create an SSH key

Geranos uses PPK to connect to the docker enabled hosts.

If you don't have a pair, create one e.g.,
```$ ssh-keygen -t rsa -b 4096 -C "user@example.com"```
This will create a pair of private and public keys at `~/.ssh/id_rsa` and `~/.ssh/id_rsa.pub` respectively.

Append the public key to `/root/.ssh/authorized_keys` on each of your target hosts.

Set the full path of the private key in your `nodes.yaml` file by editing this line:
```rsa_key: /path/to/public/key```

## Test run
This is for debuging. Make sure you have a copy of `nodes.yaml` and `credentials.yaml` at the working directory. Then:

```
  $ python /srv/geranos/geranos/api.py
```

Your server should run on 8080, if that's allowed.

## Deploy with Apache2 and GUnicorn
Install apache2 and gunicorn if you haven't already
```
$ apt install gunicorn apache2
```
Configure geranos
```
$ mkdir /etc/geranos
$ cp nodes.yaml /etc/geranos/.
$ cp credentials.yaml /etc/geranos/.
```

### Setup gunicorn
```
$ mkdir /etc/gunicorn.d
$ mkdir /var/log/gunicorn
```
Create the file `/etc/gunicorn.d/geranos`
```
CONFIG = {
  'mode': 'wsgi',
  'working_dir': '/srv/geranos',
  'python': '/usr/bin/python',
  'user': 'root',
  'group': 'www-data',
  'args': (
     '--bind=127.0.0.1:8000',
     '--bind=[::1]:8000',
     '--workers=3',
     '--timeout=52000',
     '--log-level=INFO',
     '--log-file=/var/log/gunicorn/geranos.log',
     'geranos.api:app'
  ),
}
```

### Setup Apache2
Make sure reverse proxy is enabled in apache
```
$ a2enmod proxy proxy_http
```

Add these lines to your active vhosts-ssl.conf file at `/etc/apache2/sites-enabled`, inside the `VirtualHost` tags. Or if it is not named vhosts-ssl.conf, use the one you have.

```
<VirtualHost *:443>
  ...
  ProxyPass        /geranos http://127.0.0.1:8000
  ProxyPassReverse /geranos http://127.0.0.1:8000
  ...
</VirtualHost>
```

It is advised to run this behind an SSL reverse proxy, but if you don't have an SSL proxy, just put it in the Virtual Host you desire.

### Run the bloody thing
```
$ service restart gunicorn
$ service restart apache2
```
to test if it works do this with curl (or with a browser)
```
$ curl https://example.org/geranos/all/docker/logs
  {"message": "Access forbidden"}
```
If you get any other result, problem...

## Use geranos

Read the logs from container "hello-world" from all nodes
```
$ curl -H'X-API-KEY: thesecretfromcredentialsyaml' \
    https://example.org/geranos/all/docker/logs?container=hello-world
```

Pull the 'super/heavy:1.0.1' image to all overweight hosts
```
$ curl -H'X-API-KEY: thesecretfromcredentialsyaml' -XPOST \
    https://example.org/geranos/all/docker/logs?image=super%2Fheavy:1.0.1
```
