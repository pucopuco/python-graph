# Copyright (c) 2007-2008 Pedro Matiello <pmatiello@gmail.com>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


"""
python-graph

A library for working with graphs in Python.
"""


# Module metadata
__authors__ = "Pedro Matiello"
__license__ = "MIT"


# Imports
import searching
import accessibility
import sorting
import minmax
import readwrite


class graph:
	"""
	Graph class.

	Basic operations are defined in this file.
	Algorithms should refer to external files.
	
	@sort: __init__, __len__, __str__, read, write, add_arrow, add_edge, add_nodes, del_arrow, del_edge, get_arrow_weight, get_edge_weight, get_node, get_nodes, has_arrow, has_edge, has_node, accessibility, breadth_first_search, connected_components, depth_first_search, minimal_spanning_tree, mutual_accessibility, shortest_path, topological_sorting
	"""


	def __init__(self):
		"""
		Initialize a graph.
		"""
		self.nodes = {}		# Arrow/Edge lists	(like an adjacency list)
		self.weights = {}	# Arrow/Edge weight list


	def __str__(self):
		"""
		Return a string representing the graph when requested by str() (or print).

		@rtype:  string
		@return: String representing the graph.
		"""
		return "<graph object " + str(self.get_nodes()) + " " + str(self.weights) + ">"


	def __len__(self):
		"""
		Return the size of the graph when requested by len().

		@rtype:  number
		@return: Size of the graph.
		"""
		return len(self.nodes)
	

	def read(self, string, fmt=None):
		"""
		Read a graph from a string. Nodes and arrows specified in the input will be added to the current graph.
		
		@type  string: string
		@param string: Input string specifying a graph.

		@type  fmt: string
		@param fmt: Input format. Possible formats are:
			1. XML (default)
		"""
		readwrite.read(self, string, fmt)	


	def write(self, fmt=None):
		"""
		Write the graph to a string. Depending of the output format, this string can be used by read() to rebuild the graph.
		
		@type  fmt: string
		@param fmt: Output format. Possible formats are:
			1. XML (default)

		@rtype:  string
		@return: String specifying the graph.
		"""
		return readwrite.write(self, fmt)


	def get_nodes(self):
		"""
		Return node list.

		@rtype:  list
		@return: Node list.
		"""
		return self.nodes.keys()


	def get_node(self, node):
		"""
		Return requested node.

		@type  node: *
		@param node: Node identifier

		@rtype:  list
		@return: List of nodes directly accessible from given node.
		"""
		return self.nodes[node]


	def has_node(self, node):
		"""
		Return whether the requested node exists.

		@type  node: node
		@param node: Node identifier

		@rtype:  boolean
		@return: Truth-value for node existence.
		"""
		return self.nodes.has_key(node)


	def add_nodes(self, nodelist):
		"""
		Add given nodes to the graph.
		
		@attention: While nodes can be of any type, it's strongly recommended to use only numbers and single-line strings has node identificators if you intend to use write().

		@type  nodelist: list
		@param nodelist: List of nodes to be added to the graph.
		"""
		for each in nodelist:
			self.nodes[each] = []


	def add_edge(self, u, v, wt=1):
		"""
		Add an edge (u,v) to the graph connecting nodes u and v.

		@attention: This function should not be used in directed graphs: use add_arrow() instead.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.
		
		@type  wt: number
		@param wt: Edge weight.
		
		"""
		if (v not in self.nodes[u]):
			self.nodes[u].append(v)
			self.nodes[v].append(u)
			self.weights[(u, v)] = wt
			self.weights[(v, u)] = wt


	def add_arrow(self, u, v, wt=1):
		"""
		Add an arrow (u,v) to the directed graph connecting node u to node v.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.

		@type  wt: number
		@param wt: Arrow weight.
		"""
		if (v not in self.nodes[u]):
			self.nodes[u].append(v)
			self.weights[(u, v)] = wt


	def del_edge(self, u, v):
		"""
		Remove an edge (u, v) from the graph.

		@attention: This function should not be used in directed graphs: use del_arrow() instead.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.
		"""
		if (v in self.nodes[u]):
			self.nodes[u].remove(v)
			self.nodes[v].remove(u)
			del(self.weights[(u,v)])
			del(self.weights[(v,u)])


	def del_arrow(self, u, v):
		"""
		Remove an arrow (u, v) from the directed graph.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.
		"""
		if (v in self.nodes[u]):
			self.nodes[u].remove(v)
			del(self.weights[(u,v)])


	def get_arrow_weight(self, u, v):
		"""
		Get the weight of an arrow.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.
		
		@rtype:  number
		@return: Arrow weight
		"""
		return self.weights[(u, v)]


	def get_edge_weight(self, u, v):
		"""
		Get the weight of an arrow.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.
		
		@rtype:  number
		@return: Edge weight
		"""
		return self.weights[(u, v)]


	def has_arrow(self, u, v):
		"""
		Return whether an arrow from node u to node v exists.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.

		@rtype:  boolean
		@return: Truth-value for arrow existence.
		"""
		return self.weights.has_key((u,v))


	def has_edge(self, u, v):
		"""
		Return whether an edge between nodes u and v exists.

		@type  u: node
		@param u: One node.

		@type  v: node
		@param v: Other node.

		@rtype:  boolean
		@return: Truth-value for edge existence.
		"""
		return self.weights.has_key((u,v)) and self.weights.has_key((v,u))


	def depth_first_search(self, root=None):
		"""
		Depht-first search.
		
		@type  root: node
		@param root: Optional root node (will explore only root's connected component)

		@rtype:  tuple
		@return:  tupple containing a dictionary and two lists:
			1. Generated spanning tree
			2. Graph's preordering
			3. Graph's postordering
		"""
		return searching.depth_first_search(self, root)


	def breadth_first_search(self, root=None):
		"""
		Breadth-first search.

		@type  root: node
		@param root: Optional root node (will explore only root's connected component)

		@rtype:  dictionary
		@return: Generated spanning_tree
		"""
		return searching.breadth_first_search(self, root)


	def accessibility(self):
		"""
		Accessibility matrix (transitive closure).

		@rtype:  dictionary
		@return: Accessibility information for each node.
		"""
		return accessibility.accessibility(self)


	def mutual_accessibility(self):
		"""
		Mutual-accessibility matrix (strongly connected components).

		@rtype:  list
		@return: Mutual-accessibility information for each node.
		"""
		return accessibility.mutual_accessibility(self)


	def topological_sorting(self):
		"""
		Topological sorting.

		@attention: Topological sorting is meaningful only for directed acyclic graphs.

		@rtype:  list
		@return: Topological sorting for the graph.
		"""
		return sorting.topological_sorting(self)


	def connected_components(self):
		"""
		Connected components.

		@attention: Indentification of connected components is meaningful only for non-directed graphs.

		@rtype:  dictionary
		@return: Pairing that associates each node to its connected component.
		"""
		return accessibility.connected_components(self)


	def minimal_spanning_tree(self):
		"""
		Minimal spanning tree.

		@attention: Minimal spanning tree meaningful only for weighted graphs.

		@rtype:  list
		@return: Generated spanning tree.
		"""
		return minmax.minimal_spanning_tree(self)


	def shortest_path(self, source):
		"""
		Return the shortest path distance between source node and all other nodes using Dijkstra's algorithm.
		
		@attention: All weights must be nonnegative.

		@type  source: node
		@param source: Node from which to start the search.

		@rtype:  tuple
		@return: A tuple containing two dictionaries, each keyed by target nodes.
			1. Shortest path spanning tree (each key points to previous node in the shortest path transversal).
			2. Shortest distance from given source to each target node.
		Inaccessible target nodes do not appear in either dictionary.
		"""
		return minmax.shortest_path(self, source)
