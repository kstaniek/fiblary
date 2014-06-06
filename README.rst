Fiblary Project
===============

Introduction
------------

Fiblary is a Python module wrapping Fibaro Home Center REST API. 
This allows Python programs to make calls directly to Home Center and
control the Z-wave devices and run scenes managed by HC. 
It also provides access and methods to variables, users, room
and sections defined on Home Center.

Installation
------------

Current fiblary module is provided as PyPi package. To install on a unix based system use pip::
    
    pip install fiblary


Basic usage
-----------

The main client object contains several managers controlling a basic
functions of HC:

* Sections,
* Rooms,
* Info,
* Weather, 
* Variables,
* Scenes,
* Devices,
* Events
    
and more.

It's easiest to to get some basic information about the Home Center::

    from fiblary.client import Client
    
    # Connect to Home Center
    hc = Client('v3', 'http://192.168.1.1/api/', 'admin', 'admin')
    
    # Retrieve the basic info as returned by /api/info
    info = hc.info.get()
    
    print(info)
    
will produce the similar output as below::

    {u'batteryLowNotification': True, u'temperatureUnit': u'C', u'updateStableAvailable': False, u'sunsetHour': u'16:29',
    u'softVersion': u'3.580', u'newestBetaVersion': u'3.581', u'serialNumber': u'HC2-000666', u'sunriseHour': u'07:24',
    u'beta': False, u'defaultLanguage': u'pl', u'mac': u'38:60:77:92:bf:a5', u'serverStatus': 1390148753, u'hotelMode': True,
    u'updateBetaAvailable': True, u'zwaveVersion': u'3.42'}
    
    
The returned ``info`` behaves like a dictionary::
    
    print info['softVersion']
    
but also like a property::

    print info.softVersion

Easy, eh?

For the managers that ``Client`` supports the full set of options is implemented.

Please refer to the example code attached to the project.


License
-------

Copyright (c) 2014 Klaudiusz Staniek

Apache License Version 2.0 http://www.apache.org/licenses/LICENSE-2.0