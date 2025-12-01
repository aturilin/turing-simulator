"""Educational Turing machine - Pedagogical Redesign v4.

NEW ORDER (Bottom-up, delayed state introduction):
1. Magic Demo - Hook
2. Tape - What data looks like
3. Head - How it reads/writes/moves
4. Simple Rules - Rules that work (bit flip)
5. The Problem - Why add 1 fails with simple rules
6. Lock Puzzle - NOW introduce states via lock metaphor
7. States Solve Everything - The solution
8. Finale
"""

# 8 Modules: Bottom-up discovery with delayed state introduction
LESSONS = [
    # ============================================================
    # MODULE 1: THE MAGIC TRICK (Demo FIRST - see it before theory)
    # ============================================================
    {
        "id": "magic-trick",
        "title": "The Magic Trick",
        "practice_type": "magic-demo",
        "content": """
            <div class="hook-intro">
                <p class="hook-line">Watch this.</p>
            </div>
        """
    },

    # ============================================================
    # MODULE 2: THE TAPE (Data storage - now earlier)
    # ============================================================
    {
        "id": "tape",
        "title": "The Tape",
        "practice_type": "explore-tape",
        "content": """
            <div class="concept-intro">
                <p class="lead">Now let's look at the machine you just watched.</p>
                <p>It has a <strong>tape</strong> &mdash; a row of boxes that hold symbols.</p>
            </div>

            <div class="tape-visual-demo horizontal">
                <div class="tape-cell blank">_</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell">0</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell blank">_</div>
            </div>

            <div class="insight-box">
                <p>Each box holds exactly <strong>ONE symbol</strong>:</p>
                <ul>
                    <li><strong>0</strong> or <strong>1</strong> &mdash; binary digits</li>
                    <li><strong>_</strong> &mdash; blank (empty)</li>
                </ul>
            </div>

            <div class="wow-connection">
                <p>That photo on your phone? <strong>10 million boxes</strong> like this.</p>
                <p>Each one just a 0 or 1. The computer doesn't "see" the photo &mdash; it just reads symbols.</p>
            </div>
        """
    },

    # ============================================================
    # MODULE 3: THE HEAD (Control - one cell at a time)
    # ============================================================
    {
        "id": "head",
        "title": "The Head",
        "practice_type": "control-head",
        "content": """
            <div class="concept-intro">
                <p class="lead">The machine has a <strong>head</strong> &mdash; like a finger pointing at one box.</p>
            </div>

            <div class="tape-visual-demo horizontal with-head">
                <div class="tape-cell blank">_</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell head">0</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell">1</div>
                <div class="tape-cell blank">_</div>
            </div>
            <div class="head-pointer">HEAD</div>

            <div class="constraint-box">
                <p class="constraint-title">The Catch:</p>
                <p>The head can only see <strong>ONE box</strong> at a time.</p>
                <p class="analogy"><em>Like reading a book through a keyhole &mdash; one letter at a time.</em></p>
            </div>

            <div class="actions-box">
                <p>The head can do exactly <strong>3 things</strong>:</p>
                <div class="action-list">
                    <div class="action-item">
                        <span class="action-icon">👁️</span>
                        <span class="action-text"><strong>READ</strong> the symbol</span>
                    </div>
                    <div class="action-item">
                        <span class="action-icon">✏️</span>
                        <span class="action-text"><strong>WRITE</strong> a new symbol</span>
                    </div>
                    <div class="action-item">
                        <span class="action-icon">👆</span>
                        <span class="action-text"><strong>MOVE</strong> left or right</span>
                    </div>
                </div>
            </div>
        """
    },

    # ============================================================
    # MODULE 4: SIMPLE RULES (Rules that work WITHOUT states)
    # ============================================================
    {
        "id": "simple-rules",
        "title": "Simple Rules",
        "practice_type": "simple-rules",
        "content": """
            <div class="concept-intro">
                <p class="lead">The machine follows <strong>rules</strong>.</p>
                <p>Let's start simple: <strong>flip every bit</strong>.</p>
            </div>

            <div class="rules-display simple">
                <div class="rule">See <strong>0</strong> → write <strong>1</strong>, move right</div>
                <div class="rule">See <strong>1</strong> → write <strong>0</strong>, move right</div>
                <div class="rule">See <strong>_</strong> → stop</div>
            </div>

            <div class="insight-box">
                <p>That's it. <strong>"When I see X, do Y."</strong></p>
                <p>Every program ever written &mdash; from Instagram to Excel &mdash; is just rules like this. Lots of them.</p>
            </div>
        """
    },

    # ============================================================
    # MODULE 5: THE LOCK PUZZLE (NOW introduce states)
    # ============================================================
    {
        "id": "lock-puzzle",
        "title": "The Lock Puzzle",
        "practice_type": "lock-puzzle",
        "content": """
            <div class="puzzle-intro">
                <p class="lead">Here's a lock with code <strong>1-2-3-4</strong>.</p>
                <p>Try to open it.</p>
            </div>

            <div class="puzzle-question">
                <p>Think about it: if the lock only had <strong>simple rules</strong>...</p>
                <p class="dim">"When I see 1 → check. When I see 2 → check..."</p>
                <p>...it would open when you press <strong>any</strong> correct digit!</p>
            </div>

            <div class="puzzle-insight">
                <p>But that's not how locks work.</p>
                <p>The lock must <strong>remember</strong> which digit it's waiting for.</p>
                <p class="dim">First it waits for 1. Then for 2. Then for 3. Then for 4.</p>
            </div>

            <div class="puzzle-reveal">
                <p>That memory &mdash; knowing <em>what to expect next</em> &mdash; is called a <strong>STATE</strong>.</p>
            </div>
        """
    },

    # ============================================================
    # MODULE 6: STATES SOLVE EVERYTHING
    # ============================================================
    {
        "id": "states",
        "title": "States Solve Everything",
        "practice_type": "states-solve",
        "content": """
            <div class="solution-intro">
                <p class="lead">Remember the lock?</p>
                <p>It remembered which digit to expect next. That memory is called a <strong>STATE</strong>.</p>
            </div>

            <div class="lock-timeline">
                <div class="lock-timeline-title">The lock moves through states:</div>
                <div class="lock-timeline-flow">
                    <div class="lock-step">
                        <div class="lock-step-label">WAIT_1</div>
                        <div class="lock-step-meaning">expecting<br>1st digit</div>
                    </div>
                    <div class="lock-step-arrow"></div>
                    <div class="lock-step">
                        <div class="lock-step-label">WAIT_2</div>
                        <div class="lock-step-meaning">expecting<br>2nd digit</div>
                    </div>
                    <div class="lock-step-arrow"></div>
                    <div class="lock-step">
                        <div class="lock-step-label">WAIT_3</div>
                        <div class="lock-step-meaning">expecting<br>3rd digit</div>
                    </div>
                    <div class="lock-step-arrow"></div>
                    <div class="lock-step">
                        <div class="lock-step-label">WAIT_4</div>
                        <div class="lock-step-meaning">expecting<br>4th digit</div>
                    </div>
                    <div class="lock-step-arrow"></div>
                    <div class="lock-step open">
                        <div class="lock-step-label">OPEN</div>
                        <div class="lock-step-meaning">unlocked!</div>
                    </div>
                </div>
            </div>

            <div class="key-insight">
                <div class="key-insight-header">KEY INSIGHT</div>
                <div class="key-insight-content">
                    <p>Same button press &rarr; <strong>different result</strong></p>
                    <p class="dim">depending on which state the lock is in</p>
                </div>
            </div>

            <div class="transition-box">
                <p>Our Turing machine needs the same thing!</p>
                <p class="dim">Different states = different behavior for the same symbol</p>
            </div>

            <div class="tm-states-showcase">
                <div class="tm-state-card cyan">
                    <div class="tm-state-icon">🔍</div>
                    <div class="tm-state-name">SCAN</div>
                    <div class="tm-state-desc">Looking for the end</div>
                </div>
                <div class="tm-states-arrow"></div>
                <div class="tm-state-card orange">
                    <div class="tm-state-icon">➕</div>
                    <div class="tm-state-name">ADD</div>
                    <div class="tm-state-desc">Adding 1 to digits</div>
                </div>
                <div class="tm-states-arrow"></div>
                <div class="tm-state-card green">
                    <div class="tm-state-icon">✅</div>
                    <div class="tm-state-name">DONE</div>
                    <div class="tm-state-desc">Finished!</div>
                </div>
            </div>

            <div class="conclusion-box">
                <p>Now the machine knows what to do:</p>
                <p class="highlight">In <strong>SCAN</strong> + see <strong>1</strong> &rarr; keep going right</p>
                <p class="highlight">In <strong>ADD</strong> + see <strong>1</strong> &rarr; write 0, carry left</p>
                <p class="dim">Same symbol, different state = different action!</p>
            </div>
        """
    },

    # ============================================================
    # MODULE 7: YOU NOW UNDERSTAND COMPUTERS
    # ============================================================
    {
        "id": "finale",
        "title": "You Now Understand Computers",
        "practice_type": "finale",
        "content": """
            <div class="finale-intro">
                <h2>The Complete Picture</h2>
            </div>

            <div class="recap-box">
                <div class="recap-item">
                    <span class="num">1</span>
                    <strong>Tape</strong> = memory (0s and 1s)
                </div>
                <div class="recap-item">
                    <span class="num">2</span>
                    <strong>Head</strong> = processor (read, write, move)
                </div>
                <div class="recap-item">
                    <span class="num">3</span>
                    <strong>States</strong> = what the CPU is "thinking about"
                </div>
                <div class="recap-item">
                    <span class="num">4</span>
                    <strong>Rules</strong> = the program
                </div>
            </div>

            <div class="wow-box">
                <p>That game on your phone? It's just rules.</p>
                <p>Very complicated rules, but rules.</p>
                <p>The CPU reads data, checks what mode it's in, and follows rules.</p>
            </div>

            <div class="final-revelation">
                <p>The <strong>ONLY</strong> difference between this Turing Machine and your iPhone?</p>
                <p class="revelation-answer"><strong>SPEED.</strong></p>
                <p>Your phone does this <strong>3,000,000,000</strong> times per second.</p>
            </div>
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
    },

    "bit_flip": {
        "name": "Flip All Bits",
        "description": "Turn every 0 into 1 and every 1 into 0",
        "goal": "Invert all bits",
        "initial_state": "flip",
        "accept_states": ["done"],
        "reject_states": [],
        "blank_symbol": "_",
        "default_input": "1010",

        "states": {
            "flip": {
                "label": "FLIP",
                "emoji": "🔄",
                "description": "Flipping bits one by one"
            },
            "done": {
                "label": "DONE",
                "emoji": "✅",
                "description": "Finished!"
            }
        },

        "rules": [
            {"state": "flip", "see": "0", "write": "1", "move": "right", "goto": "flip"},
            {"state": "flip", "see": "1", "write": "0", "move": "right", "goto": "flip"},
            {"state": "flip", "see": "_", "write": "_", "move": "stay", "goto": "done"}
        ],

        "transitions": {
            "flip,0": ["flip", "1", "R"],
            "flip,1": ["flip", "0", "R"],
            "flip,_": ["done", "_", "N"]
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
