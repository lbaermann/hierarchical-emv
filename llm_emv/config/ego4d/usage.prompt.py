Usage examples:
>>> history.expand()  # Shows the history tree with all child nodes expanded
>>> history.expand(date(2021, 12, 20))  # Expand the children that overlap with the given day
>>> history.expand(now() - timedelta(hours=6), now() - timedelta(hours=4))  # Expand all children that overlap with the given range (in this example "about 5 hours ago")
>>> history.expand((now() - timedelta(days=2)).date())  # Expand all children that overlap with the day before yesterday
>>> history[0].expand()  # Shows child node 0 with all its child nodes expanded
>>> history.search("green booklet") # Semantic index search. Expands the most relevant children according to similarity of the natural language query and the node's (recursively defined) index content.
>>> history[1].search("riding the bike") # Semantic index search on some node further down the tree. Expands the children of node 1 most relevant to the search term
>>> history[1][12].search("riding the bike"); history[1][42].search("riding the bike") # Semantic index search on some nodes further down the tree
>>> history[3].collapse_all_but(1); history[3][1].expand()  # Zooms into details of child node 3.1 while collapsing all other childs of node 3
>>> history[5][2].collapse_all_but(4); history[5][2][4].expand()  # Zooms into details of child node 5.2.4 while collapsing all other childs of node 5.2
>>> vqa("What color is the ... in these images?",
...     history[2][4][-1][0].image, history[2][4][-1][3].image)  # Invoke a model to answer a visual question about one or more images of low-level (action, scene) node(s). Use this if the question asks for details not contained in the history tree, but likely evident from the image(s).

# After gathering the relevant information, answer the question:
# Optionally, provide a reasoning on why you choose the respective answer
>>> answer(reasoning="...", answer="...")