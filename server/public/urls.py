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

from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns

from restriction_system.views import *
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

from restriction_system import views

from django.contrib import admin
admin.autodiscover()

workstation_list = WorkstationViewSet.as_view({
	'get': 'list',
	'post': 'create'
})

workstation_detail = WorkstationViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
})

user_list = UserViewSet.as_view({
	'get': 'list'
})

user_detail = UserViewSet.as_view({
	'get': 'retrieve'
})

restriction_day_list = RestrictionDayViewSet.as_view({
	'get': 'list',
	'post': 'create'
})

restriction_day_detail = RestrictionDayViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
})

restriction_time_list = RestrictionTimeViewSet.as_view({
	'get': 'list',
	'post': 'create'
})

restriction_time_detail = RestrictionTimeViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
})

connection_type_list = ConnectionTypeViewSet.as_view({
	'get': 'list',
	'post': 'create'
})

connection_type_detail = ConnectionTypeViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
})

restriction_login_list = RestrictionLoginViewSet.as_view({
	'get': 'list',
	'post': 'create'
})

restriction_login_detail = RestrictionLoginViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
})

group_system_list = GroupSystemViewSet.as_view({
	'get': 'list',
	'post': 'create'
})

group_system_detail = GroupSystemViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
})

user_system_list = UserSystemViewSet.as_view({
	'get': 'list',
	'post': 'create'
})

user_system_detail = UserSystemViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
})

workstation_type_list = WorkstationConnectionTypeViewSet.as_view({
	'get': 'list',
	'post': 'create'
})

workstation_type_detail = WorkstationConnectionTypeViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
})

workstation_user_list = WorkstationUserViewSet.as_view({
	'get': 'list',
	'post': 'create'
})

workstation_user_detail = WorkstationUserViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
})

building_list = BuildingViewSet.as_view({
	'get': 'list',
	'post': 'create'
})

building_detail = BuildingViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
})

room_list = RoomViewSet.as_view({
	'get': 'list',
	'post': 'create'
})

room_detail = RoomViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
})

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'restriction-day', views.RestrictionDayViewSet)
router.register(r'restriction-time', views.RestrictionTimeViewSet)
router.register(r'buildings', views.BuildingViewSet)
router.register(r'rooms', views.RoomViewSet)
router.register(r'workstations', views.WorkstationViewSet)
router.register(r'connection-type', views.ConnectionTypeViewSet)
router.register(r'workstation-type', views.WorkstationConnectionTypeViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'restriction-login', views.RestrictionLoginViewSet)
router.register(r'group-system', views.GroupSystemViewSet)
router.register(r'user-system', views.UserSystemViewSet)
router.register(r'workstation-user', views.WorkstationUserViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = patterns('',
	url(r'^$', 'restriction_system.views.home', name='home'),
	url(r'^api/', include(router.urls)),
	url(r'^api/docs', include('rest_framework_swagger.urls')),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^availability/(\w+)/$', 'restriction_system.views.availability', name='availability'),
	url(r'^about/$', 'restriction_system.views.about', name='about'),
)

urlpatterns2 = patterns('restriction_system.views',
	url(r'^connect/$', 'connect', name='connect'),
	url(r'^disconnect/$', 'disconnect', name='disconnect'),
	url(r'^cleanup/$', 'clean_workstation_users', name='clean_workstation_users'),
	url(r'^check-workstations/$', 'check_workstation', name='check_workstation'),
	url(r'^update-workstation/$', 'last_update', name='last_update'),
	url(r'^add-update/$', 'create_update_workstation', name='create_update_workstation'),
	url(r'^verification-connection/$', 'verification_connection', name='verification_connection'),
	url(r'^mod-conf-host/(\w+)/$', 'modif_conf_host', name='modif_conf_host'),
)

urlpatterns2 = format_suffix_patterns(urlpatterns2)

urlpatterns += urlpatterns2
