"""
OAM-VEST — top-level simulation runner.
Run from the package root directory.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'oam_vest_sim'))
from report import main
if __name__ == "__main__":
    main()
