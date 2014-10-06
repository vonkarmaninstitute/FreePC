#FreePC
Login restriction management system.

##Why FreePC?
In our computer labs, we needed a system that controle the access of the users on the different linux public machines. For example, a user cannot log on more than 1 computer at a time. Or he cannot connect log on the same computer 2 days in a row.
First, we looked for [availability map][am] but it did not fit our needs. So we decided to develop our own solution.

##What is FreePC?
FreePC is an open-source software. The server part is developed in Django and support the [REST framework][rest] and the client side is in bash. We are also using the pam.d to send the right information to the server.
The presentation part is not use because we are using [Zabbix][zx] which was already installed.

##Requirements
FreePC will only work on operating system using [systemd][].
###To use FreePC, you need to install:
  - python (2.7)
  - python-dateutil
  - django (>=1.6.5)
  - a web server (apache, lighttp, nginx)

###Install using pip:
  - [djangorestframework][rest]
  - markdown
  - django-filter
  - PyYAML
  - django-bootstrap3
  - django-bootstrap-themes
  - django-rest-swagger

##Download
You can download the zip version [here][dl].

##License
Code is under [GNU GPL version 3][license].

##Authors
  - Raimondo Giammanco
  - Laurent Spitaels

[license]:https://github.com/vonkarmaninstitute/FreePC/blob/master/LICENSE
[dl]:https://github.com/vonkarmaninstitute/FreePC/archive/master.zip
[rest]:http://www.django-rest-framework.org/
[zx]:http://www.zabbix.com/
[am]:http://journal.code4lib.org/articles/4067
[systemd]:http://en.wikipedia.org/wiki/Systemd
