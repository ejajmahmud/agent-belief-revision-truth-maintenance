"""CLI for agent-belief-revision-truth-maintenance."""
import sys
import argparse
from .tms import TruthMaintenanceSystem

def main():
    parser = argparse.ArgumentParser(description="Agent Belief Revision Truth Maintenance CLI")
    parser.add_argument("--demo", action="store_true", help="Run JTMS belief retraction demo")
    args = parser.parse_args()

    if args.demo:
        tms = TruthMaintenanceSystem()
        tms.add_premise("P1", "User is Pro Tier")
        tms.add_premise("P2", "Server has GPU capacity")
        tms.add_derived("D1", ["P1", "P2"], "Enable 4K stream")
        tms.add_derived("D2", ["D1"], "Allocate High-VRAM Cluster")
        print(f"[+] Initial state: D2 believed = {tms.is_believed('D2')}")
        print("[*] Retracting Premise P1 (User downgraded)...")
        tms.retract_premise("P1")
        print(f"[+] After retraction: D1 believed = {tms.is_believed('D1')}, D2 believed = {tms.is_believed('D2')}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
