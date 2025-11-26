"""Flask API for the Turing Machine Simulator."""

import os
import json
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from turing_machine import TuringMachine
from history import HistoryManager
from examples import get_example_list, get_example, get_lessons

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

machine = TuringMachine()
history = HistoryManager()


@app.route("/")
def index():
    """Serve the main web UI."""
    return render_template("index.html")


@app.route("/api/load", methods=["POST"])
def load_program():
    """Load a program and optionally set initial tape."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    program = data.get("program")
    tape_input = data.get("tape", "")

    if not program:
        return jsonify({"error": "No program provided"}), 400

    try:
        machine.load_program(program)
        if tape_input:
            machine.set_tape(tape_input)

        history.clear()
        history.push(machine.get_state())

        return jsonify({
            "success": True,
            "machine": machine.to_dict(),
            "program": {
                "states": list(set(
                    [t[0] for t in machine.transitions.keys()] +
                    [t[0] for t in machine.transitions.values()]
                )),
                "transitions": {
                    f"{k[0]},{k[1]}": list(v)
                    for k, v in machine.transitions.items()
                }
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/step", methods=["POST"])
def step():
    """Execute one step of the machine."""
    if machine.halted:
        return jsonify({
            "success": False,
            "message": "Machine is halted",
            "machine": machine.to_dict()
        })

    history.push(machine.get_state())
    executed = machine.step()

    return jsonify({
        "success": executed,
        "machine": machine.to_dict(),
        "can_undo": history.can_undo(),
        "can_redo": history.can_redo()
    })


@app.route("/api/run", methods=["POST"])
def run():
    """Run the machine until it halts or reaches max steps."""
    data = request.get_json() or {}
    max_steps = data.get("max_steps", 10000)

    history.push(machine.get_state())
    result = machine.run(max_steps)

    return jsonify({
        "result": result,
        "machine": machine.to_dict(),
        "can_undo": history.can_undo(),
        "can_redo": history.can_redo()
    })


@app.route("/api/reset", methods=["POST"])
def reset():
    """Reset the machine to initial state with current program."""
    data = request.get_json() or {}
    tape_input = data.get("tape", "")

    machine.reset()
    if tape_input:
        machine.set_tape(tape_input)

    history.clear()
    history.push(machine.get_state())

    return jsonify({
        "success": True,
        "machine": machine.to_dict(),
        "can_undo": history.can_undo(),
        "can_redo": history.can_redo()
    })


@app.route("/api/undo", methods=["POST"])
def undo():
    """Undo the last step."""
    state = history.undo()

    if state:
        machine.restore_state(state)
        return jsonify({
            "success": True,
            "machine": machine.to_dict(),
            "can_undo": history.can_undo(),
            "can_redo": history.can_redo()
        })

    return jsonify({
        "success": False,
        "message": "Nothing to undo",
        "can_undo": history.can_undo(),
        "can_redo": history.can_redo()
    })


@app.route("/api/redo", methods=["POST"])
def redo():
    """Redo a previously undone step."""
    state = history.redo()

    if state:
        machine.restore_state(state)
        return jsonify({
            "success": True,
            "machine": machine.to_dict(),
            "can_undo": history.can_undo(),
            "can_redo": history.can_redo()
        })

    return jsonify({
        "success": False,
        "message": "Nothing to redo",
        "can_undo": history.can_undo(),
        "can_redo": history.can_redo()
    })


@app.route("/api/lessons", methods=["GET"])
def lessons():
    """Get lessons for onboarding."""
    return jsonify(get_lessons())


@app.route("/api/examples", methods=["GET"])
def examples():
    """Get list of available example programs."""
    return jsonify(get_example_list())


@app.route("/api/examples/<example_id>", methods=["GET"])
def get_example_program(example_id):
    """Get a specific example program."""
    example = get_example(example_id)
    if example:
        return jsonify(example)
    return jsonify({"error": "Example not found"}), 404


@app.route("/api/challenge", methods=["GET"])
def get_challenge():
    """Generate a new TM challenge using AI."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a Turing machine teacher. Generate a simple challenge for a beginner who just learned how to add 1 to a binary number.

IMPORTANT: Do NOT generate any challenge about adding, incrementing, or subtracting numbers! The student already learned "add 1 to binary" - we need a DIFFERENT challenge.

The challenge should be solvable with 2-4 states and use only 0, 1, and blank symbols.

Good challenge examples (pick one or create similar):
- Check if a binary number has an even or odd number of 1s
- Check if a binary string is a palindrome
- Flip all bits (replace all 1s with 0s and vice versa)
- Check if a binary string starts and ends with the same symbol
- Delete all leading zeros from a number
- Check if a string has at least two 1s

BAD challenges (DO NOT USE):
- Add 1 to a binary number (already learned!)
- Subtract 1 from a binary number
- Increment or decrement anything
- Any arithmetic operation

Output ONLY valid JSON (no markdown):
{
  "task": "Clear description of what to build",
  "examples": [
    {"input": "101", "output": "Description of expected result"}
  ],
  "difficulty": "easy",
  "hint_for_stuck": "A subtle hint without revealing the answer"
}"""
                },
                {
                    "role": "user",
                    "content": "Generate a new beginner-friendly Turing machine challenge."
                }
            ],
            temperature=0.8
        )

        result = response.choices[0].message.content
        # Parse JSON from response
        challenge = json.loads(result)
        return jsonify(challenge)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/check-plan", methods=["POST"])
def check_plan():
    """Check if student's algorithm plan is correct."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    challenge = data.get("challenge")
    student_plan = data.get("plan")

    if not challenge or not student_plan:
        return jsonify({"error": "Missing challenge or plan"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a Turing machine teacher evaluating a student's algorithm plan.

The student was given a challenge and wrote their algorithm in plain English.
Evaluate if their logic would work for a Turing machine.

If WRONG:
- Give a VERY SUBTLE hint - do NOT explain the solution
- Ask a thought-provoking question like "What happens when...?" or "Have you considered...?"
- NEVER mention specific states, transitions, or implementation details
- NEVER say things like "you need a state that..." or "try tracking..."
- Just nudge them to think about what they might be missing
- Keep hints short (1 sentence max)

If CORRECT:
- Congratulate them briefly
- Convert their plan to working Turing machine rules

Output ONLY valid JSON (no markdown):
{
  "correct": true or false,
  "feedback": "Brief encouraging message (1 sentence)",
  "hint": "If wrong: a subtle question to make them think. Empty string if correct.",
  "rules": null if wrong, or if correct: {
    "name": "Algorithm name",
    "initial_state": "start",
    "accept_states": ["done"],
    "blank_symbol": "_",
    "default_input": "example",
    "states": {
      "state_name": {"label": "LABEL", "emoji": "🔍", "description": "What this state does"}
    },
    "rules": [
      {"state": "start", "see": "0", "write": "0", "move": "right", "goto": "start"}
    ],
    "transitions": {
      "start,0": ["start", "0", "R"]
    }
  }
}"""
                },
                {
                    "role": "user",
                    "content": f"""Challenge: {json.dumps(challenge)}

Student's algorithm plan:
{student_plan}

Evaluate their plan."""
                }
            ],
            temperature=0.3
        )

        result = response.choices[0].message.content
        evaluation = json.loads(result)
        return jsonify(evaluation)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
