""" This file contains useful functions for reading the textfile"""


from itertools import dropwhile

def is_comment(sentence):
    """ function to check if a line starts with c. This starts the comment line.

    Args:
        sentence (str): input string.

    Returns:
        True if sentence startswith 'c'.
    """
    # return true if a line starts with #
    return sentence.startswith('c')

def is_problem(sentence):
    """  function to check if a line starts with I(Ising) or Q(QUBO). This starts the data file.

    Args:
        sentence (str): input string.

    Returns:
        True if sentence startswith 'I' or 'Q'.

    """
    # return true if a line starts with #
    return sentence.startswith('I')

def read_weights(textfile):
    """  read the text file and do the sanity check of the inputs.

    Args:
        textfile (str): filename of the text file.

    Returns:
        num_nodes (int): numbers of nodes specified in the textfile
        num_edges (int): numbers of the edges specified in the textfile
        conn_weight (dict): dictionary about the edges (value) between \
                two nodes tuple (nodeA, nodeB) as key.

    """
    num_nodes = 0
    num_edges = 0
    conn_weight = {}
    with open(textfile) as problem_file:
        for curline in dropwhile(is_comment, problem_file):
            if is_problem(curline) and len(curline.split(' ')) == 4:
                num_nodes = int(curline.rstrip('\n').split(' ')[2])
                num_edges = int(curline.rstrip('\n').split(' ')[3])
            else:
                node_a = int(curline.rstrip('\n').split(' ')[0])
                node_b = int(curline.rstrip('\n').split(' ')[1])
                # change the node order if node_a > mode_b because it is undirected graph.
                if node_a > node_b:
                    node_a, node_b = node_b, node_a 
                weight = int(curline.rstrip('\n').split(' ')[2])
                conn_weight[(node_a, node_b)] = weight
    return num_nodes, num_edges, conn_weight
