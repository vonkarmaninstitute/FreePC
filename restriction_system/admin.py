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

## @package admin
#  Documentation for the package admin

from django.contrib import admin
from restriction_system.models import *

# Register your models here.

## Admin class to manage the restriction time.
class RestrictionTimeAdmin(admin.ModelAdmin):
	list_display = ('id','start','end')
	ordering = ('id',)

## Admin class to manage the restriction day.
class RestrictionDayAdmin(admin.ModelAdmin):
	list_display = ('name', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
	list_editable = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')
	ordering = ('name',)

## Admin class to manage the workstations.
class WorkstationAdmin(admin.ModelAdmin):
	list_display = ('hostname', 'ip', 'room', 'last_update', 'status')
	list_editable = ('status', 'room')
	list_filter = ('status', 'room')
	ordering = ('hostname', '-last_update', 'room' )
	list_per_page = 20

## Admin class to manage the connection types.
class ConnectionTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'priority')
	ordering = ('name', )

## Admin class to manage the login restrictions.
class RestrictionLoginAdmin(admin.ModelAdmin):
	list_display = ('restriction',)
	ordering = ('id', )

## Admin class to manage the groups.
class GroupSystemAdmin(admin.ModelAdmin):
	ordering = ('id', )

## Admin class to manage the users.
class UserSystemAdmin(admin.ModelAdmin):
	list_display = ('username', 'group_system')
	ordering = ('username', )

## Admin class to manage the group restrictions.
class GroupRestrictionAdmin(admin.ModelAdmin):
	list_display = ('group', 'restriction')
	ordering = ('id', )

## Admin class to manage the link between a workstation and a connection type
class WorkstationConnectionTypeAdmin(admin.ModelAdmin):
	list_display = ('workstation', 'connection_type')
	ordering = ('id', )

## Admin class to manage the connected users
class WorkstationUserAdmin(admin.ModelAdmin):
	list_display = ('workstation_type', 'user', 'connection_start', 'connection_end', 'logged')
	list_display_link = ('user',)
	search_fields = ['user__username']
	list_editable = ('logged',)
	ordering = ('-connection_start', 'user')
	list_filter = ('logged',)
	list_per_page = 20

admin.site.register(RestrictionTime, RestrictionTimeAdmin)
admin.site.register(RestrictionDay, RestrictionDayAdmin)
admin.site.register(Workstation, WorkstationAdmin)
admin.site.register(ConnectionType, ConnectionTypeAdmin)
admin.site.register(RestrictionLogin, RestrictionLoginAdmin)
admin.site.register(GroupSystem, GroupSystemAdmin)
admin.site.register(UserSystem, UserSystemAdmin)
admin.site.register(GroupRestriction, GroupRestrictionAdmin)
admin.site.register(WorkstationConnectionType, WorkstationConnectionTypeAdmin)
admin.site.register(WorkstationUser, WorkstationUserAdmin)
