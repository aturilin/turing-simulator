"""Core Turing Machine implementation."""

from dataclasses import dataclass, field
from typing import Optional
import copy


@dataclass
class MachineState:
    """Represents the complete state of a Turing machine at a point in time."""
    tape: dict[int, str]
    head_position: int
    current_state: str
    halted: bool
    accepted: bool
    step_count: int


class TuringMachine:
    """A Turing machine simulator with infinite tape in both directions."""

    def __init__(self):
        self.tape: dict[int, str] = {}
        self.head_position: int = 0
        self.current_state: str = ""
        self.initial_state: str = ""
        self.accept_states: set[str] = set()
        self.reject_states: set[str] = set()
        self.blank_symbol: str = "_"
        self.transitions: dict[tuple[str, str], tuple[str, str, str]] = {}
        self.halted: bool = False
        self.accepted: bool = False
        self.step_count: int = 0
        self.last_transition: Optional[dict] = None

    def load_program(self, program: dict) -> None:
        """Load a program (transition rules) into the machine."""
        self.initial_state = program.get("initial_state", "q0")
        self.accept_states = set(program.get("accept_states", []))
        self.reject_states = set(program.get("reject_states", []))
        self.blank_symbol = program.get("blank_symbol", "_")

        self.transitions = {}
        for key, value in program.get("transitions", {}).items():
            state, symbol = key.split(",")
            new_state, write_symbol, direction = value
            self.transitions[(state.strip(), symbol.strip())] = (
                new_state, write_symbol, direction.upper()
            )

        self.reset()

    def set_tape(self, input_string: str) -> None:
        """Initialize the tape with an input string."""
        self.tape = {}
        for i, char in enumerate(input_string):
            self.tape[i] = char
        self.head_position = 0
        self.halted = False
        self.accepted = False
        self.step_count = 0
        self.last_transition = None

    def reset(self) -> None:
        """Reset the machine to initial state."""
        self.current_state = self.initial_state
        self.head_position = 0
        self.tape = {}
        self.halted = False
        self.accepted = False
        self.step_count = 0
        self.last_transition = None

    def read_symbol(self) -> str:
        """Read the symbol at the current head position."""
        return self.tape.get(self.head_position, self.blank_symbol)

    def write_symbol(self, symbol: str) -> None:
        """Write a symbol at the current head position."""
        if symbol == self.blank_symbol and self.head_position in self.tape:
            del self.tape[self.head_position]
        else:
            self.tape[self.head_position] = symbol

    def move_head(self, direction: str) -> None:
        """Move the head left (L), right (R), or stay (N)."""
        if direction == "L":
            self.head_position -= 1
        elif direction == "R":
            self.head_position += 1

    def step(self) -> bool:
        """Execute one step of the machine. Returns True if step was executed."""
        if self.halted:
            return False

        current_symbol = self.read_symbol()
        key = (self.current_state, current_symbol)

        if key not in self.transitions:
            self.halted = True
            self.accepted = self.current_state in self.accept_states
            self.last_transition = {
                "from_state": self.current_state,
                "read": current_symbol,
                "to_state": None,
                "write": None,
                "direction": None,
                "halted": True,
                "reason": "no_transition"
            }
            return False

        new_state, write_symbol, direction = self.transitions[key]

        self.last_transition = {
            "from_state": self.current_state,
            "read": current_symbol,
            "to_state": new_state,
            "write": write_symbol,
            "direction": direction
        }

        self.write_symbol(write_symbol)
        self.move_head(direction)
        self.current_state = new_state
        self.step_count += 1

        if self.current_state in self.accept_states:
            self.halted = True
            self.accepted = True
            self.last_transition["halted"] = True
            self.last_transition["reason"] = "accepted"
        elif self.current_state in self.reject_states:
            self.halted = True
            self.accepted = False
            self.last_transition["halted"] = True
            self.last_transition["reason"] = "rejected"

        return True

    def run(self, max_steps: int = 10000) -> dict:
        """Run the machine until it halts or reaches max steps."""
        steps_executed = 0
        while not self.halted and steps_executed < max_steps:
            if not self.step():
                break
            steps_executed += 1

        return {
            "halted": self.halted,
            "accepted": self.accepted,
            "steps_executed": steps_executed,
            "max_steps_reached": steps_executed >= max_steps and not self.halted
        }

    def get_state(self) -> MachineState:
        """Get a copy of the current machine state."""
        return MachineState(
            tape=copy.deepcopy(self.tape),
            head_position=self.head_position,
            current_state=self.current_state,
            halted=self.halted,
            accepted=self.accepted,
            step_count=self.step_count
        )

    def restore_state(self, state: MachineState) -> None:
        """Restore the machine to a previous state."""
        self.tape = copy.deepcopy(state.tape)
        self.head_position = state.head_position
        self.current_state = state.current_state
        self.halted = state.halted
        self.accepted = state.accepted
        self.step_count = state.step_count
        self.last_transition = None

    def get_tape_segment(self, padding: int = 5) -> dict:
        """Get a segment of tape around the head for display."""
        if not self.tape:
            min_pos = self.head_position - padding
            max_pos = self.head_position + padding
        else:
            min_pos = min(min(self.tape.keys()), self.head_position) - padding
            max_pos = max(max(self.tape.keys()), self.head_position) + padding

        segment = {}
        for i in range(min_pos, max_pos + 1):
            segment[i] = self.tape.get(i, self.blank_symbol)

        return {
            "cells": segment,
            "head_position": self.head_position,
            "min_position": min_pos,
            "max_position": max_pos
        }

    def to_dict(self) -> dict:
        """Convert current state to a dictionary for JSON serialization."""
        tape_segment = self.get_tape_segment()
        return {
            "tape": tape_segment,
            "current_state": self.current_state,
            "halted": self.halted,
            "accepted": self.accepted,
            "step_count": self.step_count,
            "last_transition": self.last_transition
        }
