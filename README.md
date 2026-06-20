# Critical Care Optimisation: Hospital Efficiency Data Structure and Algorithms Optimisation (COMP5008 Final Assignment)

## Overview

This project implements a hospital resource management system using fundamental data structures and algorithms. The system simulates hospital operations including patient record management, department navigation, emergency scheduling, and performance reporting.

Developed for **COMP5008 – Data Structures and Algorithms**, Curtin University.

## Technologies Used

* Python 3
* Object-Oriented Programming (OOP)
* Graph Algorithms (BFS, DFS, A*)
* Hash Tables
* Binary Heaps
* Merge Sort and Quick Sort

## Project Modules

### Module 1 – Hospital Navigation

* Graph implementation using adjacency lists
* Breadth-First Search (BFS)
* Depth-First Search (DFS)
* A* Shortest Path Algorithm

### Module 2 – Patient Lookup

* Custom hash table implementation
* Patient record insertion, search, and deletion
* Collision handling and load factor analysis

### Module 3 – Emergency Scheduling

* Max Heap implementation
* Priority-based patient scheduling
* Heap insertion and extraction operations

### Module 4 – Patient Record Sorting

* Merge Sort
* Quick Sort
* Performance benchmarking and comparison

# Instrcutions to run the program for the assignment on Critical Care Optimisation: Hospital Efficiency Data Structure and Algorithms Optimisation


mod1.py	- Implements hospital layout using a weighted graph. Supports BFS, DFS, and A* algorithms for pathfinding between departments.

mod2.py	- Builds a hash table with chaining to store and retrieve patient records efficiently.

mod3.py - Uses a max-heap to prioritise patient treatments based on urgency and treatment time.

mod4.py	- Compares Merge Sort and Quick Sort algorithms on patient records for performance reporting.

case../	Contains demo input files for each module (e.g., department graphs, patient lists, request files, etc.). Also, Each module writes its processed results, logs, and timing summaries here.


## How to run: 
In order to run the python files, you need to run each module seperately. For example, python3 mod1.py


You’ll be prompted to enter an input file name, or press Enter to use a default demo input. For eaxmple, in case of 

Module 1 – Graph (Weighted, Undirected):
=========================================

Input Files: case1_full_spec.txt, case2_no_coords.txt, etc.

Purpose: Models hospital departments and corridors.

Algorithms: BFS, DFS, and A* (Manhattan heuristic) for route optimisation.

Outputs: output_graph.txt, output_bfs.txt, output_dfs.txt, output_astar.txt.



Module 2 – Hash Table (Chaining):
==================================

Input Files: m2_case1_basic.txt to m2_case4_collide_update.txt.

Purpose: Stores and retrieves patient details via custom hashing.

Outputs: m2_log.txt, m2_collisions.txt, m2_summary.txt.



Module 3 – Heap Scheduler (Emergency Queue):
==============================================

Input Files: patients_caseX.txt and requests_caseX.txt.

Purpose: Uses a Max-Heap to allocate patients based on urgency (U) and treatment time (T).

Outputs: m3_heap_trace.txt, m3_priority_log.txt, m3_summary.txt.



Module 4 – Sorting (Merge vs Quick Sort):
=============================================

Input File: m4_experiments.txt

Purpose: Compares Merge Sort (stable) and Quick Sort (median-of-three) on patient record datasets.

Outputs:

m4_timing_summary.txt – runtime measurements

m4_opcounts.txt – comparison and move counts

sorted_merge_*.txt and sorted_quick_*.txt – sorted outputs for each dataset



Dataset Types: random, nearly sorted, and reversed arrays.

Final version: 27 October, 2025


## Learning Outcomes

This project demonstrates the practical application of:

* Graph traversal and pathfinding
* Efficient data retrieval using hashing
* Priority queue scheduling using heaps
* Sorting algorithm analysis and benchmarking

## Author

Abu Fatah Mohammed Faisal

Curtin University

Master of Predictive Analytics
