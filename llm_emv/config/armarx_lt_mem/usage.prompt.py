Usage examples:
>>> history.expand()  # Shows the history tree with all child nodes expanded
>>> history.expand(date(2021, 12, 20))  # Expand the children that overlap with the given day
>>> history.expand(now() - timedelta(hours=6), now() - timedelta(hours=4))  # Expand all children that overlap with the given range (in this example "about 5 hours ago")
>>> history.expand((now() - timedelta(days=2)).date())  # Expand all children that overlap with the day before yesterday
>>> history[0].expand()  # Shows child node 0 with all its child nodes expanded
>>> history[5][2].expand()  # Shows child node 2 of child node 5 with all its child nodes expanded
>>> history.search("green cup") # Semantic index search. Expands the most relevant children according to similarity of the natural language query and the node's (recursively defined) index content.
>>> history[1][42].search("bicycle") # Semantic index search on some node further down the tree. Expands the children of node 1.42 most relevant to the search term
>>> history[3].collapse_all_but(1); history[3][1].expand()  # Zooms into details of child node 3.1 while collapsing all other childs of node 3
>>> vqa("What color is the ... in this image?",
...     history[2][4][-1][0].image)  # Invoke a model to answer a visual question about image(s) of low-level (action, scene) node(s). Use this if the question asks for details not contained in the history tree, but likely evident from the images.

# After gathering the relevant information, answer the question:
# Optionally, provide a reasoning on why you choose the respective answer
>>> answer(reasoning="...", answer="...")
