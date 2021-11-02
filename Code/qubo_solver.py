""" This file contains functions to convert the original qubo to Ising Hamiltonian
and then solve the transformed Ising Hamiltonian by using qiskit."""

from qiskit.optimization.algorithms import MinimumEigenOptimizer
from qiskit.optimization import QuadraticProgram
from qiskit.aqua.algorithms import NumPyMinimumEigensolver, QAOA
from qiskit import BasicAer
from qiskit.aqua import aqua_globals, QuantumInstance

def ising2qubo(qubo_dict):
    """ convert the Ising format to Qubo form.

    Note: The conversion is necessary because we are going to use qiskit to solve
          qubo. qiskit is using CPLEX which Integer variables may be restricted to
          the values 0 (zero) and 1 (one), in which case they are referred
          to as binary variables (SAT problem). The Ising Hamiltonian has spin {-1,1} instead.
          The conversion between qubo and Ising is via using X = (1 - S)/2.
          We can simply replace all the Ising variables by (1 - 2X) to get a new qubo-like equation.
          After the transformation.
          1. The quadratic term will be 4 times bigger.
          2. Each linear term will be 2 times bigger and we have to combine them together.
          3. There will be an offset term.

    Args:
          qubo_dict (list of dict):
          qubo_dict[0]: dict contains linear coef. of the qubo equation.
          qubo_dict[1]: dict contains quadratic coef. of the qubo equation.

    Returns:
          qubo_dict_ising (list of dict): new qubo format.
          qubo_dict_ising[0]: dict contains linear coef. of the converted qubo equation.
          qubo_dict_ising[1]: dict contains quadratic coef. of the converted qubo equation.
          qubo_dict_ising[2]: offset term of the converted qubo equation.
    """
    linear_dict = qubo_dict[0]
    quadratic_dict = qubo_dict[1]
    linear_coef_dict = {}
    offset = 0
    for key, value in linear_dict.items():
        linear_coef_dict[key] = -2 * value
        offset = value * 1 + offset
    for key, value in quadratic_dict.items():
        if key[0] in linear_coef_dict:
            linear_coef_dict[key[0]] = -2 * value + linear_coef_dict[key[0]]
        else:
            linear_coef_dict[key[0]] = -2 * value
        if key[1] in linear_coef_dict:
            linear_coef_dict[key[1]] = -2 * value + linear_coef_dict[key[1]]
        else:
            linear_coef_dict[key[1]] = -2 * value
        offset = offset +  value * 1
    quadratic_dict.update((key, value*4) for key, value in quadratic_dict.items())
    qubo_dict_ising = []
    qubo_dict_ising.append(linear_coef_dict)
    qubo_dict_ising.append(quadratic_dict)
    qubo_dict_ising.append(offset)
    return qubo_dict_ising

def qiskit_qubo_solver(qubo_dict):
    """ solve the transformed qubo using qiskit NumPyMinimumEigensolver.

    Note:  The function calls qiskit NumPyMinimumEigensolver.
           NumPy Eigensolver computes up to the first k eigenvalues of a complex-valued
           square matrix of dimension n×n, with k≤n.
           The idea is to solve the eigen values of the matrices.
           The same problem could be also solved by quantum-like algorithms like QAOA.

    Args:
           qubo_dict (lists of dicts)
           qubo_dict[0]: linear coef. of qubo terms. Like {'X0': 1, 'X1': 2}
           qubo_dict[1]: quadratic coef. of qubo terms. Like {'(X0, X1)': 1, '(X1, X2)': 2}
           qubo_dict[2]: offset terms after the qubo to Ising Hamiltonian conversion.

    Returns:
           results (tuple)
           results[0]: ground state energy of the Ising system.
           results[1]: spin states of the ground state energy in terms of Ising system.

    """
    linear_dict = qubo_dict[0]
    quadratic_dict = qubo_dict[1]
    offset = qubo_dict[2]
    linear_coef = []
    qubo = QuadraticProgram()
    for key, value in linear_dict.items():
        qubo.binary_var(key)
        linear_coef.append(value)
    qubo.minimize(linear=linear_coef, quadratic=quadratic_dict)
    # CLASSICAL METHOD 
    exact_mes = NumPyMinimumEigensolver()
    exact = MinimumEigenOptimizer(exact_mes)
    exact_result = exact.solve(qubo)
    # -------------------------   QAOA        -------------------------- 
    aqua_globals.random_seed = 10598
    quantum_instance = QuantumInstance(BasicAer.get_backend('statevector_simulator'),
                                   seed_simulator=aqua_globals.random_seed,
                                   seed_transpiler=aqua_globals.random_seed)
    qaoa_mes = QAOA(quantum_instance=quantum_instance, initial_point=[0., 0.])
    qaoa = MinimumEigenOptimizer(qaoa_mes)
    qaoa_result = qaoa.solve(qubo)
    # remember to put the offset back.
    exact_ising_result = offset + exact_result.fval
    qaoa_isng_result = offset + qaoa_result.fval
    print("qaoa reult: ")
    qaoa_ising_spin = 1 - 2 * qaoa_result.x
    print(qaoa_isng_result)
    qaoa_ising_spin_sign = []
    for spin in qaoa_ising_spin:
        sign_spin = "+" if spin == 1 else "-"
        qaoa_ising_spin_sign.append(sign_spin)
    print(qaoa_ising_spin_sign)
    # we have to convert the spin from {0, 1} state to {-1, 1} state since
    # we have already convert the qubo to Ising Hamiltonian. X = (1 - S)/2
    exact_ising_spin = 1 - 2 * exact_result.x
    exact_ising_spin_sign = []
    # transform the spins to desired output formats.
    for spin in exact_ising_spin:
        sign_spin = "+" if spin == 1 else "-"
        exact_ising_spin_sign.append(sign_spin)
    results = (exact_ising_result, exact_ising_spin_sign)
    return results
