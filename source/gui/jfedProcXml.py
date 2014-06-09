
#!/usr/bin/env python

#
#    Copyright (C) 2014 DEIMOS
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: Ruben Perez <ruben.perez@deimos-space.com>


from xml.dom import minidom

class JFedParser():
    def __init__(self,file):
        self.document = minidom.parse(file)
        self.nodes = self.document.getElementsByTagName("node")
    def reparse(self,file):
        self.document = minidom.parse(file)

    def get_groundStations(self):
        gs = []
        for node in self.nodes:
            if node.attributes['client_id'].value.find("GS") != -1:
                host = node.getElementsByTagName('host')
                gs.append(str(host[0].attributes['name'].value))
        return gs
    
    def get_satellites(self):
        sat = []
        for node in self.nodes:
            if node.attributes['client_id'].value.find("SS") != -1:
                host = node.getElementsByTagName('host')
                sat.append(str(host[0].attributes['name'].value))
        return sat

if __name__ == "__main__":
    parser = JFedParser("resources/jfed.out")
    gs=parser.get_groundStations()
    print gs
    gs=parser.get_satellites()
    print gs
