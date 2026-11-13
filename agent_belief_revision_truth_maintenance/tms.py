"""Justification-based Truth Maintenance System (JTMS)."""
from enum import Enum
from typing import Dict, List, Set, Optional, Tuple, Any

class BeliefStatus(str, Enum):
    IN = "IN"    # Believed to be true
    OUT = "OUT"  # Not believed / retracted

class BeliefNode:
    def __init__(self, node_id: str, is_premise: bool = False, label: str = ""):
        self.node_id = node_id
        self.is_premise = is_premise
        self.label = label or node_id
        self.status = BeliefStatus.IN if is_premise else BeliefStatus.OUT
        self.antecedents: List[List[str]] = []  # List of justification sets (conjunctions)
        self.consequents: Set[str] = set()

class TruthMaintenanceSystem:
    """Maintains consistent dependency networks and cascades belief retractions."""

    def __init__(self):
        self.nodes: Dict[str, BeliefNode] = {}

    def add_premise(self, node_id: str, label: str = "") -> BeliefNode:
        node = BeliefNode(node_id, is_premise=True, label=label)
        self.nodes[node_id] = node
        return node

    def add_derived(self, node_id: str, antecedents: List[str], label: str = "") -> BeliefNode:
        if node_id not in self.nodes:
            self.nodes[node_id] = BeliefNode(node_id, is_premise=False, label=label)
        node = self.nodes[node_id]
        node.antecedents.append(antecedents)

        for ant_id in antecedents:
            if ant_id in self.nodes:
                self.nodes[ant_id].consequents.add(node_id)

        self._recompute_node(node_id)
        return node

    def retract_premise(self, node_id: str):
        node = self.nodes.get(node_id)
        if not node or not node.is_premise:
            return
        node.status = BeliefStatus.OUT
        self._cascade_retraction(node_id)

    def _cascade_retraction(self, node_id: str):
        node = self.nodes.get(node_id)
        if not node:
            return
        for cons_id in list(node.consequents):
            self._recompute_node(cons_id)

    def _recompute_node(self, node_id: str):
        node = self.nodes.get(node_id)
        if not node or node.is_premise:
            return

        # A derived node is IN if AT LEAST ONE of its justification sets has ALL antecedents IN
        was_in = (node.status == BeliefStatus.IN)
        now_in = False
        for just_set in node.antecedents:
            if all(self.nodes.get(ant) and self.nodes[ant].status == BeliefStatus.IN for ant in just_set):
                now_in = True
                break

        node.status = BeliefStatus.IN if now_in else BeliefStatus.OUT

        # If status changed, recursively recompute consequents
        if was_in != now_in:
            for cons_id in list(node.consequents):
                self._recompute_node(cons_id)

    def is_believed(self, node_id: str) -> bool:
        node = self.nodes.get(node_id)
        return bool(node and node.status == BeliefStatus.IN)
