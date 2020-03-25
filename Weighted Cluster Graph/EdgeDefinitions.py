# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 11:13:09 2020

@author: Donovan
"""

def SpearmansCorrelation(G, data_for_edge):
    """ Finds the similarity of subjects based on Spearmans's Correlation and creates edges.
    
    Parameters
    ----------
    data_for_edge : Pandas DataFrame
        The data used to find similarity.
    
    run_number : Pandas Series
        The run number for each subject.
        
    G : Networkx Graph
        The graph to add edges to.
        
    Returns
    -------
    G : Networkx Graph
        The graph with added edges.
    """
    from scipy.stats import spearmanr
    coeff, p_values = spearmanr(data_for_edge.T)
    for i in range(len(coeff[:,1])): 
        for j in range(len(coeff[1,:])):
            if coeff[i,j]>0.99:
                node1 = list(G.nodes())[i]
                node2 = list(G.nodes())[j]
                if G.has_edge(node1, node2) == False:
                    G.add_edge(node1,node2, weight = 3)
            elif coeff[i,j]>0.975:
                node1 = list(G.nodes())[i]
                node2 = list(G.nodes())[j]
                if G.has_edge(node1, node2) == False:
                    G.add_edge(node1,node2, weight = 2)
            elif coeff[i,j]>.95:
                node1 = list(G.nodes())[i]
                node2 = list(G.nodes())[j]
                if G.has_edge(node1, node2) == False:
                    G.add_edge(node1,node2, weight = 1)
            j += 1
        i += 1
    return G

def CosineSimilarity(G, data_for_edge):
    """ Finds the similarity of subjects based on Cosine and creates edges.
    
    Parameters
    ----------
    data_for_edge : Pandas DataFrame
        The data used to find similarity.
    
    run_number : Pandas Series
        The run number for each subject.
        
    G : Networkx Graph
        The graph to add edges to.
        
    Returns
    -------
    G : Networkx Graph
        The graph with added edges.
    """
    from sklearn.metrics.pairwise import cosine_similarity
    coeff = cosine_similarity(data_for_edge)
    for index1 in range(len(data_for_edge)): 
        for index2 in range(len(data_for_edge)):
            if index1 != index2:
                result = coeff[index1, index2]
                if result > .99:
                    node1 = list(G.nodes())[index1]
                    node2 = list(G.nodes())[index2]
                    if G.has_edge(node1, node2) == False:
                        G.add_edge(node1,node2, weight = 3)
                elif result > 0.98:
                    node1 = list(G.nodes())[index1]
                    node2 = list(G.nodes())[index2]
                    if G.has_edge(node1, node2) == False:
                        G.add_edge(node1,node2, weight = 2)
                elif result > .95:
                    node1 = list(G.nodes())[index1]
                    node2 = list(G.nodes())[index2]
                    if G.has_edge(node1, node2) == False:
                        G.add_edge(node1,node2, weight = 1)
    return G
                