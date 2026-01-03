# Password Hashing Security Demonstration

## Overview
This project is a Python-based educational tool designed to demonstrate the comparative security of various password hashing algorithms. It simulates a "data breach" scenario where a security analyst attempts to recover passwords from a compromised database using a dictionary attack.

The tool benchmarks the computational cost (time and resources) required to crack legacy algorithms (MD5, SHA1) versus modern, memory-hard algorithms (Argon2, Bcrypt), effectively illustrating why modern applications must use slow, resource-intensive hashing functions.

## Features
- **Multi-Algorithm Comparison:** Simulates attacks against MD5, SHA1, SHA256 (Unsalted), SHA256 (Salted), Bcrypt, and Argon2.
- **Real-time Benchmarking:** Measures the exact time and attempts required to crack each hash.
- **Attack Simulation:** Implements a dictionary attack using a custom wordlist.
- **Statistical Analysis:** Provides a summary comparing the speed (hashes/second) of each algorithm.
- **Progress Tracking:** Visual progress bars for long-running processes.

## Prerequisites
- Python 3.8 or higher
- `pip` (Python package installer)

## Installation & Setup

1. **Clone or Download the Repository**
   Extract the files to your local machine.

2. **Create a Virtual Environment**
   It is recommended to run this project in an isolated environment.
   
   *Windows:*
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   *Linux/Mac:*
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Script**
   ```bash
   python databreach.py
   ```

