# This file is part of FreePC.
# 
# FreePC is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# FreePC is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with FreePC.  If not, see <http://www.gnu.org/licenses/>.

## @package models
#  Documentation for the package models

from django.db import models
from django.contrib.auth.models import User, Group
from bootstrap_themes import list_themes

from django.core.exceptions import ValidationError
from dateutil import tz

# Create your models here.

## Model Class for the design of Building
class Building(models.Model):
	## The name of the building
	name = models.CharField(max_length=64)

	## toString method
	#  @param self The object pointer
	def __unicode__(self):
		return self.name

## Model Class for the design of Room
class Room(models.Model):
	## The Building
	building = models.ForeignKey(Building)
	## The name of the room
	name = models.CharField(max_length=5, primary_key=True)

	## toString method
	#  @param self The object pointer
	def __unicode__(self):
		return self.name

## Model Class for the design of RestrictionDay
class RestrictionDay(models.Model):
	## The name of the restriction
	name = models.CharField(max_length=32)
	monday = models.BooleanField() #monday if monday is restricted
	tuesday = models.BooleanField() # tuesday if tuesday is restricted
	wednesday = models.BooleanField()  #wednesday if wednesday is restricted
	thursday = models.BooleanField()  #thursday if thursday is restricted
	friday = models.BooleanField()  #friday if friday is restricted
	saturday = models.BooleanField()  #saturday if saturday is restricted
	sunday = models.BooleanField()  #sunday if sunday is restricted

	## toString method
	#  @param self The object pointer
	def __unicode__(self):
		return self.name

## Model Class for the design of RestrictionTime
class RestrictionTime(models.Model):
	## The RestrictionDay
	days = models.ForeignKey(RestrictionDay)
	## Starting time
	start = models.TimeField()
	## Ending time
	end = models.TimeField()

	## toString method
	#  @param self The object pointer
	def __unicode__(self):
		return "%s - %s" % (str(self.start),str(self.end)) 

## Model Class for the design of ConnectionType
class ConnectionType(models.Model):
	## The name of the ConnectionType
	name = models.CharField(max_length=64, primary_key=True)
	## The priority
	priority = models.PositiveSmallIntegerField()

	## toString method
	#  @param self The object pointer
	def __unicode__(self):
		return self.name

## Model Class for the design of Workstation
class Workstation(models.Model):
	## The available status
	STATUS = (
		('online', 'Online'),
		('offline', 'Offline'),
		('updating', 'Updating')
		)
	## the choosen RestrictionTime
	restriction_time = models.ForeignKey(RestrictionTime)
	## the IP address
	ip = models.IPAddressField(null=False)
	## the hostname
	hostname = models.CharField(max_length=64, null=False, primary_key=True)
	## the certificate
	certificate = models.TextField(null=True, blank=True) 
	## the status
	status = models.CharField(max_length=16, choices=STATUS)
	## the last check of the workstation
	last_update = models.DateTimeField(null=True, blank=True)
	## the maximum ssh users during restriction time
	max_users_ssh = models.PositiveSmallIntegerField()
	## the maximum ssh users during unrestriction time
	max_users_ssh_unrestricted = models.PositiveSmallIntegerField(null=True, blank=True)
	## the maximum x2go users during restriction time
	max_users_x2go = models.PositiveSmallIntegerField()
	## the maximum x2go users during unrestriction time
	max_users_x2go_unrestricted = models.PositiveSmallIntegerField(null=True, blank=True)
	## the maximum connection hours during restriction time
	max_hours_connection = models.PositiveSmallIntegerField()
	## the time you have to wait before reconnection (in hour)
	waiting_time_before_reconnect = models.PositiveSmallIntegerField()
	## the time where you can reconnect after a deconnection (in minute)
	interval_time_not_disconnection = models.PositiveSmallIntegerField()
	## the minimum percentage of CPU ressources allowed to the console users
	min_CPU_console_user = models.PositiveSmallIntegerField(null=True, blank=True)
	## the maximum percentage of CPU ressources allowed to the non console users
	max_CPU_each_non_console_user = models.PositiveSmallIntegerField(null=True, blank=True)
	## the minimum percentage of RAM ressources allowed to the console users
	min_RAM_console_user = models.PositiveIntegerField(null=True, blank=True)
	## the maximum percentage of RAM ressources allowed to the non console users
	max_RAM_each_non_console_user = models.PositiveIntegerField(null=True, blank=True)
	## the allowed connection type for the workstation
	connection_type = models.ManyToManyField(ConnectionType, through='WorkstationConnectionType')
	## the owner of the workstation
	owner = models.ForeignKey('auth.User', related_name='workstations', null=True, blank=True)
	## the Room where is the workstation
	room = models.ForeignKey(Room, null=True, blank=True)

	## toString method
	#  @param self The object pointer
	def __unicode__(self):
		return "%s - %s" % (self.hostname, str(self.ip))

## Model Class for the design of RestrictionLogin
class RestrictionLogin(models.Model):
	## the restriction
	restriction = models.CharField(max_length=64)

	## toString method
	#  @param self The object pointer
	def __unicode__(self):
		return self.restriction

## Model Class for the design of GroupSystem
class GroupSystem(Group):
	## the priority of the Group
	priority = models.PositiveSmallIntegerField()
	## the RestrictionLogin
	restrictions = models.ManyToManyField(RestrictionLogin, through='GroupRestriction')

## Model Class for the design of UserSystem
class UserSystem(models.Model):
	## the username
	username = models.CharField(max_length=64, primary_key=True)
	## the GroupSystem appartenance of the user
	group_system = models.ForeignKey(GroupSystem, null=True, blank=True)

	## toString method
	#  @param self The object pointer
	def __unicode__(self):
		return self.username

## Model Class related to the binding of Group and Restriction
class GroupRestriction(models.Model):
	## the GroupSystem
	group = models.ForeignKey(GroupSystem)
	## the RestrictionLogin
	restriction = models.ForeignKey(RestrictionLogin)

## Model Class for the design of WorkstationConnectionType
class WorkstationConnectionType(models.Model):
	## the Workstation
	workstation = models.ForeignKey(Workstation)
	## the ConnectionType
	connection_type = models.ForeignKey(ConnectionType)

	## toString method
	#  @param self The object pointer
	def __unicode__(self):
		return "%s - %s" % (self.workstation, self.connection_type)
	
## Model Class for the design of WorkstationUser
class WorkstationUser(models.Model):
	## the WorkstationConnectionType
	workstation_type = models.ForeignKey(WorkstationConnectionType)
	## the connected UserSystem
	user = models.ForeignKey(UserSystem)
	## logname file
	logname = models.CharField(max_length=128, null=True, blank=True)
	## the user is logged
	logged = models.BooleanField(default=False)
	## the starting time of the connection
	connection_start = models.DateTimeField()
	## the ending time of the connection
	connection_end = models.DateTimeField(null=True, blank=True)
	## the link of booked reservation
	reservation_link = models.URLField(null=True, blank=True)

	## toString method
	#  @param self The object pointer
	def __unicode__(self):
		return "%s - %s" % (self.workstation_type, self.user)

