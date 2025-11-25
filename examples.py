"""Educational Turing machine - Learn First, Then Play."""

# Lessons shown BEFORE the simulator
LESSONS = [
    {
        "id": "welcome",
        "title": "Welcome!",
        "content": """
            <h2>Welcome to the Turing Machine Simulator!</h2>
            <p class="lead">Learn how the simplest computer works.</p>
            <p>Today we'll teach a machine to add 1 to a binary number.</p>
            <p class="muted">(Don't worry, we'll explain everything step by step!)</p>
        """
    },
    {
        "id": "what-is-tm",
        "title": "What is a Turing Machine?",
        "content": """
            <h2>What is a Turing Machine?</h2>
            <p>A Turing machine is the <strong>simplest possible computer</strong>.</p>
            <p>It was invented by Alan Turing in 1936.</p>
            <div class="highlight-box">
                <p>It has only <strong>3 parts</strong>:</p>
                <ol>
                    <li><strong>A TAPE</strong> - like an infinite strip of paper</li>
                    <li><strong>A HEAD</strong> - that reads and writes on the tape</li>
                    <li><strong>RULES</strong> - that tell it what to do</li>
                </ol>
            </div>
            <p>That's it! Yet it can compute <em>anything</em> a modern computer can.</p>
        """
    },
    {
        "id": "tape",
        "title": "The Tape",
        "content": """
            <h2>The Tape</h2>
            <p>The tape is divided into boxes called <strong>"cells"</strong>.</p>
            <p>Each cell holds <strong>ONE symbol</strong>.</p>
            <div class="tape-demo">
                <div class="tape-cell">_</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell">0</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell">_</div>
            </div>
            <ul>
                <li>The tape goes on <strong>FOREVER</strong> in both directions</li>
                <li>Empty cells contain "blank" (shown as _)</li>
                <li>Our tape holds binary numbers: <strong>0s and 1s</strong></li>
            </ul>
        """
    },
    {
        "id": "head",
        "title": "The Head",
        "content": """
            <h2>The Head</h2>
            <p>The head points to <strong>ONE cell</strong> at a time.</p>
            <div class="tape-demo">
                <div class="tape-cell">_</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell head">0</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell">_</div>
            </div>
            <div class="head-pointer">▲ HEAD</div>
            <div class="highlight-box">
                <p>The head can:</p>
                <ul>
                    <li>✓ <strong>READ</strong> the symbol in the current cell</li>
                    <li>✓ <strong>WRITE</strong> a new symbol</li>
                    <li>✓ <strong>MOVE</strong> left or right</li>
                </ul>
            </div>
        """
    },
    {
        "id": "states",
        "title": "States (Modes)",
        "content": """
            <h2>States (Think of them as "modes")</h2>
            <p>The machine is always in <strong>ONE state</strong> at a time.</p>
            <p>States are like moods or modes of operation.</p>
            <div class="highlight-box">
                <p>For adding 1 to a binary number, we use:</p>
                <div class="state-item"><span class="state-emoji">🔍</span> <strong>SCAN</strong> - "I'm looking for the end of the number"</div>
                <div class="state-item"><span class="state-emoji">➕</span> <strong>ADD</strong> - "I'm adding 1 now"</div>
                <div class="state-item"><span class="state-emoji">✅</span> <strong>DONE</strong> - "I'm finished!"</div>
            </div>
            <p>The machine starts in <strong>SCAN</strong> mode.</p>
        """
    },
    {
        "id": "rules",
        "title": "The Rules",
        "content": """
            <h2>The Rules</h2>
            <p>Rules tell the machine what to do.</p>
            <p>Each rule says:</p>
            <div class="rule-template">
                "When in <strong>[STATE]</strong> and I see <strong>[SYMBOL]</strong>:<br>
                → Write <strong>[NEW SYMBOL]</strong><br>
                → Move <strong>[LEFT/RIGHT/STAY]</strong><br>
                → Switch to <strong>[NEW STATE]</strong>"
            </div>
            <div class="example-rule">
                <p><strong>Example rule:</strong></p>
                <p>When in <span class="badge">SCAN</span> and I see <span class="badge">1</span>:</p>
                <ul>
                    <li>→ Keep the 1 (write 1)</li>
                    <li>→ Move RIGHT</li>
                    <li>→ Stay in SCAN mode</li>
                </ul>
                <p class="muted">(This means: "Still looking, move to next cell")</p>
            </div>
        """
    },
    {
        "id": "all-rules",
        "title": "All the Rules",
        "content": """
            <h2>All 6 Rules for Adding 1</h2>
            <div class="rules-group">
                <h3>🔍 SCAN MODE (looking for the end):</h3>
                <div class="rule">See <strong>0</strong> → keep it, move right, stay in SCAN</div>
                <div class="rule">See <strong>1</strong> → keep it, move right, stay in SCAN</div>
                <div class="rule">See <strong>blank</strong> → found the end! move left, switch to ADD</div>
            </div>
            <div class="rules-group">
                <h3>➕ ADD MODE (doing the math):</h3>
                <div class="rule">See <strong>0</strong> → write 1, stop, DONE <span class="muted">(0+1=1)</span></div>
                <div class="rule">See <strong>1</strong> → write 0, move left, stay in ADD <span class="muted">(1+1=10, carry!)</span></div>
                <div class="rule">See <strong>blank</strong> → write 1, stop, DONE</div>
            </div>
        """
    },
    {
        "id": "binary",
        "title": "Binary Numbers",
        "content": """
            <h2>Binary Numbers (Super Quick!)</h2>
            <p>Binary only uses <strong>0</strong> and <strong>1</strong>.</p>
            <p>Each position is worth <strong>2x</strong> the one to its right.</p>
            <div class="binary-example">
                <code>1011</code> in binary = 8 + 0 + 2 + 1 = <strong>11</strong> in decimal
            </div>
            <p>Adding 1 is like counting:</p>
            <div class="binary-example">
                <code>1011</code> (11) + 1 = <code>1100</code> (12)
            </div>
            <p>When a digit goes from 1 to 2, it becomes 0 and we <strong>"carry"</strong> 1 to the left.</p>
            <p class="muted">(Just like 9+1=10 in regular numbers!)</p>
        """
    }
]

# The main example with educational content
EXAMPLES = {
    "binary_increment": {
        "name": "Add 1 to Binary Number",
        "description": "Take a binary number and add 1 to it",
        "goal": "Add 1 to the binary number",
        "initial_state": "scan",
        "accept_states": ["done"],
        "reject_states": [],
        "blank_symbol": "_",
        "default_input": "1011",

        "states": {
            "scan": {
                "label": "SCAN",
                "emoji": "🔍",
                "description": "Looking for the end of the number"
            },
            "add": {
                "label": "ADD",
                "emoji": "➕",
                "description": "Adding 1 and handling carry"
            },
            "done": {
                "label": "DONE",
                "emoji": "✅",
                "description": "Finished!"
            }
        },

        # Explanations shown BEFORE each action
        "next_action_explanations": {
            "scan,0": {
                "action": "Keep the 0, move RIGHT, stay in SCAN",
                "why": "I'm still looking for the end of the number."
            },
            "scan,1": {
                "action": "Keep the 1, move RIGHT, stay in SCAN",
                "why": "I'm still looking for the end of the number."
            },
            "scan,_": {
                "action": "Stay here, move LEFT, switch to ADD",
                "why": "Found the end! Time to go back and start adding."
            },
            "add,0": {
                "action": "Write 1, STOP, switch to DONE",
                "why": "0 + 1 = 1. No carry needed. We're done!"
            },
            "add,1": {
                "action": "Write 0, move LEFT, stay in ADD",
                "why": "1 + 1 = 2 = '10' in binary. Write 0, carry the 1 left."
            },
            "add,_": {
                "action": "Write 1, STOP, switch to DONE",
                "why": "No more digits, but we still have a carry. Write 1 here."
            }
        },

        "rules": [
            {"state": "scan", "see": "0", "write": "0", "move": "right", "goto": "scan"},
            {"state": "scan", "see": "1", "write": "1", "move": "right", "goto": "scan"},
            {"state": "scan", "see": "_", "write": "_", "move": "left", "goto": "add"},
            {"state": "add", "see": "0", "write": "1", "move": "stay", "goto": "done"},
            {"state": "add", "see": "1", "write": "0", "move": "left", "goto": "add"},
            {"state": "add", "see": "_", "write": "1", "move": "stay", "goto": "done"}
        ],

        "transitions": {
            "scan,0": ["scan", "0", "R"],
            "scan,1": ["scan", "1", "R"],
            "scan,_": ["add", "_", "L"],
            "add,0": ["done", "1", "N"],
            "add,1": ["add", "0", "L"],
            "add,_": ["done", "1", "N"]
        }
    }
}


def get_lessons():
    """Get all lessons for onboarding."""
    return LESSONS


def get_example_list():
    """Get list of available examples."""
    return [
        {
            "id": key,
            "name": example["name"],
            "description": example["description"],
            "default_input": example["default_input"]
        }
        for key, example in EXAMPLES.items()
    ]


def get_example(example_id: str):
    """Get a specific example by ID."""
    return EXAMPLES.get(example_id)
