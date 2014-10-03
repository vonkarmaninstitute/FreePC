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

## @package utils

from restriction_system.models import *
from datetime import datetime, timedelta
from django.utils import timezone
from dateutil import tz
import time

## Method giving a queryset of all the buidings
#
#  @return QuerySet of Building
def get_buildings():
        return Building.objects.all().order_by('name')

## Method giving a queryset of all rooms present in the building
#
#  @param b a Building
#  @return QuerySet of Room
def get_rooms_from(b):
        return Room.objects.filter(building=b).order_by('name')

## Method giving a queryset of all the workstations prensent in the room
#
#  @param r a Room
#  @return QuerySet of Workstation
def get_workstations_from(r):
	"""
	"""
        return Workstation.objects.filter(room=r).order_by('hostname')

## Method verifying if we are in restricted time
#
#  @param w a workstation
#  @param time a time
#  @return True if restricted otherwise False
def is_restricted(w, time):
	ti_zone = tz.tzlocal()
	time = time.replace(tzinfo=ti_zone)

	day = time.isoweekday()
	hour = time.time()
	
	# restriction_on_days == False mean no restriction for the day
	restriction_on_days = False

	rt = RestrictionTime.objects.get(id=w.restriction_time_id)
	rd = RestrictionDay.objects.get(id=rt.days_id)

	if day == 1:
		if rd.monday:
			restriction_on_days = True
	elif day == 2:
		if rd.tuesday:
			restriction_on_days = True
	elif day == 3:
		if rd.wednesday:
			restriction_on_days = True
	elif day == 4:
		if rd.thursday:
			restriction_on_days = True
	elif day == 5:
		if rd.friday:
			restriction_on_days = True
	elif day == 6:
		if rd.saterday:
			restriction_on_days = True
	elif day == 7:
		if rd.sunday:
			restriction_on_days = True

	if restriction_on_days:
		return ((rt.start <= hour) and (hour < rt.end))
	else:
		return False

## Method verifying if a user can connect on a workstation
#
#  @param w a Workstation
#  @param wu a WorkstationUser
#  @param user a UserSystem
#  @param time a time
#  @return True if can reconnect
def can_reconnect(w, wu, user, time):
	print "dans can_reconnect"
	ti_zone = tz.tzlocal()
	time = time.replace(tzinfo=ti_zone)
	time_start = wu.connection_start
	time_end = wu.connection_end

	total_connection_day = timedelta()
	other_connection_today = False
	#wuall = WorkstationUser.objects.filter(workstation_type_id=wu.workstation_type_id).filter(username=user.username).filter(connection_start__startswith=time).exclude(logged=True)
	#print "avant calcul total connection"
	#for wua in wuall:
	#	other_connection_today = True
	#	diff = wua.connection_end - wua.connection_start
	#	total_connection += diff

	if time_end == None:
		return None
	diff_time = time - time_end
	#print "avant other_connection_today"
	#if other_connection_today:
	#	max_hours = timedelta(hours=w.max_hours_connection)
	#	if total_connection < max_hours:
	#		return True
	timedelta_interval = timedelta(minutes=w.interval_time_not_disconnection)
	if diff_time < timedelta_interval:
		return None

	timedelta_interval = timedelta(hours=w.waiting_time_before_reconnect)
	if diff_time >= timedelta_interval:
		return None

	return diff_time

## Method giving the number of limit_connection of a workstation for a connection type.
#
#  @param workstation a Worstation
#  @param connection_type a ConnectionType
#  @param number_connection an Integer
#  @param restricted is_restricted
def vki_limit_connection(workstation, connection_type, number_connection, restricted=True):
	limit_of_connection = 0
	if connection_type.name == "console":
		limit_of_connection = 1
	elif connection_type.name == "ssh":
		if restricted:
			limit_of_connection = workstation.max_users_ssh
		else:
			limit_of_connection = workstation.max_users_ssh_unrestricted
	else:
		if restricted:
			limit_of_connection = workstation.max_users_x2go
		else:
			limit_of_connection = workstation.max_users_x2go_unrestricted
	if limit_of_connection == None:
		limit_of_connection = 10
	return number_connection < limit_of_connection
## Method giving a restriction time based on a string
#
#  @param str_time an interval of hours (hh:mm - hh:mm)
#  @return RestrictionTime Object
def get_restriction_time(str_time):
# time received in this format "hh:mm - hh:mm"
	split_time = str_time.split(' ')
	s_start = split_time[0]
	s_end = split_time[-1]

	try:
		time_start = datetime.strptime(s_start, "%H:%M").time()
		time_end = datetime.strptime(s_end, "%H:%M").time()

		print time_start
		print time_end
		rt = RestrictionTime.objects.filter(start=time_start, end=time_end).first()
		return rt
	except:
		return None
