# -*- coding: utf-8 -*-
#
#    bitcoinlib - Compact Python Bitcoin Library
#    Base Client
#    © 2016 November - 1200 Web Development <http://1200wd.com/>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import requests
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import json
from bitcoinlib.main import *
from bitcoinlib.config.services import serviceproviders

_logger = logging.getLogger(__name__)

class ClientError(Exception):
    def __init__(self, msg=''):
        self.msg = msg
        _logger.error(msg)

    def __str__(self):
        return self.msg


class BaseClient(object):

    def __init__(self, network, provider):
        try:
            self.network = network
            self.provider = provider
            self.base_url = serviceproviders[network][provider][1]
            self.resp = None
            self.units = serviceproviders[network][provider][2]
        except:
            raise ClientError("This Network is not supported by %s Client" % provider)

    def request(self, url_path, variables=None):
        url_vars = ''
        if variables is None:
            variables = []
        if variables:
            url_vars = '?' + urlencode(variables)
        url = self.base_url + url_path + url_vars
        print(url)
        self.resp = requests.get(url)
        if self.resp.status_code == 429:
            raise ClientError("Maximum number of requests reached for %s with url %s, response [%d] %s" %
                              (self.provider, url, self.resp.status_code, self.resp.text))
        elif self.resp.status_code != 200:
            raise ClientError("Error connecting to %s on url %s, response [%d] %s" %
                              (self.provider, url, self.resp.status_code, self.resp.text))
        return json.loads(self.resp.text)