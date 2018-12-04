Script for Generating Ulam Cellular Automata according to rules:
  a) it is contiguous to one and only one square of the current generation, and
  b) it touches no other previously occupied square except if the square should be its "grandparent." In addition:
  c) of this set of prospective squares of the (n+1)^{th} generation satisfying the previous condition,
     we eliminate all squares that would touch each other. However, squares that have the same parent are
     allowed to touch.

Further explanation of these rules is given in Mathematical Problems in the Biological Science \cite{bellman62}.

The pattern is called "Maltese Crosses". If a cell would touch some other cell (either already grown or being 
considered for growth in this generation) on either a corner or a side, it is rejected. 
There are two exceptions:
  1) If the cell touches some other cell by virtue of having the same parent.

  2) In the case:
      2*  5*
      1 2345
      2*  5*

    The two starred elements of the fifth generation are 
    allowed to touch potential, though previously rejected, children of the third
    generation. This allows growth to "turn corners". Note that the
    children of the third generation were rejected only because of the
    potential children of the starred members of the second generation.
