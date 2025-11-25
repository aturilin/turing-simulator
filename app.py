"""Flask API for the Turing Machine Simulator."""

from flask import Flask, render_template, request, jsonify
from turing_machine import TuringMachine
from history import HistoryManager
from examples import get_example_list, get_example, get_lessons

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
