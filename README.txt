obi-status.py
=============

obi-status.py is a very small and simple script that display the status of the [OBi110][] VoIP Telephone Adapter. More specifically, it displays the status of your SIP account registration. It takes the form of an icon whose color changes to indicate the following status:

* green: the OBi110 is operating properly (i.e. the service provider is operating correctly). 
* red: the OBi110 is not operating properly and might need a manual intervention (e.g. rebooting a failing router with a crappy SIP port forwarding module)
* grey: can not know the status of the OBi110

[OBi110]: http://obihai.com/product-primer.html

Why should I use this script?
=============================

* Well... you should'nt! I wrote it mainly to fit my needs.
* OK, if you insist, you could use it because you can not physically see the OBi110 unit (e.g. hidden in a bookshelf) and still want to know when it is not operating properly anymore.

How does it works
=================

The script is very simple (i.e. stupid) and retrieve the http://YOUROBIADDRESS/DI_S_.xml page. It then parse the page for some keywords in order to evaluate the status of the SIP service provider. 

How to set it up
================

Modify the obi-status.cfg to reflect your OBi110 configuration. You can then copy the obi-status.cfg to your home directory or you can pass a custom path as an argument to the script using "-c". 

Dependencies
============

* Python (2.7 or more)
* PyGTK (2.24 or more)

Althrough, I believe this script might work with older versions, but I have not tested them.

Acknowledgements
================

* my wife, Julie, who motivated me to write the script
* Joël Schaerer (AKA joelthelion) for its [Tomate](https://gitorious.org/tomate) software (I borrowed most of its PyGTK code)
 
Licence
=======

This code is licenced under the GNU General Public License version 3 (GPLv3).
