// Educational Turing Machine Simulator - Learn First, Then Play

class TuringSimulator {
    constructor() {
        this.lessons = [];
        this.currentLesson = 0;
        this.machineState = null;
        this.programData = null;
        this.currentExample = null;
        this.isRunning = false;
        this.runInterval = null;

        // Challenge mode state
        this.currentChallenge = null;
        this.generatedRules = null;
        this.exampleCompleted = false;

        this.initElements();
        this.bindEvents();
        this.loadLessons();
    }

    initElements() {
        // Onboarding elements
        this.onboarding = document.getElementById('onboarding');
        this.simulator = document.getElementById('simulator');
        this.lessonContent = document.getElementById('lesson-content');
        this.lessonCurrent = document.getElementById('lesson-current');
        this.lessonTotal = document.getElementById('lesson-total');
        this.progressFill = document.getElementById('progress-fill');
        this.btnLessonPrev = document.getElementById('btn-lesson-prev');
        this.btnLessonNext = document.getElementById('btn-lesson-next');
        this.btnStartSimulator = document.getElementById('btn-start-simulator');
        this.btnReviewLessons = document.getElementById('btn-review-lessons');

        // Tape elements
        this.tape = document.getElementById('tape');
        this.tapeInput = document.getElementById('tape-input');
        this.currentStateEl = document.getElementById('current-state');
        this.stateEmoji = document.getElementById('state-emoji');
        this.stateDescription = document.getElementById('state-description');
        this.statusBadge = document.getElementById('status-badge');

        // Next action elements
        this.nextActionBox = document.getElementById('next-action-box');
        this.nextState = document.getElementById('next-state');
        this.nextSymbol = document.getElementById('next-symbol');
        this.nextActionText = document.getElementById('next-action-text');
        this.nextActionWhy = document.getElementById('next-action-why');
        this.goalDisplay = document.getElementById('goal-display');

        // Controls
        this.btnStep = document.getElementById('btn-step');
        this.btnRun = document.getElementById('btn-run');
        this.btnPause = document.getElementById('btn-pause');
        this.btnReset = document.getElementById('btn-reset');
        this.btnSetTape = document.getElementById('btn-set-tape');
        this.speedSlider = document.getElementById('speed-slider');

        // Rules
        this.rulesListScan = document.getElementById('rules-list-scan');
        this.rulesListAdd = document.getElementById('rules-list-add');

        // History
        this.historyLog = document.getElementById('history-log');

        // Challenge prompt
        this.challengePrompt = document.getElementById('challenge-prompt');
        this.btnStartChallenge = document.getElementById('btn-start-challenge');

        // Challenge mode elements
        this.challengeMode = document.getElementById('challenge-mode');
        this.btnBackToSimulator = document.getElementById('btn-back-to-simulator');
        this.challengeTask = document.getElementById('challenge-task');
        this.challengeExamples = document.getElementById('challenge-examples');
        this.btnNewChallenge = document.getElementById('btn-new-challenge');
        this.studentPlan = document.getElementById('student-plan');
        this.btnCheckPlan = document.getElementById('btn-check-plan');
        this.feedbackSection = document.getElementById('feedback-section');
        this.feedbackBox = document.getElementById('feedback-box');
        this.feedbackIcon = document.getElementById('feedback-icon');
        this.feedbackMessage = document.getElementById('feedback-message');
        this.feedbackHint = document.getElementById('feedback-hint');
        this.btnRunSolution = document.getElementById('btn-run-solution');
        this.loadingOverlay = document.getElementById('loading-overlay');
    }

    bindEvents() {
        // Lesson navigation
        this.btnLessonPrev.addEventListener('click', () => this.prevLesson());
        this.btnLessonNext.addEventListener('click', () => this.nextLesson());
        this.btnStartSimulator.addEventListener('click', () => this.startSimulator());
        this.btnReviewLessons.addEventListener('click', () => this.reviewLessons());

        // Simulator controls
        this.btnStep.addEventListener('click', () => this.step());
        this.btnRun.addEventListener('click', () => this.run());
        this.btnPause.addEventListener('click', () => this.pause());
        this.btnReset.addEventListener('click', () => this.reset());
        this.btnSetTape.addEventListener('click', () => this.setTape());

        // Challenge mode
        this.btnStartChallenge.addEventListener('click', () => this.startChallengeMode());
        this.btnBackToSimulator.addEventListener('click', () => this.backToSimulator());
        this.btnNewChallenge.addEventListener('click', () => this.getChallenge());
        this.btnCheckPlan.addEventListener('click', () => this.checkPlan());
        this.btnRunSolution.addEventListener('click', () => this.runGeneratedSolution());
    }

    // ==================== ONBOARDING ====================

    async loadLessons() {
        try {
            const response = await fetch('/api/lessons');
            this.lessons = await response.json();
            this.lessonTotal.textContent = this.lessons.length;
            this.showLesson(0);
        } catch (error) {
            console.error('Failed to load lessons:', error);
        }
    }

    showLesson(index) {
        if (index < 0 || index >= this.lessons.length) return;

        this.currentLesson = index;
        const lesson = this.lessons[index];

        // Update content
        this.lessonContent.innerHTML = lesson.content;

        // Update progress
        this.lessonCurrent.textContent = index + 1;
        const progress = ((index + 1) / this.lessons.length) * 100;
        this.progressFill.style.width = progress + '%';

        // Update navigation buttons
        this.btnLessonPrev.disabled = index === 0;

        if (index === this.lessons.length - 1) {
            this.btnLessonNext.classList.add('hidden');
            this.btnStartSimulator.classList.remove('hidden');
        } else {
            this.btnLessonNext.classList.remove('hidden');
            this.btnStartSimulator.classList.add('hidden');
        }
    }

    prevLesson() {
        if (this.currentLesson > 0) {
            this.showLesson(this.currentLesson - 1);
        }
    }

    nextLesson() {
        if (this.currentLesson < this.lessons.length - 1) {
            this.showLesson(this.currentLesson + 1);
        }
    }

    startSimulator() {
        // Hide onboarding, show simulator
        this.onboarding.classList.add('hidden');
        this.simulator.classList.remove('hidden');

        // Load the binary increment example
        this.loadBinaryIncrement();
    }

    reviewLessons() {
        // Show onboarding, hide simulator
        this.simulator.classList.add('hidden');
        this.onboarding.classList.remove('hidden');
        this.showLesson(0);
    }

    // ==================== SIMULATOR ====================

    async loadBinaryIncrement() {
        try {
            const response = await fetch('/api/examples/binary_increment');
            const example = await response.json();

            this.currentExample = example;
            this.tapeInput.value = example.default_input || '1011';

            // Load program via API
            await this.loadProgram(example);

            // Render rules as cards
            this.renderRules(example.rules || []);

            // Show goal
            if (example.goal) {
                this.goalDisplay.innerHTML = `<strong>Goal:</strong> ${example.goal}`;
            }

            // Show initial next action
            this.updateNextAction();

            // Clear history
            this.historyLog.innerHTML = '';

            // Hide challenge prompt initially
            this.challengePrompt.classList.add('hidden');
            this.exampleCompleted = false;

        } catch (error) {
            console.error('Failed to load example:', error);
        }
    }

    async loadProgram(example) {
        const program = {
            initial_state: example.initial_state,
            accept_states: example.accept_states,
            reject_states: example.reject_states || [],
            blank_symbol: example.blank_symbol,
            transitions: example.transitions
        };

        try {
            const response = await fetch('/api/load', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ program, tape: this.tapeInput.value })
            });

            const data = await response.json();
            this.machineState = data.machine;
            this.programData = data.program;
            this.updateUI();
        } catch (error) {
            console.error('Failed to load program:', error);
        }
    }

    async setTape() {
        if (!this.currentExample) return;

        try {
            const response = await fetch('/api/reset', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tape: this.tapeInput.value })
            });

            const data = await response.json();
            this.machineState = data.machine;
            this.updateUI();
            this.updateNextAction();
            this.historyLog.innerHTML = '';
            this.clearActiveRules();
        } catch (error) {
            console.error('Failed to set tape:', error);
        }
    }

    async step() {
        if (!this.machineState || this.machineState.halted) return;

        try {
            const response = await fetch('/api/step', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const data = await response.json();
            this.machineState = data.machine;
            this.updateUI();
            this.addHistoryEntry(data.machine);
            this.updateNextAction();

            // Check if example completed
            if (this.machineState.halted && this.machineState.accepted && !this.exampleCompleted) {
                this.showChallengePrompt();
            }
        } catch (error) {
            console.error('Step failed:', error);
        }
    }

    async run() {
        if (!this.machineState || this.machineState.halted) return;

        this.isRunning = true;
        this.btnRun.disabled = true;
        this.btnPause.disabled = false;

        const speed = this.speedSlider.value;
        const delay = Math.max(50, 1000 - speed * 10);

        const runStep = async () => {
            if (!this.isRunning || !this.machineState || this.machineState.halted) {
                this.pause();
                return;
            }

            await this.step();

            if (this.isRunning && !this.machineState.halted) {
                this.runInterval = setTimeout(runStep, delay);
            } else {
                this.pause();
            }
        };

        runStep();
    }

    pause() {
        this.isRunning = false;
        if (this.runInterval) {
            clearTimeout(this.runInterval);
            this.runInterval = null;
        }
        this.btnRun.disabled = false;
        this.btnPause.disabled = true;
    }

    async reset() {
        this.pause();

        try {
            const response = await fetch('/api/reset', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ tape: this.tapeInput.value })
            });

            const data = await response.json();
            this.machineState = data.machine;
            this.updateUI();
            this.updateNextAction();
            this.historyLog.innerHTML = '';
            this.clearActiveRules();
        } catch (error) {
            console.error('Reset failed:', error);
        }
    }

    showChallengePrompt() {
        this.exampleCompleted = true;
        this.challengePrompt.classList.remove('hidden');
    }

    // ==================== UI UPDATES ====================

    updateUI() {
        if (!this.machineState) return;

        this.renderTape();
        this.updateStateDisplay();
    }

    renderTape() {
        if (!this.machineState || !this.machineState.tape) return;

        const { cells, head_position } = this.machineState.tape;
        this.tape.innerHTML = '';

        const positions = Object.keys(cells).map(Number).sort((a, b) => a - b);
        let headCellElement = null;

        positions.forEach(pos => {
            const cell = document.createElement('div');
            cell.className = 'tape-cell';
            cell.textContent = cells[pos] === '_' ? '' : cells[pos];

            if (pos === head_position) {
                cell.classList.add('head');
                headCellElement = cell;
            }
            if (cells[pos] === '_') {
                cell.classList.add('blank');
            }

            this.tape.appendChild(cell);
        });

        // Position head indicator
        if (headCellElement) {
            setTimeout(() => {
                const tapeWrapper = this.tape.parentElement;
                const headRect = headCellElement.getBoundingClientRect();
                const tapeRect = this.tape.getBoundingClientRect();
                const wrapperRect = tapeWrapper.getBoundingClientRect();

                const headIndicator = tapeWrapper.querySelector('.head-indicator');
                const headCenterX = headRect.left + headRect.width / 2 - tapeRect.left;
                headIndicator.style.left = headCenterX + 'px';
                headIndicator.style.transform = 'translateX(-50%)';

                // Scroll to center head
                const scrollLeft = headCellElement.offsetLeft - (wrapperRect.width / 2) + (headRect.width / 2);
                tapeWrapper.scrollLeft = scrollLeft;
            }, 0);
        }
    }

    updateStateDisplay() {
        const state = this.machineState.current_state;
        this.currentStateEl.textContent = state ? state.toUpperCase() : '-';

        // Get state info from example
        if (this.currentExample && this.currentExample.states && this.currentExample.states[state]) {
            const stateInfo = this.currentExample.states[state];
            this.stateEmoji.textContent = stateInfo.emoji || '';
            this.stateDescription.textContent = stateInfo.description || '';
        } else {
            this.stateEmoji.textContent = '';
            this.stateDescription.textContent = '';
        }

        // Update status badge
        this.statusBadge.className = 'status-badge';
        if (this.machineState.halted) {
            if (this.machineState.accepted) {
                this.statusBadge.textContent = 'DONE!';
                this.statusBadge.classList.add('done');
            } else {
                this.statusBadge.textContent = 'STOPPED';
                this.statusBadge.classList.add('halted');
            }
        } else {
            this.statusBadge.textContent = 'READY';
            this.statusBadge.classList.add('running');
        }

        // Update button states
        this.btnStep.disabled = this.machineState.halted;
        this.btnRun.disabled = this.machineState.halted || this.isRunning;
    }

    updateNextAction() {
        if (!this.machineState || !this.currentExample) return;

        // Get current state and symbol under head
        const currentState = this.machineState.current_state;
        const headPos = this.machineState.tape.head_position;
        const currentSymbol = this.machineState.tape.cells[headPos] || '_';

        // Update display of current situation
        this.nextState.textContent = currentState ? currentState.toUpperCase() : '-';
        this.nextSymbol.textContent = currentSymbol === '_' ? '(blank)' : currentSymbol;

        // Get state info
        const stateInfo = this.currentExample.states?.[currentState];

        if (this.machineState.halted) {
            // Machine is done
            this.nextActionBox.classList.add('done');
            this.nextActionText.textContent = this.machineState.accepted ?
                'Finished! The calculation is complete.' :
                'Stopped - no matching rule found.';
            this.nextActionWhy.textContent = '';
            this.clearActiveRules();
        } else {
            this.nextActionBox.classList.remove('done');

            // Get explanation for next action
            const key = `${currentState},${currentSymbol}`;
            const explanation = this.currentExample.next_action_explanations?.[key];

            if (explanation) {
                this.nextActionText.textContent = explanation.action;
                this.nextActionWhy.textContent = explanation.why;
            } else {
                this.nextActionText.textContent = 'Processing...';
                this.nextActionWhy.textContent = '';
            }

            // Highlight the active rule BEFORE execution
            this.highlightActiveRule(currentState, currentSymbol);
        }
    }

    renderRules(rules) {
        this.rulesListScan.innerHTML = '';
        this.rulesListAdd.innerHTML = '';

        rules.forEach((rule, index) => {
            const card = document.createElement('div');
            card.className = 'rule-card';
            card.dataset.state = rule.state;
            card.dataset.see = rule.see;

            const moveText = {
                'right': 'move RIGHT',
                'left': 'move LEFT',
                'stay': 'STOP'
            }[rule.move] || rule.move;

            const seeDisplay = rule.see === '_' ? 'blank' : `"${rule.see}"`;
            const writeDisplay = rule.write === '_' ? 'blank' : `"${rule.write}"`;

            card.innerHTML = `
                <div class="action">
                    See <span class="see">${seeDisplay}</span> →
                    write ${writeDisplay}, ${moveText}
                </div>
                <div class="result">→ ${rule.goto.toUpperCase()}</div>
            `;

            if (rule.state === 'scan') {
                this.rulesListScan.appendChild(card);
            } else if (rule.state === 'add') {
                this.rulesListAdd.appendChild(card);
            }
        });
    }

    highlightActiveRule(state, symbol) {
        // Clear previous highlights
        this.clearActiveRules();

        // Find and highlight the matching rule
        const allCards = document.querySelectorAll('.rule-card');
        allCards.forEach(card => {
            if (card.dataset.state === state && card.dataset.see === symbol) {
                card.classList.add('active');
            }
        });
    }

    clearActiveRules() {
        const allCards = document.querySelectorAll('.rule-card');
        allCards.forEach(card => card.classList.remove('active'));
    }

    addHistoryEntry(machine) {
        const transition = machine.last_transition;
        if (!transition) return;

        const entry = document.createElement('div');
        entry.className = 'history-entry current';

        // Remove 'current' from previous entries
        const prevEntries = this.historyLog.querySelectorAll('.history-entry.current');
        prevEntries.forEach(e => e.classList.remove('current'));

        let text = '';
        if (transition.halted) {
            text = transition.reason === 'accepted' ? 'Finished!' : 'Stopped';
        } else {
            const moveSymbol = transition.direction === 'R' ? '→' :
                              transition.direction === 'L' ? '←' : '•';
            text = `${transition.from_state.toUpperCase()}: saw "${transition.read}" → wrote "${transition.write}", moved ${moveSymbol}`;
        }

        entry.innerHTML = `
            <span class="step-num">${machine.step_count}</span>
            <span class="step-text">${text}</span>
        `;

        this.historyLog.appendChild(entry);
        this.historyLog.scrollTop = this.historyLog.scrollHeight;
    }

    // ==================== CHALLENGE MODE ====================

    startChallengeMode() {
        // Hide simulator, show challenge mode
        this.simulator.classList.add('hidden');
        this.challengeMode.classList.remove('hidden');

        // Reset challenge state
        this.currentChallenge = null;
        this.generatedRules = null;
        this.studentPlan.value = '';
        this.feedbackSection.classList.add('hidden');
        this.btnRunSolution.classList.add('hidden');

        // Get a new challenge
        this.getChallenge();
    }

    backToSimulator() {
        // Hide challenge mode, show simulator
        this.challengeMode.classList.add('hidden');
        this.simulator.classList.remove('hidden');
    }

    async getChallenge() {
        this.loadingOverlay.classList.remove('hidden');
        this.challengeTask.innerHTML = '<p class="loading">Loading challenge...</p>';
        this.challengeExamples.innerHTML = '';

        // Reset feedback
        this.feedbackSection.classList.add('hidden');
        this.btnRunSolution.classList.add('hidden');
        this.studentPlan.value = '';

        try {
            const response = await fetch('/api/challenge');
            const challenge = await response.json();

            if (challenge.error) {
                this.challengeTask.innerHTML = `<p class="error">Error: ${challenge.error}</p>`;
                return;
            }

            this.currentChallenge = challenge;

            // Display challenge task
            this.challengeTask.innerHTML = `<p>${challenge.task}</p>`;

            // Display examples
            if (challenge.examples && challenge.examples.length > 0) {
                let examplesHtml = '<h4>Examples:</h4>';
                challenge.examples.forEach(ex => {
                    examplesHtml += `
                        <div class="example-item">
                            <span class="input">${ex.input}</span>
                            <span class="arrow">→</span>
                            <span class="output">${ex.output}</span>
                        </div>
                    `;
                });
                this.challengeExamples.innerHTML = examplesHtml;
            }

        } catch (error) {
            console.error('Failed to get challenge:', error);
            this.challengeTask.innerHTML = '<p class="error">Failed to load challenge. Please try again.</p>';
        } finally {
            this.loadingOverlay.classList.add('hidden');
        }
    }

    async checkPlan() {
        const plan = this.studentPlan.value.trim();

        if (!plan) {
            alert('Please describe your algorithm first!');
            return;
        }

        if (!this.currentChallenge) {
            alert('No challenge loaded. Please get a new challenge.');
            return;
        }

        this.loadingOverlay.classList.remove('hidden');

        try {
            const response = await fetch('/api/check-plan', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    challenge: this.currentChallenge,
                    plan: plan
                })
            });

            const result = await response.json();

            if (result.error) {
                this.showFeedback(false, `Error: ${result.error}`, '');
                return;
            }

            if (result.correct) {
                this.generatedRules = result.rules;
                this.showFeedback(true, result.feedback, '');
                this.btnRunSolution.classList.remove('hidden');
            } else {
                this.showFeedback(false, result.feedback, result.hint);
            }

        } catch (error) {
            console.error('Failed to check plan:', error);
            this.showFeedback(false, 'Failed to check plan. Please try again.', '');
        } finally {
            this.loadingOverlay.classList.add('hidden');
        }
    }

    showFeedback(isCorrect, message, hint) {
        this.feedbackSection.classList.remove('hidden');
        this.feedbackBox.className = 'feedback-box ' + (isCorrect ? 'correct' : 'wrong');
        this.feedbackIcon.textContent = isCorrect ? '🎉' : '💡';
        this.feedbackMessage.textContent = message;
        this.feedbackHint.textContent = hint || '';
    }

    async runGeneratedSolution() {
        if (!this.generatedRules) return;

        // Go back to simulator with the generated rules
        this.challengeMode.classList.add('hidden');
        this.simulator.classList.remove('hidden');

        // Load the generated rules as the current example
        this.currentExample = this.generatedRules;
        this.tapeInput.value = this.generatedRules.default_input || '';

        // Load program
        await this.loadProgram(this.generatedRules);

        // Render rules (dynamically create groups based on states)
        this.renderDynamicRules(this.generatedRules.rules || []);

        // Show goal
        this.goalDisplay.innerHTML = `<strong>Your Algorithm:</strong> ${this.generatedRules.name || 'Custom'}`;

        // Update next action
        this.updateNextAction();

        // Clear history
        this.historyLog.innerHTML = '';

        // Hide challenge prompt
        this.challengePrompt.classList.add('hidden');
    }

    renderDynamicRules(rules) {
        // Clear existing rules
        const rulesGroups = document.querySelector('.rules-groups');
        rulesGroups.innerHTML = '';

        // Group rules by state
        const rulesByState = {};
        rules.forEach(rule => {
            if (!rulesByState[rule.state]) {
                rulesByState[rule.state] = [];
            }
            rulesByState[rule.state].push(rule);
        });

        // Create a group for each state
        for (const [state, stateRules] of Object.entries(rulesByState)) {
            const stateInfo = this.currentExample.states?.[state] || {};
            const emoji = stateInfo.emoji || '📌';
            const label = stateInfo.label || state.toUpperCase();

            const group = document.createElement('div');
            group.className = 'rules-group';
            group.innerHTML = `
                <h3><span class="state-emoji-small">${emoji}</span> ${label}</h3>
                <div class="rules-list" id="rules-list-${state}"></div>
            `;

            const rulesList = group.querySelector('.rules-list');

            stateRules.forEach(rule => {
                const card = document.createElement('div');
                card.className = 'rule-card';
                card.dataset.state = rule.state;
                card.dataset.see = rule.see;

                const moveText = {
                    'right': 'move RIGHT',
                    'left': 'move LEFT',
                    'stay': 'STOP'
                }[rule.move] || rule.move;

                const seeDisplay = rule.see === '_' ? 'blank' : `"${rule.see}"`;
                const writeDisplay = rule.write === '_' ? 'blank' : `"${rule.write}"`;

                card.innerHTML = `
                    <div class="action">
                        See <span class="see">${seeDisplay}</span> →
                        write ${writeDisplay}, ${moveText}
                    </div>
                    <div class="result">→ ${rule.goto.toUpperCase()}</div>
                `;

                rulesList.appendChild(card);
            });

            rulesGroups.appendChild(group);
        }
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.simulator = new TuringSimulator();
});
