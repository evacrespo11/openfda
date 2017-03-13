# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2016 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#     Eva Encinas Crespo
#

'''<html>
<head></head>
<body>
  <ul>  #Comienzo de una lista desordenada
    <li>Drug1</li> #List item
    ...
    <li>Drug10</li>
  </ul>
</body>
</html>'''

import http.server
import socketserver

import http.client   #biblioteca
import json
##
# WEB SERVER
##



class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

#OPENFDA_API_URL = "api.fda.gov" ----> por si en el conn hubieses puesto OPENFDA_API_URL


    OPENFDA_API_URL = "api.fda.gov"
    OPENFDA_API_EVENT = "/drug/event.json"
    OPENFDA_API_LYRICA = "/drug/event.json?search=patient.drug.medicinalproduct="
    OPENFDA_API_COMPANY = "/drug/event.json?search=companynumb"

    def get_event (self):

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_EVENT + "?limit=10")
        r1 = conn.getresponse()

        data1 = r1.read()
        data = data1.decode("utf8")
        data2 = json.loads(data) #----> a diccioneario cuando es load es de fichero adicc y loads es de str a dicc

        return data2

    def get_lyrica (self):

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_LYRICA + self.get_input() + "&limit=10")
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode("utf8")
        data2 = json.loads(data) #----> a diccionario cuando es load es de fichero adicc y loads es de str a dicc

        return data2

    def get_company(self):

        conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request("GET", self.OPENFDA_API_COMPANY + "&limit=10")
        r1 = conn.getresponse()
        data1 = r1.read()
        data = data1.decode("utf8")
        data2 = json.loads(data)

# GET

    def do_GET(self):

        #P
        main_page = False
        is_event_drug = False
        is_search_drug = False

        is_event_company = False
        is_search_company = False

        if self.path == '/':
            main_page = True

        elif "search_drug" in self.path:
            is_search_drug = True

        elif self.path == '/receive_drug':
            is_event_drug = True

        elif "search_company" in self.path:
            is is_search_company = True

        elif self.path == '/receive_company':
            is is_event_company = True



        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        html = self.get_main_page()

        if main_page:
            self.wfile.write(bytes(html, "utf8")) #Aqui hemos tenido que cambiar el message por un html

        elif is_event_drug:
            event = self.get_event()

            event1 = event["results"]
            #for i in range(len(event1)):
                #drug = [i]["patient"]["medicinalproduct"]
                #print (drug)
                #print (event1[1])
            lista1 = []
            for event in event1:
                event2 = (event['patient']['drug'][0]['medicinalproduct'])
                # if EVENT2 == MEDI_INTRO:
                event3 = json.dumps(event2) #de dicc a str
                lista1 += [event3]
            html_medicinas=self.get_event_html(lista1)
            self.wfile.write(bytes(html_medicinas , "utf8"))

            return

        elif is_search_drug:

            search=self.get_lyrica()

            search1 = search["results"]
            lista =[]
            for event in search1:

                search2 = event['companynumb']
                search3 =json.dumps(search2)
                lista += [search3]

            html_search=self.get_search_html(lista)
            self.wfile.write(bytes(html_search , "utf8"))
            return



        # Send message back to client
        #message = "Hello world! " + self.path
    def get_main_page(self):

        html = """
        <html>
            <head>
                <title>OpenFDA Cool App</title>
            </head>
            <body>
                <h1>OpenFDA Client</h1>
                <form method="get" action="receive_drug">
                    <input type = "submit" value="10 DRUGS">
                    </input>
                </form>
                <form method="get" action="search_drug">
                    <input type = "text" name="drug"></input>
                    <input type = "submit" value="Search Drug">
                    </input>
                </form>
                <form method="get" action="receive_company">
                    <input type = "submit" value="10 COMPANIES">
                    </input>
                </form>
                <form method="get" action="search_company">
                    <input type = "text" name="companies"></input>
                    <input type = "submit" value="Search Companies">
                    </input>
                </form>
            </body>
        </html>
        """
        return html

    def get_event_html (self, lista):

        html_event = """
        <html>
            <head></head>
            <body>
                <h1>Medicamentos</h1>
            <ul>
        """
        for i in lista:
            html_event+="<li>"+i+"</li>"

        html_event+="""
            </ul>
            </body>
        </html>
        """

        return html_event


    def get_search_html (self, lista):

        html_search = """
        <html>
            <head></head>
            <body>
                <h1>Companies</h1>
            <ul>
        """
        for i in lista:
            html_search+="<li>"+i+"</li>"

        html_search+="""
            </ul>
            </body>
        </html>
        """

        return html_search

    def get_input(self):

        drug =self.path
        drug1=drug.split('=')[1]

        return drug1


    #de array a str: a= ["1","2"]
    # "," join(a)

    #loads: str---->dicc
    #dumps: dicc---->str
    #<ul> ---> voy a abrir una lista
