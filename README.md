# Quantum Finance Project

## Introduction To QUBO : Meetup Resources

This repository contains a copy of the presentation as well as the code which was presented at the first [Quantum Finance Project](https://www.meetup.com/quantumfinance/) meetup held on 21 October 2021, entitled [Introduction to QUBO](https://www.meetup.com/quantumfinance/events/280596537/) and presented by ChingCheng Hsu.

## Presentation

The presentation was given remotely, using a Jupyter notebook to display the slides and illustrate some results during the talk.  The notebook is provided at this repo in the `Presentation` folder.

## Code

The presentation involved also the discussion and demonstration of a QUBO solving method implemented in Python.  The code and some sample input files are contained in the `Code` directory of this repo.

### Prerequisites

- Python 3.9+

### Running the code

- Install required packages  
  ```
  pip install -r requirements.txt
  ```
- Run the main script
  ```python
  cd Code
  python qubo_main.py
  ```
- Update or add input files in `Code/inputs`, and change the input file in use by updating the filename passed to `read_weights` in line 11 of qubo_main.py.