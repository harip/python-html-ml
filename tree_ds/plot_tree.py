# https://matplotlib.org/gallery/shapes_and_collections/artist_reference.html?highlight=matplotlib%20pyplot%20hsv

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import numpy as np

class PlotTree:
    def __init__(self,config={}):
        plt.rcdefaults()
        self.fig, self.ax = plt.subplots()
        self.grid = None
        self.patches = []
        self.tree = None
        self.plotted = dict()
        self.config=config

    def label(self, label_xy, text):
        plt.text(label_xy[0], label_xy[1], text, ha="center", family='sans-serif', size=9)

    def get_arrow(self, start_loc, end_loc):
        return mpatches.Arrow( start_loc[0],
                                start_loc[1],
                                end_loc[0]-start_loc[0],
                                end_loc[1]-start_loc[1],
                                width=0.1)

    def set_mgrid(self):
        # Get number of paths, this will determine the width of the plot/grid
        num_of_paths = len(self.tree.paths) 

        # Get the height of the tree, this will determine the height of the plot
        max_node_path = self.tree.height+1

        # Create grid
        grid_size_y = complex(0, max_node_path)
        grid_size_x = complex(0, num_of_paths)
 
        x = 0
        y = num_of_paths*0.2
        self.grid = np.mgrid[x:y:grid_size_x, x:y:grid_size_y].reshape(2, -1).T
        self.grid = self.grid[::-1]

        if "show_grid" in self.config and self.config["show_grid"]==True:
            self.display_grid()

    def display_grid(self):
        plt.plot(self.grid[:,0], self.grid[:,1], 'ro')

    def arrange_paths(self):
        path_tuple=[(k,"-".join([self.tree.node_belongs_to_path[nv].Node.id for nv in v]))  for k,v in self.tree.paths.items()]
        path_tuple=sorted(path_tuple,key=lambda x:x[1])
        self.tree.paths=dict((tup[0],self.tree.paths[tup[0]]) for tup in path_tuple)

    def set_plot(self):
        colors = np.linspace(0, 1, len(self.patches))
        collection = PatchCollection(self.patches, cmap=plt.cm.hsv, alpha=0.3)
        # collection.set_array(np.array(colors))
        self.ax.add_collection(collection)
        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def get_node_plot_pos(self):
        path_counter=0
        path_node_counter=0
        arrange_nodes=[]

        # k is the key, path name
        # v is the list of nodes in the path
        for k,v in self.tree.paths.items():
            node_pos_in_path=0
            for j in v:      
                node = self.tree.node_belongs_to_path[j].Node
                arrange_nodes.append((node,path_node_counter))

                # Make a note of which nodes have been plotted on the chart
                path_node_counter = path_node_counter+1
                node_pos_in_path=node_pos_in_path+1                

            # New path always starts from the top, all paths are not of same height
            path_counter = path_counter+1
            path_node_counter = (self.tree.height+1)*path_counter

        # get uniq 
        node_ids=set(t[0].id for t in arrange_nodes)

        # get all the grid locations for a node_id
        node_pos=dict()
        for node_id in node_ids:
            node_grid_pos=[a_nodes[1] for a_nodes in arrange_nodes if a_nodes[0].id==node_id]
            node_plot_count=len(node_grid_pos)

            x=self.grid[node_grid_pos[0]][0]
            y=self.grid[node_grid_pos[0]][1]
            if node_plot_count>1:
                # calculate the middle, only consider x values
                end_x=self.grid[ node_grid_pos[node_plot_count-1]][0]
                center_x=(x+end_x)/2                
                node_pos[node_id]=(center_x,y)
            else:
                node_pos[node_id]=(x,y)
                
        return node_pos

    def plot_tree(self, treeds):
        self.tree = treeds
        self.arrange_paths()        
        self.set_mgrid()        
        node_h=0.5
        node_w=2*node_h
        prev_node_loc_center=[]
 
        node_plot_pos_mod=self.get_node_plot_pos()
        plotted_node=dict()

        # k is the key, path name
        # v is the list of nodes in the path
        for k,v in self.tree.paths.items():
            node_pos_in_path=0
            for j in v:                           
                node = self.tree.node_belongs_to_path[j].Node
                center_xy=[node_plot_pos_mod[node.id][0],node_plot_pos_mod[node.id][1] ]

                if j not in plotted_node :
                    # ellipse = mpatches.Ellipse(center_xy, node_w, node_h,color='r')
                    # self.patches.append(ellipse)            
                    self.label(center_xy, node.node_key)     

                # Draw arrow
                if node_pos_in_path != 0:
                    arrow = self.get_arrow(prev_node_loc_center,center_xy)
                    self.patches.append(arrow)

                # Make a note of which nodes have been plotted on the chart
                plotted_node[j]=True 
                prev_node_loc_center=center_xy
                node_pos_in_path=node_pos_in_path+1   

        self.set_plot()        

    def plot_paths(self, treeds):
        self.tree = treeds
        self.arrange_paths()        
        self.set_mgrid()
        node_w=0.2 
        path_counter=0
        path_node_counter=0
        prev_node_loc=0
 
        plotted_node=dict()

        # k is the key, path name
        # v is the list of nodes in the path
        for k,v in self.tree.paths.items():
            node_pos_in_path=0
            for j in v:              

                # Draw ellipse
                ellipse = mpatches.Ellipse(self.grid[path_node_counter], node_w, 0.1)
                self.patches.append(ellipse)

                # Get text of node
                node = self.tree.node_belongs_to_path[j].Node
                self.label(self.grid[path_node_counter], node.node_key)

                # Draw arrow
                if node_pos_in_path != 0:
                    arrow = self.get_arrow( self.grid[prev_node_loc],
                                            self.grid[path_node_counter])
                    self.patches.append(arrow)

                # Make a note of which nodes have been plotted on the chart
                plotted_node[j]=path_node_counter
                prev_node_loc=path_node_counter
                path_node_counter = path_node_counter+1
                node_pos_in_path=node_pos_in_path+1                

            # New path always starts from the top, all paths are not of same height
            path_counter = path_counter+1
            path_node_counter = (self.tree.height+1)*path_counter

        self.set_plot()
        