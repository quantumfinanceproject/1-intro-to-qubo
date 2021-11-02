""" Main function to run the solver of qubo optimization problems."""

from tools import read_weights
from qubo_calculation import create_qubo_bfs
from qubo_solver import qiskit_qubo_solver, ising2qubo

CONN_WEIGHT = {} # a dictionary contains the weights information between nodes. 
NUM_NODES = 0
NUM_EDGES = 0
# read input file to get the nodes and weights information
NUM_NODES, NUM_EDGES, CONN_WEIGHT = read_weights('./Code/inputs/qubo_inputs.txt')
# use bfs algorithem to visit the nodes and weights and create qubo object. 
qubo_dict = create_qubo_bfs(CONN_WEIGHT, NUM_NODES)
# transform qubo object to Ising Hamiltonian or vice versa. 
qubo_dict = ising2qubo(qubo_dict)
# the ground state energy is actually the eigen value of the Ising Hamiltonian.
# call the qiskit qaoa and classical qubo solver and print the results. 
results = qiskit_qubo_solver(qubo_dict)
print("classical numerical results:")
print(results[0])
print(''.join(results[1]))
