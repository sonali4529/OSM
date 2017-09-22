#impot osm api
from osmapi import OsmApi
#import time
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D as lines
#to draw barchart import
import NodeBarChart as nodeChart
import WayBarChart as wayChart
import BuildingBarChart as buildingChart
import nodeHistory#for node history
#parameters to write nodes langitudes or latitudes
plat=0
plong=0
f=0
placecount=0
waycount=0
atmcount=0
buildingcount=0
tollcount=0
progress=0

#1 st point ATTRIBUTE COMPLETENESS
#point of interest
mtag=0
www=0#ways with out width
swoh=0#shop without opening hour
wwr=0#worship without relegion
dt=0#drive through
wocuisine=0##places with out amenity details
#geocoding
poi=0# POIS with out details
bmt=0#building missing tags
#Routing and Navigation
nomxsp=0#no max speed tag
nochrg=0# no charge tag in toll
nort=0#railway without crossing tag
nolyr=0# layer tag without bridge or tunnel
start_time = time.time()
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
    global placecount
    global waycount
    global atmcount
    global buildingcount
    global tollcount
    global progress
    global www
    global swoh
    global wwr
    global dt
    global wocuisine
    global mtag
    global nomxsp
    global nochrg
    global nort
    global nolyr
    global poi
    global bmt
    #time is started
    start_time = time.time()
    MyApi=OsmApi()
    result=MyApi.Map(min_lon, min_lat, max_lon, max_lat)#get dataset from OSM website
    nodeChart.drawNodeBarchart(result,plt)#draw bar chart of nodes
    wayChart.drawWayBarchart(result,plt)#draw barchart of ways
    buildingChart.drawBuildingBarchart(result,plt)##draw barchart of building
    #create new figure for map
    fig, ax = plt.subplots()#add labels, title and axes ticks
    ax.ticklabel_format(useOffset=False)
    ax.set_ylabel('Longitude')
    ax.set_xlabel('Latitude')
    ax.set_title(area)
    num=0
    node_num=0
    for rs in result:
        if(rs['type']=="node"):#to print the places
            node_num += 1
            if(len(rs['data']['tag'])==0):#missing tags
                mtag+=1
            if(len(rs['data']['tag'])!=0):#check place is not empty
                nodeHistory.getNodeHistory(int(rs['data']['id']))
                placecount +=1
                #print(rs['data'])
                try:#try if a place has no name
                    key=rs['data']['tag'].keys()
                    if 'building' in key:#check building, atm, and toll tags
                       buildingcount += 1
                       if 'height' not in key or 'building:levels' not in key:
                           bmt+=1
                    if 'atm' in key:
                       atmcount += 1
                    if 'toll' in key:
                       tollcount += 1
                       if 'charge' not in key:#toll without charge
                           nochrg+=1
                    if 'amenity' in key:
                        #place of worship start
                        if(rs['data']['tag']['amenity']=='place_of_worship'):
                            if 'religion' not in key:
                                wwr+=1
                            if 'religion' in key:
                                if(rs['data']['tag']['religion']==''):
                                    wwr+=1
                            if 'name' not in key or 'addr:housenumber' not in key:
                                poi+=1
                        #end place of worship
                        #drive through
                        if(rs['data']['tag']['amenity']=='pharmacy' or rs['data']['tag']['amenity']=='bank' or rs['data']['tag']['amenity']=='atm' or rs['data']['tag']['amenity']=='fast_food' or rs['data']['tag']['amenity']=='post_office'):
                            if 'drive_through' in key :
                                dt+=1
                            if 'name' not in key or 'addr:housenumber' not in key:
                                poi+=1
                        #end drive through
                        #food place
                        if(rs['data']['tag']['amenity']=='fast_food' or rs['data']['tag']['amenity']=='restaurant' or rs['data']['tag']['amenity']=='bar' or rs['data']['tag']['amenity']=='cafe'):
                            if 'cuisine' not in key:
                                wocuisine+=1
                            if 'name' not in key or 'addr:housenumber' not in key:
                                poi+=1
                        #end food place
                    #place which are shop
                    if 'shop' in key:
                        if 'opening_hours' not in key:
                            swoh+=1
                        if 'opening_hours' in key:
                            if(rs['data']['tag']['opening_hours']==''):
                                swoh+=1
                        if 'name' not in key or 'addr:housenumber' not in key:
                                poi+=1
                    detail=""
                    for k in key:
                        detail=detail+k+" - "+rs['data']['tag'][k]+"\n"#collect all information of particular node
                        #print (detail)
                    placesDraw(lat=rs['data']['lat'],long=rs['data']['lon'],name=detail)
                except:
                    print("error")
        elif(rs['type']=="way"):#to print the ways
            num +=1
            if(len(rs['data']['tag'])==0):#missing tags
                mtag+=1
            progress = (num/(len(result)-node_num))*100
            if(len(rs['data']['nd'])!=0):
                waycount += 1
                #print(rs['data'])
                key=rs['data']['tag'].keys()
                if 'building' in key:#check building, atm, and toll tags
                    buildingcount += 1
                if 'atm' in key:
                    atmcount += 1
                if 'toll' in key:
                    tollcount += 1
                    if 'charge' not in key:#toll without charge
                           nochrg+=1
                if 'railway' in key:# check for railway crossing tag
                    if 'crossing' not in key:
                        nort+=1
                if 'layer' in key:# layer wothout tunnel or bridge tag
                    if ('bridge' not in key and 'tunnel' not in key):
                        nolyr+=1
                if 'width' not in key:
                    www+=1
                if 'maxspeed' not in key:
                    nomxsp+=1
                detail=""
                for k in key:
                    detail=detail+k+" - "+rs['data']['tag'][k]+"\n"#collect all information of particular way
                    #print (detail)
                global f
                f=0# a new way is started
                for nd in rs['data']['nd']:
                    getNode(nd,detail)
    #print("Time taken in the Process --- %s seconds ---" % (time.time() - start_time))
    print('1.	General Information on Study Area ')
    print(waycount,'Total ways')
    print(www,'ways with out width')
    print(mtag,'missing tags')
    print('2.	Points-Of-Interest')
    print(swoh,'shop without opening hour')
    print(wwr,'worship without relegion')
    print(dt,'drive through')
    print(wocuisine,'places with out cuisine details')
    print('3.   Geocoding')
    print(poi,'No. of POIs without names and housenumbers ')
    print(bmt,'No. of building with missing tags Height and Levels')
    print('4.   Routing and Navigation')
    print(nomxsp,'no max speed tag')
    print(nochrg,'no charge tag in toll')
    print(nort,'railway without crossing tag')
    print(nolyr,'layer tag without bridge or tunnel')
    progress=100
    return result;

#to draw the places with names
def placesDraw(lat,long,name):
    plt.plot([lat,], [long,], 'ro')
    plt.annotate(name, xy=(lat, long),size=5,color='blue'
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
        plt.annotate(name, xy=(lat, long),size=5,
            )
    elif(f==1):
        plt.plot([plat,lat],[plong,long],color='black')
        plat=lat
        plong=long
    return

#function to get changeset
def getChangset(id):
    #time is started
    start_time = time.time()
    MyApi=OsmApi()
    #print("Changset is  :",MyApi.ChangesetGet(id))
    #print("Time taken in the Process --- %s seconds ---" % (time.time() - start_time))
    return

#function to get Relation for cities or any area
def getRelation(id):
    #time is started
    start_time = time.time()
    MyApi=OsmApi()
    rs=MyApi.RelationGet(id,RelationVersion=-1)
    #print("The relations are : ", rs)
    key=rs['tag'].keys()
    if(len(rs['member'])!=0):
       for member in rs['member']:
           if(member['type']=="way"):
              resultway=getWay(member['ref'])
              nodes=resultway['nd']
              keys=resultway['tag'].keys()
              detail=""
              for k in keys:
                  try:
                      detail=detail+k+" - "+resultway['tag'][k]+"\n"#collect all information of particular way
                  except:
                       print("error")
              #print (detail)
              global f
              f=0# a new way is started
              for nd in nodes:
                  getNode(nd,detail)
           if(member['type']=="node"):
              resultnode=MyApi.NodeGet(memeber['ref'])
              keynode=resultnode['tag'].keys()
              detail=""
              for k in keynode:
                  detail=detail+k+" - "+resultnode['tag'][k]+"\n"#collect all information of particular node
              #print (detail)
              placesDraw(lat=resultnode['lat'],long=resultnode['lon'],name=detail)
    #print("Time taken in the Process --- %s seconds ---" % (time.time() - start_time))
    return rs;

#function to get way
def getWay(id):
    #time is started
    start_time = time.time()
    MyApi=OsmApi()
    #print("The Way are : ", MyApi.WayGet(id,WayVersion=-1))
    ways=MyApi.WayGet(id,WayVersion=-1)
    #print("Time taken in the Process --- %s seconds ---" % (time.time() - start_time))
    return ways;
def read_Progress():
    global progress
    return progress
def draw_graphs(min_lat,max_lat,min_lon, max_lon):
    plt.axis([min_lat,max_lat,min_lon, max_lon])
    red_patch = mpatches.Patch(color='red', label='Node',linewidth=3)
    black_patch = mpatches.Patch(color='black', label='Ways',linewidth=3)
    plt.legend(handles=[red_patch,black_patch]) 
    plt.savefig('Pics/Map.png')
    nodeHistory.graph()
    nodeHistory.plot()
    return
def development(result):
    firstYearn=""
    fyn=0
    secondYearn=""
    syn=0
    thirdYearn=""
    tyn=0
    fourthYearn=""
    fryn=0
    fifthYearn=""
    ffyn=0
    firstYearw=""
    fyw=0
    secondYearw=""
    syw=0
    thirdYearw=""
    tyw=0
    fourthYearw=""
    fryw=0
    fifthYearw=""
    ffyw=0
    for rs in result:
        try:#try if a place has no name
            key=rs['data']['tag'].keys()
            detail=""
            for k in key:
                detail=detail+k+" - "+rs['data']['tag'][k]+", "
        except:
            print("error")
        if(rs['type']=="node"):#to check the places
            if(len(rs['data']['tag'])!=0):#check place is not with empty details
                if(rs['data']['timestamp'].year==2016):
                    fyn +=1
                    firstYearn=firstYearn+"     \n"+str(fyn)+". Position - ("+str(rs['data']['lat'])+","+str(rs['data']['lon'])+"), Info : "+detail+"\n"
                if(rs['data']['timestamp'].year==2015):
                    syn +=1
                    secondYearn=secondYearn+"     \n"+str(syn)+". Position - ("+str(rs['data']['lat'])+","+str(rs['data']['lon'])+"), Info : "+detail+"\n"
                if(rs['data']['timestamp'].year==2014):
                    tyn +=1
                    thirdYearn =thirdYearn+"     \n"+str(tyn)+". Position - ("+str(rs['data']['lat'])+","+str(rs['data']['lon'])+"), Info : "+detail+"\n"
                if(rs['data']['timestamp'].year==2013):
                    fryn +=1
                    fourthYearn=fourthYearn+"     \n"+str(fryn)+". Position - ("+str(rs['data']['lat'])+","+str(rs['data']['lon'])+"), Info : "+detail+"\n"
                if(rs['data']['timestamp'].year==2012):
                    ffyn +=1
                    fifthYearn=fifthYearn+"     \n"+str(ffyn)+". Position - ("+str(rs['data']['lat'])+","+str(rs['data']['lon'])+"), Info : "+detail+"\n"
        if(rs['type']=="way"):#to check the way
             if(len(rs['data']['tag'])!=0):#check place is not with empty details
                if(rs['data']['timestamp'].year==2016):
                    fyw +=1
                    firstYearw=firstYearw+"    "+str(fyw)+". Info : "+detail+"\n"
                if(rs['data']['timestamp'].year==2015):
                    syw +=1
                    secondYearw=secondYearw+"  "+str(syw)+". Info : "+detail+"\n"
                if(rs['data']['timestamp'].year==2014):
                    tyw +=1
                    thirdYearw =thirdYearw+"   "+str(tyw)+". Info : "+detail+"\n"
                if(rs['data']['timestamp'].year==2013):
                    fryw +=1
                    fourthYearw=fourthYearw+"   "+str(fryw)+". Info : "+detail+"\n"
                if(rs['data']['timestamp'].year==2012):
                    ffyw +=1
                    fifthYearw=fifthYearw+"    "+str(ffyw)+". Info : "+detail+"\n"
    if(len(firstYearn)==0):
        firstYearn="No Development in this year"
    if(len(secondYearn)==0):
        secondYearn="No Development in this year"
    if(len(thirdYearn)==0):
        thirdYearn="No Development in this year"
    if(len(fourthYearn)==0):
        fourthYearn="No Development in this year"
    if(len(fifthYearn)==0):
        fifthYearn="No Development in this year"
    if(len(firstYearw)==0):
        firstyearw="No Development in this year"
    if (len(secondYearw)==0):
        secondYearw="No Development in this year"
    if(len(thirdYearw)==0):
        thirdYearw="No Development in this year"
    if(len(fourthYearw)==0):
        fourthYearw="No Development in this year"
    if(len(fifthYearw)==0):
        fifthYearw="No Development in this year"
    dictn={'fn':firstYearn,'sn':secondYearn,'tn':thirdYearn,'frn':fourthYearn,'ffn':fifthYearn,'fw':firstYearw,'sw':secondYearw,'tw':thirdYearw,'frw':fourthYearw,'ffw':fifthYearw}
    key=['www','swoh','wwr','dt','wocuisine','mtag','nomxsp','nochrg','nort','nolyr','poi','bmt','placecount','waycount','buildingcount','atmcount','tollcount']#send all ATTRIBUTE COMPLETENESS dat with development dictionary
    val=[www,swoh,wwr,dt,wocuisine,mtag,nomxsp,nochrg,nort,nolyr,poi,bmt,placecount,waycount,buildingcount,atmcount,tollcount]
    iv=0
    for k in key:
        dictn[k]=val[iv]
        iv+=1
    return dictn#"Developments of Nodes in last Five years"+"\n    Year 2012    \n"+fifthYearn+"\n    Year 2013    \n"+fourthYearn+"\n    Year 2014    \n"+thirdYearn+"\n    Year 2015    \n"+secondYearn+"\n    Year 2016    \n"+firstYearn+"\n\nDevelopments of Ways in last Five years"+"\n    Year 2012    \n"+fifthYearw+"\n    Year 2013    \n"+fourthYearw+"\n    Year 2014    \n"+thirdYearw+"\n    Year 2015    \n"+secondYearw+"\n    Year 2016    \n"+firstYearw
           
#getNode(4725617612);
#getChangset(9906507);
#getRelation(1948585);
#getWay(479479418);
#Map(min_lat=28.5878,min_lon=77.1851, max_lat=28.6278, max_lon=77.2533,area="")
#Map(min_lat=30.8244,min_lon=75.6244, max_lat=31.0000, max_lon=76.0501,area="")
#print("Time taken in the Process --- %s seconds ---" % (time.time() - start_time))
