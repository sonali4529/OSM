import numpy as np
#draw barchart of nodes
def drawNodeBarchart(resultMap,plt):
    firstyear=0
    secondYear=0
    thirdYear=0
    fourthYear=0
    fifthYear=0
    for rs in resultMap:
        if(rs['type']=="node"):#to check the places
            if(len(rs['data']['tag'])!=0):#check place is not with empty details
                if(rs['data']['timestamp'].year==2016):
                    firstyear += 1
                if(rs['data']['timestamp'].year==2015):
                    secondYear += 1
                if(rs['data']['timestamp'].year==2014):
                    thirdYear += 1
                if(rs['data']['timestamp'].year==2013):
                    fourthYear += 1
                if(rs['data']['timestamp'].year==2012):
                    fifthYear += 1
    N = 5
    node_means = (fifthYear, fourthYear, thirdYear, secondYear, firstyear)

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, node_means, width, color='r',)
    # add  labels, title and axes ticks
    ax.set_ylabel('No. of Nodes')
    ax.set_title('Nodes created in last five Years')
    ax.set_xticks(ind )
    ax.set_xticklabels(('2012', '2013', '2014', '2015', '2016'))
    ax.legend((rects1[0],), ('Nodes',))
    plt.savefig('Pics/node_chart.png')
    return
