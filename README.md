# Python Productivity CLI & Time-Box Scheduler

A command-line application designed to manage personal productivity through persistent data tracking, automated meal planning, and constraint-based time scheduling.

This project was built from scratch to demonstrate full CRUD (Create, Read, Update, Delete) operations using native File I/O, state persistence via CSVs, and algorithmic optimization.

## Core Modules

*   **Task Scheduler (Constraint Optimization):** Features a recursive algorithm that acts as a time-box assistant. Users input a free block of time (e.g., 45 minutes), and the algorithm evaluates the to-do list to return the optimal combination of tasks that fit the block based on duration and priority limits.
*   **To-Do List (CRUD operations):** A persistent task manager that parses CSV data into nested Python dictionaries for sorting by priority tier or time estimates, allowing for seamless additions and deletions.
*   **Sleep Tracker (Data Aggregation):** Logs daily sleep hours, automatically enforcing chronological sorting within the CSV. Calculates rolling averages across dynamic, user-defined timeframes.
*   **Menu Planner (Relational Mapping):** Maps days of the week to custom recipes, cross-referencing a persistent ingredient database to automatically generate targeted weekly grocery lists.

## Architecture & Storage
The application utilizes a **Zero-Dependency Architecture**. It relies entirely on Python's standard library, utilizing local `.csv` files as lightweight databases for persistent state management across sessions.

## Usage
Run the main script to enter the interactive CLI loop:
```bash
python main.py
```

From the main menu, navigate using the prompted alphanumeric keys to access the To-Do List, Sleep Tracker, Menu Plan, or Scheduler.

*Note: This repository includes mock `.csv` files containing sample data so the application can be run and tested locally out of the box.*
