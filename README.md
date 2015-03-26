#FreePC
####The client side script will arrive soon.
Login restriction management system.

##Why FreePC?
In our institution the vast majority of computational resources (workstations, desktops, clusters) are running under GNU/Linux. 
Researchers have normally a dedicated workstation where only selected people can log without any restrictions. Students generally need to use the public linux machines. 

These machines use NFS mounted filesystems for their homes, scratch space, programs, etc. etc. 

While precise guidelines exist for the use of these public machines, students have repeteadly violated them, consciously or not.

The most damaging behaviour is to leave a session locked in one workstation and logging in another one the day after or the same day to harness more resources.

Another detrimental behaviour is to select a machine and start camping there, leaving around personal belongings that have no place in a public room.

Finally,

In our computer labs, we needed a system that control and rationalize the access of the users on the different linux public machines. 

For example, a user cannot log on more than 1 computer at a time. 

Or he cannot connect log on the same computer 2 days in a row.

First, we looked for [availability map][am] but it did not fit our needs. So we decided to develop our own solution.

##What is FreePC?
FreePC is an open-source software. 

The server part is developed in Django and support the [REST framework][rest] and the client side is leveraging customized [PAM][pam] modules. 

The presentation part is currently not use because we are using [Zabbix][zx] which was already installed, but will be completed soon.

##Requirements
FreePC will only work on operating system using [systemd][], currently deployed and tested on Fedora 20 machines, will be update to a new Fedora release when we will migrate our machines (possibly skipping 21 and jumping straight to 22).

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
[pam]:http://en.wikipedia.org/wiki/Pluggable_authentication_module
