from collections import OrderedDict
from collections import deque

def create_qubo_bfs(Mat, num_nodes):
    """ Generate qubo formula using bfs (breadth first search) algorithm for graph traversal.

    Note:
        The main idea of this function is to generate qubo table for later qiskit qubo solver to consume.
        The "qubo table" which looks like below.

             | X0 | X1 | X2
        ---------------------
        X0   |    |    |
        ---------------------
        X1   |    |    |
        ---------------------
        X2   |    |    |

        This table is symmetric since the weights between nodes are identical in both directions.
        Given a graph with its nodes and edges information, we are able to use bfs to construct this table.
        The output is created following the qiskit qubo solver format. 

    Args:
        Mat (dict): Dictionary contains edges (as value) between two nodes (nodeA, nodeB) as key.
        num_nodes: Number of nodes in the graph.

    Returns:
        qubo_dict (dict) 
        qubo_dict[0]: linear_coef (dict): linear coef. of the qubo of the full graph.
        qubo_dict[1]: quadratic_coef (dict): quadratic coef. of the qubo of the full graph.

    """
    visited = [False] * num_nodes
    linear_coef = OrderedDict() # make sure the ordering is correct starting from root node
    quadratic_coef = {}
    node_q = deque()
    for i in range(num_nodes):
        if not visited[i]:
            node_q.append(i)
            while node_q:
                curr = node_q.popleft()
                visited[curr] = True
                linear_coef["X"+str(curr)] = Mat[(curr, curr)] if (curr, curr) in Mat else 0
                for j in range(curr, num_nodes):
                    if (curr, j) in Mat and (not visited[j]):
                        node_q.append(j)
                        if curr == j:
                            linear_coef["X" + str(curr)] = Mat[(curr, j)]
                        else:
                            quadratic_coef[("X" + str(curr), "X" + str(j))] = Mat[(curr, j)]
    qubo_dict=[]
    qubo_dict.append(linear_coef)
    qubo_dict.append(quadratic_coef)
    return qubo_dict
