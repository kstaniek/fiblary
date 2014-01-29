.. fiblary documentation master file, created by
   sphinx-quickstart on Sat Jan 18 10:03:51 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Fiblary's documentation!
===================================

Other sections:

.. toctree::
   :maxdepth: 1

   Examples
   API Docs
   
============
Introduction
============

Fiblary is a Python module wrapping Fibaro Home Center REST API. 
This allows Python programs to make calls directly to Home Center and
control the Z-wave devices and run scenes managed by HC. 
It also provides access and methods to variables, users, room
and sections defined on Home Center.

The main client object contains several managers controlling a basic
functions of HC:
* Sections,
* Rooms,
* Info,
* Weather, 
* Variables,
* Scenes,
* Devices,
* Events,
    
    and more.

It's easiest to to get some basic information about the Home Center::

    from fiblary.client import Client
    
    # Connect to Home Center
    hc = Client('v3', 'http://192.168.1.1/api', 'admin', 'admin')
    
    # Retrieve the basic info asreturned by /api/info
    info = hc.info.get()
    
    print(info)
    
will produce the similar output as below::

    {u'batteryLowNotification': True, u'temperatureUnit': u'C', u'updateStableAvailable': False, u'sunsetHour': u'16:29',
    u'softVersion': u'3.580', u'newestBetaVersion': u'3.581', u'serialNumber': u'HC2-000666', u'sunriseHour': u'07:24',
    u'beta': False, u'defaultLanguage': u'pl', u'mac': u'38:60:77:92:bf:a5', u'serverStatus': 1390148753, u'hotelMode': True,
    u'updateBetaAvailable': True, u'zwaveVersion': u'3.42'}
    
    
The returned ``info`` behaves like a dictionary::
    
    print info['softVersion']
    
but also like a proprerty::
    
    print info.softVersion
        
``VERSION`` can be: "v3" or "v4". The library is prepared to handle new API v4 when unveiled by vendor.

Easy, eh?


For the managers that ``Client`` supports the full set of options is implemented.
