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
 fiblary.common.beacon
 ~~~~~~~~~~~~~~~~~~~~~

 Home Center Beacon Implementation

"""


from fiblary.common.net import get_mac
import socket
import threading

SERVER_TIMEOUT = 0.2


class Beacon(threading.Thread):
    def __init__(self, serial):
        threading.Thread.__init__(self)
        self.port = 44444
        self.key = 'FIBARO'
        self.quit = False
        self.serial = serial

        self.mac = get_mac()

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(SERVER_TIMEOUT)
        sock.bind(("", self.port))

        while not self.quit:
            try:
                message, address = sock.recvfrom(len(self.key))
            except socket.error:
                continue

            if message != self.key:
                # not my client
                continue

            sock.sendto('ACK {} {}'.format(self.serial, self.mac), address)

        sock.close()

# b = Beacon('HC2-999329')
# b.daemon = True
# b.start()
# time.sleep(10000)
