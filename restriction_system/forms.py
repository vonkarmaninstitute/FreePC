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

## @package forms
#  Documentation for the forms package

from django import forms
from restriction_system.models import *

class FormRestrictionTime(forms.ModelForm):
	class Meta:
		model = RestrictionTime

class FormConnectionType(forms.ModelForm):
	class Meta:
		model = ConnectionType

class FormWorkstation(forms.ModelForm):
	class Meta:
		model = Workstation

class FormRestrictionLogin(forms.ModelForm):
	class Meta:
		model = RestrictionLogin

class FormGroupSystem(forms.ModelForm):
	class Meta:
		model = GroupSystem

class FormUserSystem(forms.ModelForm):
	class Meta:
		model = UserSystem

class FormGroupRestriction(forms.ModelForm):
	class Meta:
		model = GroupRestriction

class FormWorkstationConnectionType(forms.ModelForm):
	class Meta:
		model = WorkstationConnectionType

class FormWorkstationUser(forms.ModelForm):
	class Meta:
		model = WorkstationUser

