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

## @package views
#  Documentation of the package views

from django.utils import timezone
from dateutil import tz
import time
from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime, timedelta

from restriction_system.models import *
from restriction_system.utils import *
from restriction_system.serializers import *

from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route

from rest_framework.permissions import IsAuthenticated

from restriction_system.permissions import *

import subprocess

## View rendering the home page
def home(request):
	return render(request, 'index.html',{
		'buildings':get_buildings(),
		})
## View rendering the about page
def about(request):
	return render(request, 'about.html',{
		'buildings':get_buildings(),
		})

## View rendering the availability map
def availability(request, room):
	return render(request, 'room.html', {
		'room':room,
		'buildings':get_buildings(),
		})

## Method toeck if the workstations are still online,
#  if not, it disconnect the users connected on the workstations 
@api_view(['POST',])
def check_workstation(request, format=None):
	if request.method == 'POST':
		the_30min = timedelta(minutes=30)
		now = datetime.today()
		all_ws = Workstation.objects.all()
		cpt_ws = 0
		cpt_users = 0
		for ws in all_ws:
			interval_30min = now - ws.last_update
			if interval_30min > the_30min:
				cpt_ws += 1
				ws.status = "offline"
				all_wc = WorkstationConnectionType.objects.filter(workstation_id=ws.hostname)
				for wc in all_wc:
					all_wu = WorkstationUser.objects.filter(workstation_type_id=wc.id)
					for wu in all_wu:
						cpt_users += 1
						wu.connection_end = now
						wu.logged = False
						wu.save()
		msg = "%d workstations offline and %d users have been disconnected of the database." % (cpt_ws, cpt_users)
		data = {"code": 0, "content": msg}
		return Response(data, status=status.HTTP_200_OK)
	pass

## Method to update the last_update value of a workstation 
@api_view(['POST',])
def last_update(request, format=None):
	if request.method == 'POST':
		now = datetime.today()
		host = request.DATA['hostname']
		ws = Workstation.objects.get(hostname=host)
		ws.last_update = now
		ws.status = "online"
		ws.save()
		format_time = "%d %b %Y - %H:%M"
		time = now.strftime(format_time)
		msg = "Last update of %s : %s" % (host, time)
		data = {"code": 0, "content": msg}
		return Response(data, status=status.HTTP_200_OK)
	pass

## Method to clean the workstation_user all workstation_users older than 72h
@api_view(['POST',])
def clean_workstation_users(request, format=None):

	if request.method == 'POST':
		cpt = 0 
		now = datetime.today()
		wuc = WorkstationUser.objects.filter(logged=True)
		for wu in wuc:
			if not wu.logged:
				if wu.connection_end:
					time = now - wu.connection_end
					if time.total_seconds() > (3600 * 72):
						wu.delete()
						cpt += 1
				else:
					time = now - wu.connection_start
					if time.total_seconds() > (3600 * 72):
						wu.delete()
						cpt += 1

		msg = "%d workstation_user have been removed from the database." % (cpt)
		print msg 
		data = {"code": 0, "content": msg}
		return Response(data, status=status.HTTP_200_OK)


## Method verifying the users are still connected
@api_view(['POST',])
#@permission_classes((IsAuthenticated,))
def verification_connection(request, format=None):
	if request.method == 'POST':
		now = datetime.today()
		hostname = request.DATA['hostname']
		users = request.DATA['users']
		wcall = WorkstationConnectionType.objects.filter(workstation_id=hostname)
		wuc = WorkstationUser.objects.filter(logged=True).filter(workstation_type_id__in=wcall)
		for wu in wuc:
			if wu.user.username not in users:
				wu.logged = False
				wu.connection_end = now
				wu.save()

		ws = Workstation.objects.get(hostname=request.DATA['hostname'])
		ws.status = "online"
		ws.last_update = now
		ws.save()
		data = {"code": 0, "content": "Done"}
		return Response(data)

## Method to create or update a workstation
@api_view(['POST','GET',])
#@permission_classes((IsAuthenticated,))
def create_update_workstation(request, format=None):
	if request.method == 'POST':
		json_w = request.DATA
		rt = get_restriction_time(json_w['restriction_time'])
		if rt == None:
			msg = "Restriction time does not exist : " + json_w['restriction_time']
			data = {"code": 11, "content": msg}
			return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)

		workstation, created = Workstation.objects.get_or_create(hostname=json_w['hostname'],
					defaults={'restriction_time':rt,
						'ip':json_w['ip'],
						'certificate':json_w['certificate'],
						'status': 'online',
						'max_users_ssh':json_w['max_users_ssh'],
						'max_users_x2go':json_w['max_users_x2go'],
						'max_hours_connection':json_w['max_hours_connection'],
						'waiting_time_before_reconnect':json_w['waiting_time_before_reconnect'],
						'interval_time_not_disconnection':json_w['interval_time_not_disconnection'],
						'room':json_w['room']
						}
					)
		# create workstation type
		if created:
			try:
				workstation.max_users_ssh_unrestricted = json_w['max_users_ssh_unrestricted']
			except:
				pass
			try:
				workstation.max_users_x2go_unrestricted = json_w['max_users_x2go_unrestricted']
			except:
				pass
			try:
				workstation.min_CPU_console_user = json_w['min_CPU_console_user']
			except:
				pass
			try:
				workstation.max_CPU_each_non_console_user = json_w['max_CPU_each_non_console_user']
			except:
				pass
			try:
				workstation.min_RAM_console_user = json_w['min_RAM_console_user']
			except:
				pass
			try:
				workstation.max_RAM_each_non_console_user = json_w['max_RAM_each_non_console_user']
			except:
				pass
			workstation.last_update = datetime.today()
			workstation.save()
			ct_list = json_w['connection_type']
			for ct in ct_list:
				type_ct = ConnectionType.objects.get(name=ct)
				wt = WorkstationConnectionType.objects.create(workstation=workstation,connection_type=type_ct)  
			msg = "Workstation "+workstation.hostname+" created"
			print msg
			data = {"code": 0, "content": msg}
			return Response(data, status=status.HTTP_201_CREATED)
		else:
			workstation.restriction_time = rt
			workstation.ip=json_w['ip']
			workstation.certificate=json_w['certificate']
			workstation.status=json_w['status']
			workstation.max_users_ssh=json_w['max_users_ssh']
			workstation.max_users_x2go=json_w['max_users_x2go']
			workstation.max_hours_connection=json_w['max_hours_connection']
			workstation.waiting_time_before_reconnect=json_w['waiting_time_before_reconnect']
			workstation.interval_time_not_disconnection=json_w['interval_time_not_disconnection']
			workstation.room=json_w['room']
			workstation.last_update = datetime.today()
			try:
				workstation.max_users_ssh_unrestricted = json_w['max_users_ssh_unrestricted']
			except:
				pass
			try:
				workstation.max_users_x2go_unrestricted = json_w['max_users_x2go_unrestricted']
			except:
				pass
			try:
				workstation.min_CPU_console_user = json_w['min_CPU_console_user']
			except:
				pass
			try:
				workstation.max_CPU_each_non_console_user = json_w['max_CPU_each_non_console_user']
			except:
				pass
			try:
				workstation.min_RAM_console_user = json_w['min_RAM_console_user']
			except:
				pass
			try:
				workstation.max_RAM_each_non_console_user = json_w['max_RAM_each_non_console_user']
			except:
				pass
			workstation.save()
			
			msg = "Workstation "+workstation.hostname+" updated"
			print msg
			data = {"code": 0, "content": msg}
			return Response(data, status=status.HTTP_200_OK)
	if request.method == 'GET':
		pass

## Method to connect a user
@api_view(['POST','GET',])
#@permission_classes((IsAuthenticated,))
def connect(request, format=None):
	if request.method == 'POST':
		ct = None
		us = None
		ws = None
		wt = None
		wtall = None
		now = datetime.today()
		#now = timezone.now()
		# on cree le "WorkstationUser" Object
		try:
			ct = ConnectionType.objects.get(name=request.DATA['connection_type'])
		except:
			data = {"code": 2, "content": "Connection type does not exist", "connection_type": request.DATA['connection_type']}
			return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
		try:
			us, created = UserSystem.objects.get_or_create(username=request.DATA['username'])
		except:
			data = {"code": 3, "content": "User does not exist", "username": request.DATA['username']}
			return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
		try:
			ws = Workstation.objects.get(hostname=request.DATA['hostname'])
			ws.last_update = now
			ws.status = "online"
			ws.save()
		except:
			data = {"code": 4, "content": "Hostname does not exist", "hostname": request.DATA['hostname']}
			return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
		try:
			wt = WorkstationConnectionType.objects.filter(workstation=ws.hostname).get(connection_type=ct.name)
			wtall = WorkstationConnectionType.objects.filter(workstation=ws.hostname)
		except:
			data = {"code": 5, "content": "Workstation - Connection type link does not exist"}
			return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)

		if ct and us and ws and wt:
			try:
				restricted = is_restricted(ws, now)
				if restricted: # to modify because of the timezone
					wuqs = WorkstationUser.objects.filter(user=us).exclude(workstation_type_id__in=wtall)
					for wu in wuqs:
						if wu.logged:
							wtac = WorkstationConnectionType.objects.get(id=wu.workstation_type_id)
							msg = "You are already connect on " + wtac.workstation_id + "."
							data = {"code": 6, "content": msg}
							return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
					wuqs = WorkstationUser.objects.filter(user=us).filter(workstation_type_id__in=wtall).order_by('-connection_end')
					wuqdist = WorkstationUser.objects.filter(workstation_type_id=wt.id).exclude(user=us).exclude(logged=False).order_by('user').values('user').distinct()
					limited = vki_limit_connection(ws, ct, len(wuqdist))
					if limited:
						print "can connect"
					else:
						print "cannot connect"
						msg = "The maximum connection number has been reached."
						data = {"code": 9, "content": msg}
						return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
					for wu in wuqs:
						time_passed = can_reconnect(ws, wu, us, now)
						if time_passed == None:
							print "can reconnect"
						else:
							print "cannot reconnect"
							waiting_total_time = timedelta(hours=ws.waiting_time_before_reconnect)
							time_have_to_wait = waiting_total_time - time_passed
							msg = "You have to wait %s before to reconnect on %s." % (str(time_have_to_wait), ws.hostname)
							data = {"code": 8, "content": msg}
							return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
				else:
					wuqdist = WorkstationUser.objects.filter(workstation_type_id=wt.id).exclude(user=us).exclude(logged=False).order_by('user').values('user').distinct()
					if limit_connection(w, ct, wuqdist, restricted):
						print "can connect"
					else:
						msg = "The maximum connection number has been reached."
						data = {"code": 9, "content": msg}
						return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
			except:
				pass
			wu = WorkstationUser.objects.create(workstation_type_id=wt.id, user=us, logname=request.DATA['logname'], logged=True,connection_start=now)
			wu.save()
			msg = "You are succesfully connected on " + request.DATA['hostname']
			data = {"code": 0, "content": msg}
			return Response(data, status=status.HTTP_201_CREATED)
		else:
			data = {"code": 100, "content": "Critical error"}
			return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
				
			
	if request.method == 'GET':
		data = {"code": 1}
		return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)

## Method to disconnect a user
@api_view(['POST','GET',])
#@permission_classes((IsAuthenticated,))
def disconnect(request, format=None):
	if request.method == 'POST':
		#return Response(request.DATA)
		ct = None
		us = None
		ws = None
		wt = None
		now = datetime.today()
		#now = timezone.now()
		# on cree le "WorkstationUser" Object
		try:
			ct = ConnectionType.objects.get(name=request.DATA['connection_type'])
		except:
			data = {"code": 2, "content": "Connection type does not exist", "connection_type": request.DATA['connection_type']}
			return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
		try:
			us = UserSystem.objects.get(username=request.DATA['username'])
		except:
			data = {"code": 3, "content": "User does not exist", "username": request.DATA['username']}
			return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
		try:
			ws = Workstation.objects.get(hostname=request.DATA['hostname'])
			ws.last_update = now
			ws.status = "online"
			ws.save()
		except:
			data = {"code": 4, "content": "Hostname does not exist", "hostname": request.DATA['hostname']}
			return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
		try:
			wt = WorkstationConnectionType.objects.filter(workstation=ws.hostname).get(connection_type=ct.name)
		except:
			data = {"code": 5, "content": "Workstation - Connection type link does not exist"}
			return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)

		if ct and us and ws and wt:
			try:
				disconnection = False
				wuqs = WorkstationUser.objects.filter(workstation_type_id=wt.id).filter(user=us).order_by('-connection_start')
				for wu in wuqs:
					if wu.logged:
						wu.logged = False
						wu.connection_end = now
						wu.save()
						disconnection = True
						msg = "You are succesfully disconnected on " + request.DATA['hostname']
						data = {"code": 0, "content": msg}
						return Response(data, status=status.HTTP_201_CREATED)
				if not disconnection:
					data = {"code": 7, "content": "No connection to disconnect"}
					return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
					
			except:
				pass
		else:
			return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)
				
			
	if request.method == 'GET':
		data = {"code": 1}
		return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(['GET', 'POST', ])
#@permission_classes((IsAuthenticated,))
def modif_conf_host(request, hostname, format=None):
	created = False
	config = check_output(["curl", "http://"+hostname+"/info.conf"])
	if created:
		data = {"code": 0}
		return Response(data, status=status.HTTP_201_CREATED)
	else:
		data = {"code": 1}
		return Response(data, status=status.HTTP_503_SERVICE_UNAVAILABLE)


@api_view(('GET',))
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'workstations': reverse('workstation-list', request=request, format=format),
		'restriction-time': reverse('restriction-time-list', request=request, format=format),
		'connection-type': reverse('connection-type-list', request=request, format=format),
		'restriction-login': reverse('restriction-login-list', request=request, format=format),
		'group-system': reverse('group-system-list', request=request, format=format),
		'user-system': reverse('user-system-list', request=request, format=format),
		'workstation-type': reverse('workstation-type-list', request=request, format=format),
		'workstation-user': reverse('workstation-user-list', request=request, format=format),
		'buildings': reverse('buildings-list', request=request, format=format),
		'rooms': reverse('roomslist', request=request, format=format),
	})

## This viewset automatically provides `list`, `create`, `retrieve`,
#  `update` and `destroy` actions.
class WorkstationViewSet(viewsets.ModelViewSet):
	queryset = Workstation.objects.all()
	serializer_class = WorkstationSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

	def pre_save(self, obj):
		obj.owner = self.request.user

## This viewset automatically provides `list` and `detail` actions.
class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

## Retrieve, update or delete a RestrictionDay instance.
class RestrictionDayViewSet(viewsets.ModelViewSet):
	queryset = RestrictionDay.objects.all()
	serializer_class = RestrictionDaySerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

## Retrieve, update or delete a RestrictionTime instance.
class RestrictionTimeViewSet(viewsets.ModelViewSet):
	queryset = RestrictionTime.objects.all()
	serializer_class = RestrictionTimeSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

## Retrieve, update or delete a ConnectionType instance.
class ConnectionTypeViewSet(viewsets.ModelViewSet):
	queryset = ConnectionType.objects.all()
	serializer_class = ConnectionTypeSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

## Retrieve, update or delete a RestrictionLogin instance.
class RestrictionLoginViewSet(viewsets.ModelViewSet):
	queryset = RestrictionLogin.objects.all()
	serializer_class = RestrictionLoginSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

## Retrieve, update or delete a GroupSystem instance.
class GroupSystemViewSet(viewsets.ModelViewSet):
	queryset = GroupSystem.objects.all()
	serializer_class = GroupSystemSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

## Retrieve, update or delete a UserSystem instance.
class UserSystemViewSet(viewsets.ModelViewSet):
	queryset = UserSystem.objects.all()
	serializer_class = UserSystemSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

## Retrieve, update or delete a WorkstationConnectionType instance.
class WorkstationConnectionTypeViewSet(viewsets.ModelViewSet):
	queryset = WorkstationConnectionType.objects.all()
	serializer_class = WorkstationConnectionTypeSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

## Retrieve, update or delete a WorkstationUser instance.
class WorkstationUserViewSet(viewsets.ModelViewSet):
	queryset = WorkstationUser.objects.all()
	serializer_class = WorkstationUserSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

	@detail_route(methods=['post'])
	def accept_connection(self, request, pk=None):
		
		pass

## Retrieve, update or delete a Building instance.
class BuildingViewSet(viewsets.ModelViewSet):
	queryset = Building.objects.all()
	serializer_class = BuildingSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

## Retrieve, update or delete a room instance.
class RoomViewSet(viewsets.ModelViewSet):
	queryset = Room.objects.all()
	serializer_class = RoomSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
