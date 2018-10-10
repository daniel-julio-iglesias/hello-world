#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""REST Based Web Services

WAM 2.2.02
OUAF 4.3.0.6

Note: REST Support is available in Oracle Utilities Application Framework 4.3.0.2.0 and above.
One of the newest methods for integration is Restful Services. REST based web services allow
requesting systems to access and manipulate textual representations of web resources using
a uniform and predefined set of stateless operations

Limitations of REST Support
This implementation of REST is an initial set of facilities available for integration and is
bundled in the online server in this release. In future releases, this facility will be
expanded to support additional functionality and be moved to an integration implementation,
along with Inbound Web Services.
The following limitations apply to this release of the REST support:
...

REST Security Fundamentals
Fundamentally REST is a conversational protocol which reuses the existing HTTP/S protocol.
This is important to understand for a number of reasons:

- To invoke a REST service a session token must be obtained for all subsequent calls from that
location. In the implementation of REST you must invoke a call from the location using the URL
shown below, with the authentication credentials, as a "POST", and retrieve the session token
generated by the J2EE Web Application Server:
http://<host>:<port>/<context>/restSecurityToken
where:
<host> Host for the online server
<port> Port number for the cluster or server for online
<context> Context root set at installation time.

- This session token must be used for ALL subsequent calls from that client till either the
non-activity timeout is reached or the session is terminated by the J2EE Web Application Server.

- You cannot generate a new session token for each call as that may be interpreted as an invalid
call by the J2EE Web Application Service.

- The "ouafSecurityToken" ("OUAF-Security-Token") value will be returned in the header that needs to be
reused for each subsequent call.


Setting Up REST Services
By default a REST based servlet is deployed to the online server with a predefined context to
support REST based services. By default all the following object types are exposed as Web Services:
» Business Objects
» Business Services
» Service Scrip
The associated schemas with these objects can be exposed in XML or JSON format for the interface.

Invoking REST Services
After getting a session token, the REST service can be invoked using a POST:
Object Invocation URL
Business Object https://<host>:<port>/<context>/<servletRoot>/ouaf/busObj/<businessObject>
Business Service https://<host>:<port>/<context>/<servletRoot>/ouaf/busSvc/<businessService>
Service Script https://<host>:<port>/<context>/<servletRoot>/ouaf/script/<serviceScript>
Where:
<host> Host Name for product server
<port> Port Number for online server
<context> Context set for the environment
<servletRoot> REST Servlet Root context. In Oracle Utilities Application Framework 4.2.0.2
and above the value is "rest" and for Oracle Utilities Application Framework V4.3.0.4
and above, the value is "resources".
<businessObject> Business Object Name
<businessService> Business Service Name
<serviceScript> Service Script Name
For example:
http://somehost:6500/ouaf/rest/ouaf/message/busSvc/F1User

REST Formats

By default the transmission of data in REST is in XML format (application/xml). JSON is
also supported by setting the following variables in the header:

Header Variable Value
Content-Type "Content-Type: application/json"
Accept Accept: "application/json"

When using JSON the request payload may look like:
{"scriptname": {"input": {"fieldA": "ABC", "fieldB": 12345} } }
The corresponding output may look like:
{"scriptname": {"input": {"fieldA": "ABC", "fieldB": 12345}, "output": {"result": "def"} } }
For schemas that include lists the JSON returns an instance for each row. For example:
{"scriptName": {"outputList": [ {"item": "one"}, {"item": "two"} ] }}

Mapping XML to JSON

The Oracle Utilities Application Framework automatically transforms XML to JSON when JSON
is specified as the output format. The transform uses the following rules:

- There are three different techniques available to convert between XML and JSON. These are
available using the "JSON_CONVRSN_METH_FLG" lookup. The three methods are:
    - Standard API Conversion – This is a Jettison based conversion method.
    - XSL Transformation – This allows an implementation custom method for transforming XML to
    JSON and vice-versa. You must configure the custom XSL used for the transformation. Refer to
    the online help for details of this configuration.
    - OUAF JSON Conversion – This is the internal converter supplied with the Oracle Utilities
    Application Framework. This section will document the transformation rules used by this
    conversion

REST Services Security

REST based services uses session-based authentication, either by establishing a session token
via a POST or by using an API key as a POST body argument or as a cookie.
Note: Oracle highly recommends that usernames, passwords, session tokens, and API keys
should not appear in the URL.

Guaranteed Delivery
By default, the REST support provides a real time request and response architecture. If the server
cannot process the REST call then an appropriate error is issued. For some implementations,
it is necessary to guarantee the transaction is completed, even asynchronously. A facility in
the product allows an object to be specified as a repository to persist the inbound transaction
to process it when the resources are available.
The facility is specified as an algorithm on the installation record for the Guaranteed Delivery
system event.
Note: Individual products may ship algorithms for use in implementations. If no algorithm is
supplied, then the product cannot use this facility.
Note: For more information about this facility refer to the online documentation and the
"F1-GuaranteedDelivery" business service.

REST Error Format
The REST interface produces a Problem Detail document in XML/JSON format that outlines the
information about the error that has occurred. The format is as outlined below:

Element Usage
problemType URL of format:
    <protocol>://<host>:<port>/<context>/<restcontext>/ouaf/message/<category>/<message>
    Where:
    <protocol> - Protocol used. Usually http or https.
    <host> - Hostname or IP address of server generating error.
    <port> - Port number of environment generating error.
    <context> - Server context set at installation time.
    <restcontext> - REST servlet context. Varies according to version (either rest or resources)
    <category> - Message category within Oracle Utilities Application Framework
    <message> - Message Number within Oracle Utilities Application Framework
title Fully qualified error message from Oracle Utilities Application Framework in CDATA format
httpStatus The HTTP Status code for the error
detail The long message description from the Oracle Utilities Application Framework in CDATA format
problemInstance Fully qualified URL with data and identity in format:
    <protocol>://<host>:<port>/<context>/<restcontext>/ouaf/errorMessageInstance/<time
    stamp>/<user>/<category>/<message>?request=<request>;method=<method>
    Where:
    <protocol> - Protocol used. Usually http or https.
    <host> - Hostname or IP address of server generating error.
    <port> - Port number of environment generating error.
    <context> - Server context set at installation time.
    <restcontext> - REST servlet context. Varies according to version (either rest or resources)
    <timestamp> - Timestamp of error in ISO format.
    <user> - User used for transaction.
    <category> - Message category within Oracle Utilities Application Framework
    <message> - Message Number within Oracle Utilities Application Framework
    <request> - Request URL
<method> - HTTP method used for transaction
serverMessage Server Message group
messageCategory Message category within Oracle Utilities Application Framework
messageNbr Message Number within Oracle Utilities Application Framework
callSequence Delimited sequence of programs called.
messageText Fully qualified error message from Oracle Utilities Application Framework in CDATA format
longDescription The long message description from the Oracle Utilities Application Framework in CDATA format
"""

from config import Config
import json
import requests


# proxies = {
#     'http': 'http://username:password@Proxyadresse:Proxyport',
#     'https': 'https://username:password@Proxyadresse:Proxyport',
# }


class APITest:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.base_uri = 'http://httpbin.org'

    def get(self):
        uri = self.base_uri + '/get'
        print(uri)
        r = requests.get(self.base_uri + '/get')
        # r = requests.get(self.base_uri + '/get', proxies=proxies)
        return r.json()


def main():
    # print("Hello World!")
    api_test = APITest()
    print(api_test.get())

    # r = requests.get('http://httpbin.org/get', proxies=proxies)
    # print(r)


if __name__ == '__main__':
    main()
