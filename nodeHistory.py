#impot osm api
from osmapi import OsmApi
import matplotlib.pyplot as plt
import numpy as np
#import time
import time
start_time = time.time()
tagfirst=0
tagsecond=0
tagthird=0
tagfourth=0
tagfifth=0
tagsixth=0
nodefirst=0
nodesecond=0
nodethird=0
nodefourth=0
nodefifth=0
nodesixth=0
#function to read node
avgtagfirst=0
avgtagsecond=0
avgtagthird=0
avgtagfourth=0
avgtagfifth=0
avgtagsixth=0
def getNodeHistory(id) :
    global tagfirst
    global tagsecond
    global tagthird
    global tagfourth
    global tagfifth
    global tagsixth
    global nodefirst
    global nodesecond
    global nodethird
    global nodefourth
    global nodefifth
    global nodesixth
    #time is started
    start_time = time.time()
    MyApi=OsmApi()
    nodeHistory=MyApi.NodeHistory(id)
    for version in nodeHistory.keys():
        user = nodeHistory[version]['user']
        version = int(nodeHistory[version]['version'])
        id=nodeHistory[version]['id']
        if(version == 1):
            if(len(nodeHistory[version]['tag'])!= 0):
                tagfirst +=len(nodeHistory[version]['tag'])
            nodefirst +=1
        if(version == 2):
            if(len(nodeHistory[version]['tag'])!= 0):
                tagsecond +=len(nodeHistory[version]['tag'])
            nodesecond +=1
        if(version == 3):
            if(len(nodeHistory[version]['tag'])!= 0):
                tagthird +=len(nodeHistory[version]['tag'])
            nodethird +=1
        if(version == 4):
            if(len(nodeHistory[version]['tag'])!= 0):
                tagfourth +=len(nodeHistory[version]['tag'])
            nodefourth +=1
        if(version == 5):
            if(len(nodeHistory[version]['tag'])!= 0):
                tagfifth +=len(nodeHistory[version]['tag'])
            nodefifth +=1
        if(version == 6):
            if(len(nodeHistory[version]['tag'])!= 0):
                tagsixth +=len(nodeHistory[version]['tag'])
            nodesixth +=1
    return
def printDetails():
    global avgtagfirst
    global avgtagsecond
    global avgtagthird
    global avgtagfourth
    global avgtagfifth
    global avgtagsixth
    try:
        avgtagfirst = tagfirst/nodefirst
        avgtagsecond = tagsecond/nodesecond
        avgtagthird = tagthird/nodethird
        avgtagfourth = tagfourth/nodefourth
        avgtagfifth = tagfifth/nodefifth
        avgtagsixth = tagsixth/nodesixth
    except:
        print()
    #print('tagfirst',tagfirst)
    #print('tagsecond',tagsecond)
    #print('tagthird',tagthird)
    #print('tagfourth',tagfourth)
    #print('tagfifth',tagfifth)
    #print('tagsixth',tagsixth)
    #print('nodefirst',nodefirst)
    #print('nodesecond',nodesecond)
    #print('nodethird',nodethird)
    #print('nodefourth',nodefourth)
    #print('nodefifth',nodefifth)
    #print('nodesixth',nodesixth)
    #print('avgtagfirst',avgtagfirst)
    #print('avgtagsecond',avgtagsecond)
    #print('avgtagthird',avgtagthird)
    #print('avgtagfourth',avgtagfourth)
    #print('avgtagfifth',avgtagfifth)
    #print('avgtagsixth',avgtagsixth)
    #print("Time taken in the Process --- %s seconds ---" % (time.time() - start_time))
    return
def graph():
    N = 6
    node_means = (nodefirst,nodesecond,nodethird,nodefourth,nodefifth,nodesixth
                  )
    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects = ax.plot(ind, node_means, color='c',linewidth=3.3,)
    ax.set_ylabel('number of nodes')
    ax.set_title('Number of nodes in each version')
    ax.set_xticks(ind )
    ax.set_xticklabels(('Version 1', 'Version 2', 'Version 3', 'Version 4', 'Version 5','Version 6'))
    plt.savefig('Pics/node_number_version.png')
    return

def plot():
    printDetails()
    N = 6
    node_means = (avgtagfirst,avgtagsecond,avgtagthird,avgtagfourth,avgtagfifth,avgtagsixth)

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects = ax.bar(ind, node_means, width, color='0.75',)
    # add labels, title and axes ticks
    ax.set_ylabel('Mean number of tags')
    ax.set_title('Nodes history version Details')
    ax.set_xticks(ind )
    ax.set_xticklabels(('Version 1', 'Version 2', 'Version 3', 'Version 4', 'Version 5','Version 6'))
    plt.savefig('Pics/history_chart.png')
    return
getNodeHistory(4725617612);

