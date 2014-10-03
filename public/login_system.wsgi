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

import os, sys
#Calculate the path based on the location of the WSGI script
apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)
sys.path.append('/var/www/html/login_system')

os.environ['DJANGO_SETTINGS_MODULE'] = 'login_system.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
