// Educational Turing Machine Simulator - Learn First, Then Play

// ==================== STATE GRAPH VISUALIZATION ====================

class StateGraph {
    constructor(containerId, states, transitions, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;

        this.states = states || {};
        this.transitions = transitions || {};

        // Calculate dynamic size based on number of states
        const numStates = Object.keys(this.states).length;
        const baseWidth = Math.max(400, numStates * 100);
        const baseHeight = Math.max(300, numStates * 60);

        this.options = {
            width: options.width || baseWidth,
            height: options.height || baseHeight,
            nodeRadius: options.nodeRadius || 40,
            animated: options.animated !== false
        };

        this.activeState = null;
        this.activeTransition = null;
        this.svg = null;
        this.nodeElements = {};
        this.edgeElements = {};

        this.render();
    }

    render() {
        if (!this.container) return;

        // Clear container
        this.container.innerHTML = '';

        // Create SVG
        this.svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        this.svg.setAttribute('width', '100%');
        this.svg.setAttribute('height', this.options.height);
        this.svg.setAttribute('viewBox', `0 0 ${this.options.width} ${this.options.height}`);
        this.svg.classList.add('state-graph-svg');

        // Add defs for arrow markers and gradients
        this.addDefs();

        // Calculate node positions
        const positions = this.calculatePositions();

        // Draw edges first (so they're behind nodes)
        this.drawEdges(positions);

        // Draw nodes
        this.drawNodes(positions);

        this.container.appendChild(this.svg);
    }

    addDefs() {
        const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');

        // Arrow marker
        const marker = document.createElementNS('http://www.w3.org/2000/svg', 'marker');
        marker.setAttribute('id', 'arrowhead');
        marker.setAttribute('markerWidth', '10');
        marker.setAttribute('markerHeight', '7');
        marker.setAttribute('refX', '9');
        marker.setAttribute('refY', '3.5');
        marker.setAttribute('orient', 'auto');

        const polygon = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
        polygon.setAttribute('points', '0 0, 10 3.5, 0 7');
        polygon.setAttribute('fill', '#888');
        polygon.classList.add('arrow-head');
        marker.appendChild(polygon);
        defs.appendChild(marker);

        // Active arrow marker (green)
        const markerActive = marker.cloneNode(true);
        markerActive.setAttribute('id', 'arrowhead-active');
        markerActive.querySelector('polygon').setAttribute('fill', '#4caf50');
        defs.appendChild(markerActive);

        // Node gradient
        const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
        gradient.setAttribute('id', 'node-gradient');
        gradient.setAttribute('x1', '0%');
        gradient.setAttribute('y1', '0%');
        gradient.setAttribute('x2', '100%');
        gradient.setAttribute('y2', '100%');

        const stop1 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        stop1.setAttribute('offset', '0%');
        stop1.setAttribute('stop-color', '#667eea');
        gradient.appendChild(stop1);

        const stop2 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        stop2.setAttribute('offset', '100%');
        stop2.setAttribute('stop-color', '#764ba2');
        gradient.appendChild(stop2);
        defs.appendChild(gradient);

        // Active node gradient (green)
        const gradientActive = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
        gradientActive.setAttribute('id', 'node-gradient-active');
        gradientActive.setAttribute('x1', '0%');
        gradientActive.setAttribute('y1', '0%');
        gradientActive.setAttribute('x2', '100%');
        gradientActive.setAttribute('y2', '100%');

        const stopA1 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        stopA1.setAttribute('offset', '0%');
        stopA1.setAttribute('stop-color', '#4caf50');
        gradientActive.appendChild(stopA1);

        const stopA2 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
        stopA2.setAttribute('offset', '100%');
        stopA2.setAttribute('stop-color', '#2e7d32');
        gradientActive.appendChild(stopA2);
        defs.appendChild(gradientActive);

        this.svg.appendChild(defs);
    }

    calculatePositions() {
        const stateIds = Object.keys(this.states);
        const positions = {};
        const cx = this.options.width / 2;
        const cy = this.options.height / 2;
        const n = stateIds.length;

        if (n <= 3) {
            // Triangle/line layout for 2-3 states
            if (n === 1) {
                positions[stateIds[0]] = { x: cx, y: cy };
            } else if (n === 2) {
                positions[stateIds[0]] = { x: cx - 100, y: cy };
                positions[stateIds[1]] = { x: cx + 100, y: cy };
            } else {
                // Triangle
                positions[stateIds[0]] = { x: 100, y: 80 };
                positions[stateIds[1]] = { x: this.options.width - 100, y: 80 };
                positions[stateIds[2]] = { x: cx, y: this.options.height - 80 };
            }
        } else if (n <= 6) {
            // Circle layout with better spacing
            const angleStep = (2 * Math.PI) / n;
            const radius = Math.min(this.options.width, this.options.height) / 2.5;

            stateIds.forEach((stateId, i) => {
                const angle = -Math.PI / 2 + i * angleStep;
                positions[stateId] = {
                    x: cx + radius * Math.cos(angle),
                    y: cy + radius * Math.sin(angle)
                };
            });
        } else {
            // Grid layout for many states
            const cols = Math.ceil(Math.sqrt(n));
            const rows = Math.ceil(n / cols);
            const cellWidth = this.options.width / (cols + 1);
            const cellHeight = this.options.height / (rows + 1);

            stateIds.forEach((stateId, i) => {
                const col = i % cols;
                const row = Math.floor(i / cols);
                positions[stateId] = {
                    x: cellWidth * (col + 1),
                    y: cellHeight * (row + 1)
                };
            });
        }

        return positions;
    }

    drawNodes(positions) {
        const r = this.options.nodeRadius;

        for (const [stateId, state] of Object.entries(this.states)) {
            const pos = positions[stateId];
            if (!pos) continue;

            const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            group.classList.add('state-node');
            group.setAttribute('data-state', stateId);

            // Circle
            const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
            circle.setAttribute('cx', pos.x);
            circle.setAttribute('cy', pos.y);
            circle.setAttribute('r', r);
            circle.setAttribute('fill', 'url(#node-gradient)');
            circle.classList.add('node-circle');
            group.appendChild(circle);

            // Emoji
            const emoji = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            emoji.setAttribute('x', pos.x);
            emoji.setAttribute('y', pos.y - 5);
            emoji.setAttribute('text-anchor', 'middle');
            emoji.setAttribute('dominant-baseline', 'middle');
            emoji.setAttribute('font-size', '18');
            emoji.textContent = state.emoji || '●';
            group.appendChild(emoji);

            // Label - truncate if too long
            let labelText = state.label || stateId.toUpperCase();
            const maxLen = 8;
            if (labelText.length > maxLen) {
                labelText = labelText.substring(0, maxLen - 1) + '…';
            }

            const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
            label.setAttribute('x', pos.x);
            label.setAttribute('y', pos.y + 16);
            label.setAttribute('text-anchor', 'middle');
            label.setAttribute('dominant-baseline', 'middle');
            label.setAttribute('font-size', '10');
            label.setAttribute('font-weight', 'bold');
            label.setAttribute('fill', 'white');
            label.textContent = labelText;
            group.appendChild(label);

            this.svg.appendChild(group);
            this.nodeElements[stateId] = group;
        }
    }

    drawEdges(positions) {
        // Group transitions by from-to pair
        const edgeMap = {};

        for (const [key, value] of Object.entries(this.transitions)) {
            const [fromState, symbol] = key.split(',');
            const toState = value[0];
            const writeSymbol = value[1];
            const direction = value[2];

            const edgeKey = `${fromState}->${toState}`;
            if (!edgeMap[edgeKey]) {
                edgeMap[edgeKey] = [];
            }
            edgeMap[edgeKey].push({ symbol, writeSymbol, direction, key });
        }

        for (const [edgeKey, transitions] of Object.entries(edgeMap)) {
            const [fromState, toState] = edgeKey.split('->');
            const fromPos = positions[fromState];
            const toPos = positions[toState];

            if (!fromPos || !toPos) continue;

            const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            group.classList.add('transition-group');
            group.setAttribute('data-from', fromState);
            group.setAttribute('data-to', toState);

            if (fromState === toState) {
                // Self-loop
                this.drawSelfLoop(group, fromPos, transitions);
            } else {
                // Regular edge
                this.drawEdge(group, fromPos, toPos, transitions);
            }

            this.svg.appendChild(group);

            // Store reference for each transition key
            transitions.forEach(t => {
                this.edgeElements[t.key] = group;
            });
        }
    }

    drawSelfLoop(group, pos, transitions) {
        const r = this.options.nodeRadius;

        // Draw loop arc above the node
        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        const loopRadius = 25;
        const startX = pos.x - 15;
        const startY = pos.y - r;
        const endX = pos.x + 15;
        const endY = pos.y - r;

        path.setAttribute('d', `M ${startX} ${startY}
            A ${loopRadius} ${loopRadius} 0 1 1 ${endX} ${endY}`);
        path.setAttribute('fill', 'none');
        path.setAttribute('stroke', '#888');
        path.setAttribute('stroke-width', '2');
        path.setAttribute('marker-end', 'url(#arrowhead)');
        path.classList.add('transition-arrow');
        group.appendChild(path);

        // Label
        const labelText = transitions.map(t => {
            const sym = t.symbol === '_' ? '␣' : t.symbol;
            return sym;
        }).join(',');

        const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        label.setAttribute('x', pos.x);
        label.setAttribute('y', pos.y - r - loopRadius - 8);
        label.setAttribute('text-anchor', 'middle');
        label.setAttribute('font-size', '10');
        label.setAttribute('fill', '#666');
        label.textContent = labelText;
        group.appendChild(label);
    }

    drawEdge(group, fromPos, toPos, transitions) {
        const r = this.options.nodeRadius;

        // Calculate edge points (from circle edge to circle edge)
        const dx = toPos.x - fromPos.x;
        const dy = toPos.y - fromPos.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        const nx = dx / dist;
        const ny = dy / dist;

        const startX = fromPos.x + nx * r;
        const startY = fromPos.y + ny * r;
        const endX = toPos.x - nx * (r + 8);
        const endY = toPos.y - ny * (r + 8);

        // Curved path
        const midX = (startX + endX) / 2;
        const midY = (startY + endY) / 2;
        const curvature = 20;
        const cpX = midX - ny * curvature;
        const cpY = midY + nx * curvature;

        const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
        path.setAttribute('d', `M ${startX} ${startY} Q ${cpX} ${cpY} ${endX} ${endY}`);
        path.setAttribute('fill', 'none');
        path.setAttribute('stroke', '#888');
        path.setAttribute('stroke-width', '2');
        path.setAttribute('marker-end', 'url(#arrowhead)');
        path.classList.add('transition-arrow');
        group.appendChild(path);

        // Label
        const labelText = transitions.map(t => {
            const sym = t.symbol === '_' ? '␣' : t.symbol;
            return sym;
        }).join(',');

        const label = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        label.setAttribute('x', cpX);
        label.setAttribute('y', cpY - 5);
        label.setAttribute('text-anchor', 'middle');
        label.setAttribute('font-size', '10');
        label.setAttribute('fill', '#666');
        label.setAttribute('class', 'edge-label');
        label.textContent = labelText;
        group.appendChild(label);
    }

    setActiveState(stateId) {
        // Remove active from all nodes
        for (const [id, node] of Object.entries(this.nodeElements)) {
            node.classList.remove('active');
            const circle = node.querySelector('.node-circle');
            if (circle) {
                circle.setAttribute('fill', 'url(#node-gradient)');
            }
        }

        // Set active node
        if (stateId && this.nodeElements[stateId]) {
            const node = this.nodeElements[stateId];
            node.classList.add('active');
            const circle = node.querySelector('.node-circle');
            if (circle) {
                circle.setAttribute('fill', 'url(#node-gradient-active)');
            }
        }

        this.activeState = stateId;
    }

    animateTransition(fromState, toState, symbol) {
        if (!this.options.animated) return;

        const key = `${fromState},${symbol}`;
        const edge = this.edgeElements[key];

        if (edge) {
            // Add active class
            edge.classList.add('active');
            const path = edge.querySelector('.transition-arrow');
            if (path) {
                path.setAttribute('stroke', '#4caf50');
                path.setAttribute('stroke-width', '3');
                path.setAttribute('marker-end', 'url(#arrowhead-active)');
            }

            // Remove after animation
            setTimeout(() => {
                edge.classList.remove('active');
                if (path) {
                    path.setAttribute('stroke', '#888');
                    path.setAttribute('stroke-width', '2');
                    path.setAttribute('marker-end', 'url(#arrowhead)');
                }
            }, 500);
        }
    }

    clearActiveTransition() {
        // Reset all edges to normal state
        Object.values(this.edgeElements).forEach(edge => {
            edge.classList.remove('active');
            const path = edge.querySelector('.transition-arrow');
            if (path) {
                path.setAttribute('stroke', '#888');
                path.setAttribute('stroke-width', '2');
                path.setAttribute('marker-end', 'url(#arrowhead)');
            }
        });
    }

    update(states, transitions) {
        this.states = states || this.states;
        this.transitions = transitions || this.transitions;
        this.nodeElements = {};
        this.edgeElements = {};
        this.render();
    }
}

// ==================== TURING SIMULATOR ====================

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

        // State graph
        this.stateGraph = null;

        // Skip onboarding flag (for direct simulator access)
        this.skipOnboarding = false;
    }

    init() {
        this.initElements();
        this.bindEvents();

        if (this.skipOnboarding) {
            // Skip lessons, go directly to simulator
            this.loadBinaryIncrement();
        } else {
            this.loadLessons();
        }
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
        // Lesson navigation (may not exist on simulator page)
        if (this.btnLessonPrev) this.btnLessonPrev.addEventListener('click', () => this.prevLesson());
        if (this.btnLessonNext) this.btnLessonNext.addEventListener('click', () => this.nextLesson());
        if (this.btnStartSimulator) this.btnStartSimulator.addEventListener('click', () => this.startSimulator());
        if (this.btnReviewLessons) this.btnReviewLessons.addEventListener('click', () => this.reviewLessons());

        // Simulator controls
        if (this.btnStep) this.btnStep.addEventListener('click', () => this.step());
        if (this.btnRun) this.btnRun.addEventListener('click', () => this.run());
        if (this.btnPause) this.btnPause.addEventListener('click', () => this.pause());
        if (this.btnReset) this.btnReset.addEventListener('click', () => this.reset());
        if (this.btnSetTape) this.btnSetTape.addEventListener('click', () => this.setTape());

        // Challenge mode (may not exist on simulator page)
        if (this.btnStartChallenge) this.btnStartChallenge.addEventListener('click', () => this.startChallengeMode());
        if (this.btnBackToSimulator) this.btnBackToSimulator.addEventListener('click', () => this.backToSimulator());
        if (this.btnNewChallenge) this.btnNewChallenge.addEventListener('click', () => this.getChallenge());
        if (this.btnCheckPlan) this.btnCheckPlan.addEventListener('click', () => this.checkPlan());
        if (this.btnRunSolution) this.btnRunSolution.addEventListener('click', () => this.runGeneratedSolution());
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

        // Initialize lesson graph if this is the "states" lesson
        if (lesson.id === 'states') {
            // Binary increment example states and transitions for the lesson graph
            const states = {
                scan: { label: 'SCAN', emoji: '🔍', description: 'Looking for end' },
                add: { label: 'ADD', emoji: '➕', description: 'Adding 1' },
                done: { label: 'DONE', emoji: '✅', description: 'Finished' }
            };
            const transitions = {
                'scan,0': ['scan', '0', 'R'],
                'scan,1': ['scan', '1', 'R'],
                'scan,_': ['add', '_', 'L'],
                'add,0': ['done', '1', 'N'],
                'add,1': ['add', '0', 'L'],
                'add,_': ['done', '1', 'N']
            };
            new StateGraph('lesson-graph', states, transitions, { animated: false });
        }

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

            // Initialize state graph
            this.stateGraph = new StateGraph(
                'simulator-graph',
                example.states,
                example.transitions,
                { animated: true }
            );
            // Set initial active state
            this.stateGraph.setActiveState(example.initial_state);

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

            // Update state graph
            if (this.stateGraph && data.machine.last_transition) {
                const t = data.machine.last_transition;
                this.stateGraph.animateTransition(t.from_state, t.to_state, t.read);
                this.stateGraph.setActiveState(data.machine.current_state);
            }

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

            // Reset state graph to initial state
            if (this.stateGraph && this.machineState) {
                this.stateGraph.clearActiveTransition();
                this.stateGraph.setActiveState(this.machineState.current_state);
            }
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

// Initialize (for old index.html page with onboarding)
document.addEventListener('DOMContentLoaded', () => {
    // Only auto-init if we have the onboarding element (old index.html)
    // For new pages, initialization happens in their own script blocks
    if (document.getElementById('onboarding')) {
        window.simulator = new TuringSimulator();
        window.simulator.init();
    }
});
