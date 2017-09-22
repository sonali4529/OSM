#impot osm api
from osmapi import OsmApi
#import time
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D as lines
plat=0
plong=0
f=0
placecount=0
waycount=0
atmcount=0
buildingcount=0
tollcount=0
progress=0
#function to read node
def getNode(id,name) :
    #time is started
    start_time = time.time()
    MyApi=OsmApi()
    #print("The node is : ", MyApi.NodeGet(id))
    node=MyApi.NodeGet(id)
    waysDraw(node['lat'],node['lon'],name)#this node goes to draw ways
    #print("Time taken in the Process --- %s seconds ---" % (time.time() - start_time))
    return

#function to read MAP
def Map(min_lon, min_lat, max_lon, max_lat,area):
    global mini_lon
    global mini_lat
    global maxi_lon
    global maxi_lat
    mini_lon = min_lon
    mini_lat = min_lat
    maxi_lon = max_lon
    maxi_lat = max_lat
    #time is started
    start_time = time.time()
    MyApi=OsmApi()
    result=MyApi.Map(min_lon, min_lat, max_lon, max_lat)#get dataset from OSM website
    #create new figure for map
    fig, ax = plt.subplots()#add labels, title and axes ticks
    ax.ticklabel_format(useOffset=False)
    ax.set_ylabel('Longitude')
    ax.set_xlabel('Latitude')
    ax.set_title(area)
    for rs in result:
        if(rs['type']=="node"):#to print the places
            if(len(rs['data']['tag'])!=0):#check place is not empty
                try:#try if a place has no name
                    key=rs['data']['tag'].keys()
                    detail=""
                    for k in key:
                        detail=detail+k+" - "+rs['data']['tag'][k]+"\n"#collect all information of particular node
                        #print (detail)
                    placesDraw(lat=rs['data']['lat'],long=rs['data']['lon'],name=detail)
                except:
                    print("error")
        elif(rs['type']=="way"):#to print the ways
            if(len(rs['data']['nd'])!=0):
                key=rs['data']['tag'].keys()
                detail=""
                for k in key:
                    detail=detail+k+" - "+rs['data']['tag'][k]+"\n"#collect all information of particular way
                    #print (detail)
                global f
                f=0# a new way is started
                for nd in rs['data']['nd']:
                    getNode(nd,detail)
    draw_graphs(min_lat,max_lat,min_lon, max_lon)
    return result;

#to draw the places with names
def placesDraw(lat,long,name):
    plt.plot([lat,], [long,], 'ro')
    plt.annotate(name, xy=(lat, long),size=10,color='blue'
            )
    return
#to draw ways with names
def waysDraw(lat,long,name):
    global f
    global plat
    global plong
    if(f==0):#check way is new 
        f=1
        plat=lat
        plong=long
        plt.annotate(name, xy=(lat, long),size=10,
            )
    elif(f==1):
        plt.plot([plat,lat],[plong,long],color='black')
        plat=lat
        plong=long
    return

def draw_graphs(mini_lat,maxi_lat,mini_lon, maxi_lon):
    print("Reached draw graphs")
    plt.axis([mini_lat,maxi_lat,mini_lon, maxi_lon])
    red_patch = mpatches.Patch(color='red', label='Node',linewidth=3)
    black_patch = mpatches.Patch(color='black', label='Ways',linewidth=3)
    plt.legend(handles=[red_patch,black_patch]) 
    plt.show()
    return

Map(min_lat=28.6316,min_lon=77.2182, max_lat=28.6341, max_lon=77.2215,area="")
