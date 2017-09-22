from bottle import get, post, request,route, run, template, static_file, redirect # or route
import ReadOSM as read
import threading
import time
#thread function
progress=0
class myThread (threading.Thread):
    def __init__(self,counter):
        threading.Thread.__init__(self)
        self.counter = counter
    def run(self):
        print ("Starting " + self.name)
        set_Progress(self.counter,)
        print ("Exiting " + self.name)


@get('/osm') # or @route('/osm')
def start():
    return '''
        <body background="white">
        <form action="/osm" method="post" align="center">
            <h1>Welcome to Open Street Map</h1></br></br>
            <h3>Enter the Following parameters to Get the OSM Data</h1>
            Minimum Latitude:</br></br>
            <input name="minlat" type="text" /></br></br>
            Minimum Longitude:</br></br>
            <input name="minlon" type="text" /></br></br>
            Maximum Latitude:</br></br>
            <input name="maxlat" type="text" /></br></br>
            Maximum Longitude:</br></br>
            <input name="maxlon" type="text" /></br></br>
            Relation ID:</br></br>
            <input name="relation" type="text" /></br></br>
            <h1>OR</h1>
            You can choose particular region</br></br>
            <input name = city type=text role="combobox"  aria-owns="listchoices"  list=browsers ></br></br>
            <datalist id=browsers >
            <option> New Delhi
            <option> Patiala
            <option> Ludhiana
            <option> Chandigarh
            </datalist>
            <input value="Get OSM Data" type="submit" />
        </form>
        </body>
    '''

@post('/osm') # or @route('/login', method='POST')
def do_osm():
    minlat = request.forms.get('minlat')
    minlon = request.forms.get('minlon')
    maxlat = request.forms.get('maxlat')
    maxlon = request.forms.get('maxlon')
    relation = request.forms.get('relation')
    city = request.forms.get('city')
    print(city)
    if city=="New Delhi":
        minlat=28.6034
        maxlat=28.6311
        minlon=77.1893
        maxlon=77.2485
        relation=1942586
    if city=="Patiala":
        minlat=30.1261
        minlon=76.1407
        maxlat=30.5362
        maxlon=76.6983
        relation=1948585
    if city=="Ludhiana":
        minlat=30.8244
        maxlat=31.0000
        minlon=75.6244
        maxlon=76.0501
        relation=1948490
    if city=="Chandigarh":
        minlat=30.7005
        maxlat=30.7495
        minlon=76.7251
        maxlon=76.8164
        relation=1942809
    thread1 = myThread(2)
    thread1.start()
    result=read.Map(min_lat=float(minlat),min_lon=float(minlon), max_lat=float(maxlat), max_lon=float(maxlon),area=city)
    if relation=="":
        result_relation="Empty"
        print("Relation is Empty but you can proceed with out Relation")
    else:
        result_relation=read.getRelation(relation)
    read.draw_graphs(min_lat=float(minlat),min_lon=float(minlon), max_lat=float(maxlat), max_lon=float(maxlon))
    devlp=read.development(result)
    #print(devlp)
    return template('''<body background="white" align="center">
                    <h1>Welcome to Open Street Map</h1></br></br>
                    <p>MAP Result is:</p><br>
                    <textarea rows="10" cols="100">{{map}}</textarea>
                    <p>Relation Result is:</p><br>
                    <textarea rows="4" cols="100" >{{rel}}</textarea>
                    <h2>Map of selected area is:</h2><br>
                    <img src="/static/Map.png"><br>
                    <h2>ATTRIBUTES<h2>
                    <table align="center">
                      <colgroup>
                        <col span="2" style="background-color:skyblue">
                        <col style="background-color:yellow">
                      </colgroup>
                    <tr>
                    <th>ATTRIBUTE</th>
                    <th>COUNT</th>
                    </tr>
                    <tr>
                    <td>Total Places</td>
                    <td>{{placecount}}</td>
                    </tr>
                    <tr>
                    <td>Total Ways</td>
                    <td>{{waycount}}</td>
                    </tr>
                    <tr>
                    <td>Total Building<h3></td>
                    <td>{{buildingcount}}</td>
                    </tr>
                    <tr>
                    <td>Total ATM</td>
                    <td>{{atmcount}}</td>
                    </tr>
                    <tr>
                    <td>Total Tolls </td>
                    <td>{{tollcount}}</td>
                    </tr>
                    </table>
                    <h2>ATTRIBUTE COMPLETENESS</h2>
                    <table align="center">
                      <colgroup>
                        <col span="2" style="background-color:skyblue">
                        <col style="background-color:yellow">
                      </colgroup>
                    <tr>
                    <th></th>
                    <th>ATTRIBUTE</th>
                    <th>COUNT</th>
                    </tr>
                    <tr>
                    <td>1.	General Information on Study Area </td>
                    <td>Missing tags </td>
                    <td>{{mtag}}</td>
                    </tr>
                    <tr>
                    <td></td>
                    <td>Ways without width <h3></td>
                    <td>{{www}}</td>
                    </tr>
                    <tr>
                    <td>2.	Points-Of-Interest</td>
                    <td>Shops without opening hours </td>
                    <td>{{swoh}}</td>
                    </tr>
                    <tr>
                    <td></td>
                    <td>Worship places without religion </td>
                    <td>{{wwr}}</td>
                    </tr>
                    <tr>
                    <td></td>
                    <td>Drive Through tag in pharmacy, bank, atm, or fastfood, postbox </td>
                    <td>{{dt}}</td>
                    </tr>
                    <tr>
                    <td></td>
                    <td>No of places with amenity =’fast_food’ or ‘restaurant’ or ‘bar’ or ‘café’ without cuisine tags</td>
                    <td>{{wocuisine}}</td>
                    </tr>
                    <tr>
                    <td>3.	Geocoding</td>
                    <td>No. of POIs without names and housenumbers</td>
                    <td>{{poi}}</td>
                    </tr>
                    <tr>
                    <td></td>
                    <td>No. of building with missing tags Height and Levels</td>
                    <td>{{bmt}}</td>
                    </tr>
                    <tr>
                    <td>4.	Routing and Navigation</td>
                    <td>No of Highways with missing tag ‘maxspeed’ </td>
                    <td>{{nomxsp}}</td>
                    </tr>
                    <tr>
                    <td></td>
                    <td>No of Tolls with missing tag ‘charge’ </td>
                    <td>{{nochrg}}</td>
                    </tr>
                    <tr>
                    <td></td>
                    <td>No of Railway without crossing tags</td>
                    <td>{{nort}}</td>
                    </tr>
                    <tr>
                    <td></td>
                    <td>Ways with layer tag without tag bridge or tunnel </td>
                    <td>{{nolyr}}</td>
                    </tr>
                    </table>
                    <h2>Number of nodes in each version:</h2><br>
                    <img src="/static/node_number_version.png"></br>
                    <h2>Version History of Nodes:</h2><br>
                    <img src="/static/history_chart.png"></br>
                    <h2>Bar Chart of Buildings created in last five years is:</h2><br>
                    <img src="/static/building_chart.png"><br>
                    <h2>Bar Chart of Nodes created in last five years is:</h2><br>
                    <img src="/static/node_chart.png"><br>
                    <h2>Bar Chart of way created in last five years is:</h2><br>
                    <img src="/static/way_chart.png"></br>
                    <h1>Development:</h1></br>
                    <h2>Development of Nodes in Last five years<h2><br>
                    <table align="center">
                      <colgroup>
                        <col span="2" style="background-color:skyblue">
                        <col style="background-color:yellow">
                      </colgroup>
                    <tr>
                    <th>Year</th>
                    <th>Development</th>
                    </tr>
                    <tr>
                    <td>Year 2012</td>
                    <td><pre>{{ffn}}</pre></td>
                    </tr>
                    <tr>
                    <td>Year 2013<h3></td>
                    <td><pre>{{frn}}</pre></td>
                    </tr>
                    <tr>
                    <td>Year 2014</td>
                    <td><pre>{{tn}}</pre>}</td>
                    </tr>
                    <tr>
                    <td>Year 2015</td>
                    <td><pre>{{sn}}</pre></td>
                    </tr>
                    <tr>
                    <td>Year 2016</td>
                    <td><pre>{{fn}}</pre></td>
                    </tr>
                    </table>
                    <h2>Development of Ways in Last five years<h2><br>
                    <table align="center">
                      <colgroup>
                        <col span="2" style="background-color:skyblue">
                        <col style="background-color:yellow">
                      </colgroup>
                    <tr>
                    <th>Year</th>
                    <th>Development</th>
                    </tr>
                    <tr>
                    <td>Year 2012</td>
                    <td><pre>{{ffw}}</pre></td>
                    </tr>
                    <tr>
                    <td>Year 2013</td>
                    <td><pre>{{frw}}</pre></td>
                    </tr>
                    <tr>
                    <td>Year 2014</td>
                    <td><pre>{{tw}}</pre></td>
                    </tr>
                    <tr>
                    <td>Year 2015</td>
                    <td><pre>{{sw}}</pre></td>
                    </tr>
                    <tr>
                    <td>Year 2016</td>
                    <td><pre>{{fw}}</pre></td>
                    </tr>
                    </table>
                    </body>
                    ''',devlp,map=result,rel=result_relation,)


def set_Progress(delay):
    global progress
    while progress<100:
        time.sleep(delay)
        progress=read.read_Progress()
        print_progress()
    return

@post('/osm/prog')
def print_progress():
    global progress
    print("\nProgress",progress)
    return template('<b>completed: {{prog}} %</b>',prog=progress)

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='C:/Users/user/Desktop/final/OSM/OSM/Pics')


run(host='localhost', port=5000)
