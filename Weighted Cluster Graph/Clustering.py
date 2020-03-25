# -*- coding: utf-8 -*-
"""
Spyder Editor

Donovan Orn.
"""
#library(Hmisc)
#library(GGally)
#library(sna)
#library(scales)
#library(NISTunits)
import os
import networkx as nx

class WeightedClusterGraph():
    ''' Adds each subject as a node to Graph G.
    
    Parameters
    ----------
    X : Pandas DataFrame
        The data that will be used to create edges in EdgeDefinition
        
    y : iterable
        Resulting variable of the data.
        
    EdgeDefinition : Function of form "Function(G, data_for_edge)"
        Function used to add edges based on desired criteria.
    
    G : Networkx Graph
        The graph nodes will be added to.
        
    Class Variables
    ---------------
    G : Networkx Graph
        The Weighted Graph.
    
    Built in Functions
    ------------------
    DrawGraph(node_color_map, edge_color_map, node_size)
        Saves the weighted graph in Graphs folder. Graphs folder will be created if it does not exist.
    
    convert2Excel()
        Saves an csv file that represents the weighted graph.
        This csv is of the form:
        SOURCE,TARGET,WEIGHT\n
        node,node,weight of edge\n
        ...\n
        ...
        
        Where each row represents the edges.
        (CyptoScape Friendly)
    '''
    
    def __init__(self, X, y, EdgeDefinition, name = 'ClusterGraph'):
        def CreateNodes(G, y):
            for node_name in y:
                G.add_node(str(node_name))        
            return G
        G = nx.Graph()
        G.name = str(name)
        G = CreateNodes(G, y)
        G = EdgeDefinition(G, X)
        self.G = G

    def DrawGraph(self, node_color_map = None, edge_color_map = None,  node_size = 120, folder_extention = ''):
        """ Draws the network graph and saves them to 'Graphs' folder.
        
        Parameters
        ----------
        node_color_map : List of Strings
            contains the color order of the nodes.
            
        edge_color_map : List of Strings
            Contains the color order for each edge.
        
        node_size = 100 : integer
            Size of the nodes in the graphs
            
        """
        import matplotlib.pyplot as plt

        edges = self.G.edges()
        weights = [self.G[u][v]['weight'] * 2 for u, v in edges]
        nx.draw(self.G, pos = nx.kamada_kawai_layout(self.G), node_size = node_size, node_color = node_color_map, edge_color = edge_color_map, width = weights, with_labels = True)
        if not os.path.exists('Graphs/' + str(folder_extention)):
            os.makedirs('Graphs/' + str(folder_extention))
        plt.savefig('Graphs/'  + str(folder_extention) + self.G.name + '_kawai_minTrails.png')
        plt.show()
        
        nx.draw(self.G, pos = nx.spring_layout(self.G), node_size = node_size, node_color = node_color_map, edge_color = edge_color_map, width = weights, with_labels = True)
        plt.savefig('Graphs/'  + str(folder_extention) + self.G.name + '_spring_minTrails.png')
        plt.show()
        
    def convert2Excel(self, name = ''):
        """Saves a csv table file to be converted to Cyptoscape graph."""
        file_string = 'SOURCE,TARGET,WEIGHT\n'
        for edge in self.G.edges():
            source_node = edge[0]
            target_node = edge[1]
            weight = self.G.get_edge_data(edge[0], edge[1])['weight']
            file_string = file_string + str(source_node) + ',' + str(target_node) + ',' + str(weight) + '\n'
        with open(str(name) + self.G.name + '.csv', 'w') as file:
            file.write(file_string)