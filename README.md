Script for Generating Ulam Cellular Automata according to rules:
  a) it is contiguous to one and only one square of the current generation, and
  b) it touches no other previously occupied square except if the square should be its "grandparent." In addition:
  c) of this set of prospective squares of the (n+1)^{th} generation satisfying the previous condition,
     we eliminate all squares that would touch each other. However, squares that have the same parent are
     allowed to touch.

