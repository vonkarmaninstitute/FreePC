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

## @package serializers
#  Documentation for the serializer package

from restriction_system.models import *
from django.forms import widgets
from rest_framework import serializers
from django.contrib.auth.models import User

## Class to serialize RestrictionDay
class RestrictionDaySerializer(serializers.ModelSerializer):
	
	class Meta:
		model = RestrictionDay

## Class to serialize RestrictionTime
class RestrictionTimeSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = RestrictionTime

## Class to serialize ConnectionType
class ConnectionTypeSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = ConnectionType

## Class to serialize Workstation
class WorkstationSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Workstation

## Class to serialize RestrictionLogin
class RestrictionLoginSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = RestrictionLogin

## Class to serialize GroupSystem
class GroupSystemSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = GroupSystem

## Class to serialize UserSystem
class UserSystemSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = UserSystem

## Class to serialize GroupRestriction
class GroupRestrictionSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = GroupRestriction

## Class to serialize WorkstationConnectionType
class WorkstationConnectionTypeSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = WorkstationConnectionType

## Class to serialize WorkstationUser
class WorkstationUserSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = WorkstationUser

## Class to serialize User
class UserSerializer(serializers.ModelSerializer):
	
	workstations = serializers.HyperlinkedRelatedField(many=True, view_name='workstation-detail')

	class Meta:
		model = User
		fields = ('id', 'username', 'workstations')

## Class to serialize Building
class BuildingSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Building

## Class to serialize Room
class RoomSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Room


## Class to serialize Connection
class ConnectionSerializer(serializers.Serializer):
	
	workstation = serializers.CharField(required=True, max_length=64)
	connection_type = serializers.CharField(required=True, max_length=64)
	logname = serializers.CharField(required=False, max_length=128)
