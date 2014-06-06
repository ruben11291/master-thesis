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
