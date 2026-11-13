"""Unit tests for agent-belief-revision-truth-maintenance."""
import unittest
from agent_belief_revision_truth_maintenance.tms import TruthMaintenanceSystem

class TestTruthMaintenanceSystem(unittest.TestCase):
    def setUp(self):
        self.tms = TruthMaintenanceSystem()

    def test_premise_and_derivation(self):
        self.tms.add_premise("A", "Axiom A")
        self.tms.add_premise("B", "Axiom B")
        self.tms.add_derived("C", ["A", "B"], "Conclusion C")
        self.assertTrue(self.tms.is_believed("C"))

    def test_cascade_retraction(self):
        self.tms.add_premise("A", "Fact A")
        self.tms.add_derived("B", ["A"], "Derived B")
        self.tms.add_derived("C", ["B"], "Derived C")
        self.assertTrue(self.tms.is_believed("C"))
        self.tms.retract_premise("A")
        self.assertFalse(self.tms.is_believed("B"))
        self.assertFalse(self.tms.is_believed("C"))

    def test_disjunctive_justifications(self):
        self.tms.add_premise("A", "Fact A")
        self.tms.add_premise("B", "Fact B")
        self.tms.add_derived("C", ["A"], "C via A")
        self.tms.add_derived("C", ["B"], "C via B")
        self.assertTrue(self.tms.is_believed("C"))
        self.tms.retract_premise("A")
        # C should still be believed because B is IN
        self.assertTrue(self.tms.is_believed("C"))

if __name__ == "__main__":
    unittest.main()
