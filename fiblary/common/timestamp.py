#  Copyright 2014 Klaudiusz Staniek
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
 fiblary.timiestamp
 ~~~~~~~~~~~~~~~~~~

 Timestamp manipulations

"""

import datetime as dt
import dateutil


def timestamp_to_iso(timestamp):
    return dt.datetime.fromtimestamp(timestamp).isoformat(' ')


def datetime_to_epoch(date_time):
    return date_time.strftime('%s')
    # return int((date_time - dt.datetime(1970,1,1)).total_seconds())


def string_to_datetime(date_time):
    return dateutil.parser.parse(date_time)
