# show working directory
import os
import sys

# Show working directory
print("Working directory before changing:", os.getcwd())


# Set the working directory to the root of your project
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)

# Add the project root to the Python path
sys.path.append(project_root)

# Show working directory after changing
print("Working directory after changing:", os.getcwd())

# Print the Python path
print("Python path:", sys.path)

# Attempt to import the module
try:
    from PyCarPlt.tire2d import *
    print("Import successful")
except Exception as e:
    print("Import failed:", e)
