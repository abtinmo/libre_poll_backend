<h1 align="center">
  LibrePoll Backend API 📊
</h1>
<p align="center">
  <strong>
    LibrePoll Is A Tools For Creating And Sharing Polls, Free & OpenSource.
  </strong>
<p align="center">
  For React.js client side see: <a href="https://github.com/shervinmo/libre_poll_fronend">LibrePoll React</a>
</p>
<!-- <p align="center">
  <a href="https://example.org">
   Domain
  </a>
</p> -->

<p align="center">
  <a href="https://github.com/shervinmo/libre_poll_backend/commits/master">
    <img src="https://img.shields.io/github/last-commit/shervinmo/libre_poll_backend.svg" alt="Latest Commits" />
  </a>
  <a href="https://travis-ci.com/shervinmo/libre_poll_backend">
    <img src="https://api.travis-ci.com/shervinmo/libre_poll_backend.svg?branch=master" alt="Current build status." />
  </a>
    <!-- <img src="https://cdn.jsdelivr.net/gh/shervinmo/libre_poll_backend@master/coverage/badge-lines.svg" alt="Current test covarage status." /> -->
  <a href="https://github.com/shervinmo/libre_poll_backend/#contributing">
    <img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg" alt="Contributions" />
  </a>
  <a href="https://github.com/shervinmo/libre_poll_backend/blob/develop/LICENSE">
    <img src="https://img.shields.io/github/license/shervinmo/libre_poll_backend.svg" alt="License" />
  </a>
  <!-- <a href="https://twitter.com/shervinmo">
    <img src="https://img.shields.io/twitter/follow/shervinmo.svg?label=Follow&style=social?style=plastic" alt="Twitter" />
  </a> -->
</p>



## Table of Contents
* [Key Features](#key-features)
* [Stack](#stack)
* [Development Setup](#setup)
* [Contributing](#contributing)

## Key Features
sanic
postgresql

## Stack
* item No.1
* item No.2

## Setup
install requirements with pip
```
pip install -r requirements.txt
```
you need to install postgresql , if not familiar follow this :

[postgresql ubuntu 18.4](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04)

edit db/config.py and update secret_key and database config.
```
secrect_key = "YOUR_KEY"
db_config = 'user=YOUR_USER  password=YOUR_PASSWORD host=YOUR_HOST dbname=YOUR_DATABASE_NAME'
```

next run this command to create tables in database
```
 psql YOUR_DATABSE_NAME < Database.sql
```
finally
```
python3 server.py
```

## Contributing
Pull requests are welcome. You'll probably find lots of improvements to be made.

Open issues for feedback, requesting features, reporting bugs or discussing ideas.
