"""Flask API for the Turing Machine Simulator."""

import os
import json
import uuid
import random
from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
from dotenv import load_dotenv
from turing_machine import TuringMachine
from history import HistoryManager
from examples import get_example_list, get_example, get_lessons

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "turing-machine-secret-key-change-me")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

machine = TuringMachine()
history = HistoryManager()

# Which lessons have practice exercises
# Lesson 4=head, 5=states, 6=rules, 8=binary (7=all-rules has no practice)
LESSONS_WITH_PRACTICE = [4, 5, 6, 8]


# ==================== TURING MACHINE VERIFIER ====================

def run_tm_solution(rules, input_str, max_steps=1000):
    """
    Run a Turing machine solution and return the result.

    rules: dict of state -> {symbol -> {write, move, goto}}
    input_str: the input string to put on tape

    Returns: {halted, state, output, steps, timeout}
    """
    tape = {}
    for i, char in enumerate(input_str):
        tape[i] = char

    head_pos = 0
    state = "START"
    steps = 0

    while steps < max_steps:
        symbol = tape.get(head_pos, "_")

        if state == "DONE":
            return {
                "halted": True,
                "state": state,
                "output": tape.get(head_pos, "_"),
                "steps": steps,
                "timeout": False
            }

        if state not in rules or symbol not in rules[state]:
            return {
                "halted": True,
                "state": state,
                "output": tape.get(head_pos, "_"),
                "steps": steps,
                "timeout": False,
                "error": f"No rule for state={state}, symbol={symbol}"
            }

        rule = rules[state][symbol]
        tape[head_pos] = rule["write"]

        if rule["move"] == "right":
            head_pos += 1
        elif rule["move"] == "left":
            head_pos -= 1
        # "stay" = don't move

        state = rule["goto"]
        steps += 1

    return {
        "halted": False,
        "state": state,
        "output": tape.get(head_pos, "_"),
        "steps": steps,
        "timeout": True
    }


def verify_solution(rules, test_cases):
    """
    Verify a solution against test cases.
    Returns: {passed: bool, results: [...], failed_count: int}
    """
    results = []
    failed_count = 0

    for tc in test_cases:
        input_str = tc.get("input", "")
        expected = tc.get("expected", "")

        result = run_tm_solution(rules, input_str)

        passed = (
            result["state"] == "DONE" and
            result["output"] == expected and
            not result["timeout"]
        )

        if not passed:
            failed_count += 1

        results.append({
            "input": input_str,
            "expected": expected,
            "actual": result["output"],
            "state": result["state"],
            "passed": passed,
            "steps": result["steps"],
            "timeout": result.get("timeout", False)
        })

    return {
        "passed": failed_count == 0,
        "results": results,
        "failed_count": failed_count
    }


# ==================== PAGE ROUTES ====================

@app.route("/")
def index():
    """Redirect to first lesson."""
    from flask import redirect
    return redirect("/lesson/1")


@app.route("/lesson/<int:lesson_num>")
def lesson(lesson_num):
    """Display a specific lesson."""
    lessons = get_lessons()

    if lesson_num < 1 or lesson_num > len(lessons):
        return render_template("lessons/welcome.html", active_page="lessons")

    lesson_data = lessons[lesson_num - 1]
    has_practice = lesson_num in LESSONS_WITH_PRACTICE

    return render_template(
        "lessons/lesson.html",
        lesson=lesson_data,
        lesson_num=lesson_num,
        total_lessons=len(lessons),
        has_practice=has_practice,
        active_page="lessons"
    )


@app.route("/lesson/<int:lesson_num>/practice")
def lesson_practice(lesson_num):
    """Display practice exercise for a lesson."""
    if lesson_num not in LESSONS_WITH_PRACTICE:
        return render_template("lessons/welcome.html", active_page="lessons")

    # TODO: Implement practice templates
    return render_template(
        "lessons/practice.html",
        lesson_num=lesson_num,
        active_page="lessons"
    )


@app.route("/simulator")
def simulator():
    """Simulator page."""
    return render_template("simulator/index.html", active_page="simulator")


@app.route("/challenge")
def challenge_task():
    """Challenge mode - task page."""
    return render_template("challenge/task.html", active_page="challenge")


@app.route("/challenge/states")
def challenge_states():
    """Challenge mode - define states."""
    breadcrumbs = [
        {"label": "Task", "url": "/challenge", "completed": True},
        {"label": "States", "url": "/challenge/states", "completed": False}
    ]
    return render_template(
        "challenge/states.html",
        active_page="challenge",
        breadcrumbs=breadcrumbs
    )


@app.route("/challenge/rules/<state_name>")
def challenge_rules(state_name):
    """Challenge mode - define rules for a state."""
    breadcrumbs = [
        {"label": "Task", "url": "/challenge", "completed": True},
        {"label": "States", "url": "/challenge/states", "completed": True},
        {"label": state_name, "url": f"/challenge/rules/{state_name}", "completed": False}
    ]
    return render_template(
        "challenge/rules.html",
        state_name=state_name,
        active_page="challenge",
        breadcrumbs=breadcrumbs
    )


@app.route("/challenge/review")
def challenge_review():
    """Challenge mode - review algorithm."""
    breadcrumbs = [
        {"label": "Task", "url": "/challenge", "completed": True},
        {"label": "States", "url": "/challenge/states", "completed": True},
        {"label": "Rules", "url": "#", "completed": True},
        {"label": "Review", "url": "/challenge/review", "completed": False}
    ]
    return render_template(
        "challenge/review.html",
        active_page="challenge",
        breadcrumbs=breadcrumbs
    )


@app.route("/challenge/run")
def challenge_run():
    """Challenge mode - run tests."""
    breadcrumbs = [
        {"label": "Task", "url": "/challenge", "completed": True},
        {"label": "States", "url": "/challenge/states", "completed": True},
        {"label": "Rules", "url": "#", "completed": True},
        {"label": "Review", "url": "/challenge/review", "completed": True},
        {"label": "Test", "url": "/challenge/run", "completed": False}
    ]
    return render_template(
        "challenge/run.html",
        active_page="challenge",
        breadcrumbs=breadcrumbs
    )


# ==================== LEGACY ROUTE (for old single-page app) ====================

@app.route("/old")
def old_index():
    """Serve the old single-page UI (for backwards compatibility)."""
    return render_template("index.html")


# ==================== API ROUTES ====================


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
    """Generate a new TM challenge with VERIFIED solution."""
    from flask import make_response

    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            # Generate challenge + solution in ONE call
            response = client.chat.completions.create(
                model="gpt-4o",  # Use better model for accurate solutions
                messages=[
                    {
                        "role": "system",
                        "content": """You are a Turing machine expert. Generate a challenge WITH a working solution.

TURING MACHINE RULES:
- States: START (entry), DONE (halt), plus your working states
- Symbols: 0, 1, _ (blank)
- Head starts at position 0 (first character)
- Output: symbol at head position when machine reaches DONE

CHALLENGE TYPES - YOU MUST RANDOMLY PICK ONE (use the random number below):
1. PARITY: Count 1s → output "1" if EVEN count, "0" if ODD count
2. HAS_CONSECUTIVE: Output "1" if input has two consecutive same symbols (00 or 11), "0" otherwise
3. ENDS_SAME_AS_START: Output "1" if first and last non-blank chars are equal, "0" otherwise
4. MORE_ONES_THAN_ZEROS: Output "1" if count of 1s > count of 0s, "0" otherwise
5. LENGTH_PARITY: Output "1" if input length is even, "0" if odd
6. CONTAINS_PATTERN_01: Output "1" if input contains "01" somewhere, "0" otherwise
7. ALL_SAME: Output "1" if all symbols are identical (all 0s or all 1s), "0" otherwise
8. FIRST_EQUALS_LAST: Output "1" if first char equals last char, "0" otherwise

DO NOT USE trivial challenges that don't need working states!

CRITICAL: You MUST provide a WORKING solution that passes ALL test cases!

OUTPUT FORMAT - Return ONLY valid JSON:
{
  "id": "unique-id",
  "task": "Clear one-sentence task description",
  "task_detail": "Detailed explanation: when to output 1, when to output 0",
  "output_spec": {
    "description": "What the output symbol means",
    "values": {"1": "meaning of 1", "0": "meaning of 0"}
  },
  "test_cases": [
    {"input": "101", "expected": "0", "reason": "explanation"},
    {"input": "11", "expected": "1", "reason": "explanation"},
    {"input": "0", "expected": "0", "reason": "explanation"},
    {"input": "", "expected": "1", "reason": "empty input case"}
  ],
  "suggested_states": ["STATE1", "STATE2"],
  "hint": "A helpful hint",
  "solution": {
    "START": {
      "0": {"write": "0", "move": "right", "goto": "STATE1"},
      "1": {"write": "1", "move": "right", "goto": "STATE2"},
      "_": {"write": "1", "move": "stay", "goto": "DONE"}
    },
    "STATE1": {
      "0": {"write": "0", "move": "right", "goto": "STATE1"},
      "1": {"write": "1", "move": "right", "goto": "STATE2"},
      "_": {"write": "0", "move": "stay", "goto": "DONE"}
    }
  }
}

IMPORTANT:
- Test the solution mentally against ALL test cases before outputting
- test_cases.expected MUST match what the solution actually outputs
- Make sure solution handles empty input (head at blank)
- Every state must have rules for 0, 1, AND _ (blank)"""
                    },
                    {
                        "role": "user",
                        "content": f"Generate challenge type #{random.randint(1, 8)} from the list. Make sure the solution actually works!"
                    }
                ],
                temperature=0.7
            )

            result = response.choices[0].message.content

            # Clean up response
            result = result.strip()
            if result.startswith("```"):
                lines = result.split("\n")
                result = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
                if result.startswith("json"):
                    result = result[4:]
            result = result.strip()

            challenge = json.loads(result)

            # VERIFY the solution actually works
            if "solution" in challenge and "test_cases" in challenge:
                verification = verify_solution(challenge["solution"], challenge["test_cases"])

                if verification["passed"]:
                    # SUCCESS! Store in session and return
                    challenge["id"] = str(uuid.uuid4())
                    challenge["verified"] = True
                    session["current_challenge"] = challenge

                    # Return challenge WITHOUT solution (user shouldn't see it yet)
                    response_data = {k: v for k, v in challenge.items() if k != "solution"}
                    resp = make_response(jsonify(response_data))
                    # Prevent caching so new challenges are always generated
                    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                    resp.headers['Pragma'] = 'no-cache'
                    resp.headers['Expires'] = '0'
                    return resp
                else:
                    # Solution failed verification - log and retry
                    print(f"Attempt {attempt + 1}: Solution failed verification")
                    print(f"Failed tests: {verification['failed_count']}")
                    for r in verification["results"]:
                        if not r["passed"]:
                            print(f"  Input '{r['input']}': expected '{r['expected']}', got '{r['actual']}'")
                    continue
            else:
                print(f"Attempt {attempt + 1}: Missing solution or test_cases")
                continue

        except json.JSONDecodeError as e:
            print(f"Attempt {attempt + 1}: JSON parse error - {e}")
            continue
        except Exception as e:
            print(f"Attempt {attempt + 1}: Error - {e}")
            continue

    # All attempts failed - return error
    resp = make_response(jsonify({"error": "Failed to generate valid challenge after multiple attempts. Please try again."}), 500)
    resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp


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


@app.route("/api/challenge/validate-states", methods=["POST"])
def validate_states():
    """Validate student's chosen states for a challenge."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    challenge = data.get("challenge")
    states = data.get("states")

    if not challenge or not states:
        return jsonify({"error": "Missing challenge or states"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a Turing machine teacher helping a student design their algorithm.

The student was given a challenge and has chosen some states for their Turing machine.
Evaluate if their states are a good starting point.

Remember: States in a Turing machine represent "memory" - what the machine needs to remember.

Be encouraging! Even if not perfect, if they're on the right track, let them continue.
Only reject if fundamentally wrong or missing critical states.

Output ONLY valid JSON:
{
  "valid": true or false,
  "feedback": "Brief encouraging message (1-2 sentences)"
}"""
                },
                {
                    "role": "user",
                    "content": f"""Challenge: {json.dumps(challenge)}

Student's chosen states:
{json.dumps(states, indent=2)}

Are these states appropriate for this challenge?"""
                }
            ],
            temperature=0.3
        )

        result = response.choices[0].message.content
        evaluation = json.loads(result)
        return jsonify(evaluation)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/challenge/validate-rules", methods=["POST"])
def validate_rules():
    """Validate rules for a specific state."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    challenge = data.get("challenge")
    state_name = data.get("state_name")
    state_rules = data.get("rules")
    all_states = data.get("all_states")

    if not challenge or not state_rules:
        return jsonify({"error": "Missing data"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a Turing machine teacher helping a student define rules for their algorithm.

The student has defined rules for one state. Check if these rules make sense for the challenge.

Be encouraging but point out problems:
- Does the logic fit the task?
- Are there obvious mistakes (e.g., infinite loops)?
- Is the transition to next states reasonable?

Output ONLY valid JSON:
{
  "valid": true or false,
  "feedback": "Brief feedback (1-2 sentences). If valid, be encouraging. If not, explain what's wrong.",
  "suggestion": "If invalid: hint how to fix. Empty string if valid."
}"""
                },
                {
                    "role": "user",
                    "content": f"""Challenge: {json.dumps(challenge)}

State being defined: {state_name}
All states: {json.dumps(all_states)}

Rules for {state_name}:
- See 0: write {state_rules['0']['write']}, move {state_rules['0']['move']}, go to {state_rules['0']['goto']}
- See 1: write {state_rules['1']['write']}, move {state_rules['1']['move']}, go to {state_rules['1']['goto']}
- See blank: write {state_rules['_']['write']}, move {state_rules['_']['move']}, go to {state_rules['_']['goto']}

Are these rules appropriate for this state?"""
                }
            ],
            temperature=0.3
        )

        result = response.choices[0].message.content
        evaluation = json.loads(result)
        return jsonify(evaluation)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/challenge/get-answer", methods=["POST"])
def get_answer():
    """Get the VERIFIED correct answer for a specific state from session."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    state_name = data.get("state_name")

    if not state_name:
        return jsonify({"error": "Missing state_name"}), 400

    # Get verified solution from session
    challenge = session.get("current_challenge")

    if not challenge:
        return jsonify({"error": "No active challenge. Please start a new challenge."}), 400

    if "solution" not in challenge:
        return jsonify({"error": "Challenge has no verified solution."}), 400

    solution = challenge["solution"]

    if state_name not in solution:
        # State doesn't exist in solution - return helpful message
        available_states = list(solution.keys())
        return jsonify({
            "error": f"State '{state_name}' not in solution. Available states: {available_states}",
            "hint": f"The verified solution uses these states: {available_states}. You may need to rename your states."
        }), 400

    # Return the verified rules for this state
    return jsonify({
        "rules": solution[state_name],
        "explanation": f"Verified rules for {state_name} that pass all test cases.",
        "verified": True,
        "solution_states": list(solution.keys())
    })


@app.route("/api/challenge/get-full-solution", methods=["GET"])
def get_full_solution():
    """Get the complete verified solution for the current challenge."""
    challenge = session.get("current_challenge")

    if not challenge:
        return jsonify({"error": "No active challenge. Please start a new challenge."}), 400

    if "solution" not in challenge:
        return jsonify({"error": "Challenge has no verified solution."}), 400

    return jsonify({
        "solution": challenge["solution"],
        "states": list(challenge["solution"].keys()),
        "test_cases": challenge.get("test_cases", []),
        "verified": True
    })


@app.route("/api/challenge/check-algorithm", methods=["POST"])
def check_algorithm():
    """Check if student's complete algorithm is correct."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    challenge = data.get("challenge")
    states = data.get("states")
    rules = data.get("rules")

    if not challenge or not rules:
        return jsonify({"error": "Missing challenge or rules"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a Turing machine teacher evaluating a student's complete algorithm.

Analyze if the algorithm correctly solves the given challenge.

Check for:
1. Does it handle all input cases correctly?
2. Will it always terminate (reach DONE state)?
3. Are there missing rules for any state/symbol combinations?
4. Does the logic make sense for the task?

If CORRECT: Congratulate them!
If INCORRECT: Give specific, helpful feedback about what's wrong and how to fix it.

Output ONLY valid JSON:
{
  "correct": true or false,
  "feedback": "Brief assessment (1-2 sentences)",
  "suggestion": "If incorrect: specific suggestion what to fix. Empty string if correct."
}"""
                },
                {
                    "role": "user",
                    "content": f"""Challenge: {json.dumps(challenge)}

States: {json.dumps(states)}

Rules:
{json.dumps(rules, indent=2)}

Evaluate this Turing machine algorithm."""
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
