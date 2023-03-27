import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
import os

data_file = os.path.join(os.path.dirname(__file__), "corr_final_copy.csv")
df = pd.read_csv(data_file)
df.rename(columns = {'mutual' : 'weight'}, inplace = True)
mapping = {True : 'red', False: 'blue'}
df["color"] = df["plus"].map(mapping)
df = df[['node1', 'node2', 'weight', 'color']]

# Make title
st.title('Network Graph Visualization of MST')

# Create networkx graph object for drawing
G = nx.from_pandas_edgelist(df, 'node1', 'node2', ['weight', 'color'])
T = nx.minimum_spanning_tree(G)

# Initiate PyVis network object
defi_net = Network(height='465px', bgcolor='white', font_color='black')

# Take Networkx graph and translate it to a PyVis graph format
defi_net.from_nx(G)

# Generate network with specific layout settings
defi_net.repulsion(node_distance=420, central_gravity=0.33,
                    spring_length=110, spring_strength=0.10,
                    damping=0.95)

# Save and read graph as HTML file (on Streamlit Sharing)
try:
    path = '/tmp'
    defi_net.save_graph(f'{path}/pyvis_graph.html')
    HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

# Save and read graph as HTML file (locally)
except:
    path = '/html_files'
    defi_net.save_graph(f'{path}/pyvis_graph.html')
    HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

# Load HTML file in HTML component for display on Streamlit page
components.html(HtmlFile.read(), height=435)