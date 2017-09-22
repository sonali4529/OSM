import numpy as np
#draw way barchart
def drawBuildingBarchart(resultMap,plt):
    firstyear=0
    secondYear=0
    thirdYear=0
    fourthYear=0
    fifthYear=0
    for rs in resultMap:
        key=rs['data']['tag'].keys()
        if 'building' in key:#check building
            if(rs['data']['timestamp'].year==2016):#check year of creation of ways
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
    rects1 = ax.bar(ind, node_means, width, color='green',)
    # add labels, title and axes ticks
    ax.set_ylabel('No. of Buildings')
    ax.set_title('Building created in last five Years')
    ax.set_xticks(ind )
    ax.set_xticklabels(('2012', '2013', '2014', '2015', '2016'))
    ax.legend((rects1[0],), ('Building',))
    plt.savefig('Pics/building_chart.png')
    return
