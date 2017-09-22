import osmnx as ox
from matplotlib import *

G = ox.graph_from_bbox(37.79, 37.78, -122.41, -122.43)
G_projected = ox.project_graph(G)
ox.plot_graph(G_projected,filename='test',save=True,show=False)
