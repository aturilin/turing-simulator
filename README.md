# Turing Machine Simulator

A web-based Turing machine simulator with interactive visualization, state diagrams, and undo/redo functionality.

## Features

- Interactive tape visualization with head position indicator
- SVG state diagram that highlights the current state
- Step-by-step execution or continuous run mode
- Adjustable execution speed
- Undo/redo functionality
- Multiple example programs included
- JSON-based program format
- Execution log

## Installation

1. Clone the repository:
```bash
git clone https://github.com/aturilin/turing-simulator.git
cd turing-simulator
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:5000`

3. Select an example program or write your own in JSON format

4. Enter initial tape content (optional)

5. Click "Load Program" to initialize the machine

6. Use the controls:
   - **Step**: Execute one transition
   - **Run**: Run continuously until halt
   - **Pause**: Stop continuous execution
   - **Reset**: Reset to initial state
   - **Undo/Redo**: Navigate through history

## Program Format

Programs are defined in JSON format:

```json
{
  "name": "Program Name",
  "description": "What this program does",
  "initial_state": "q0",
  "accept_states": ["halt"],
  "reject_states": [],
  "blank_symbol": "_",
  "transitions": {
    "state,symbol": ["new_state", "write_symbol", "direction"]
  }
}
```

### Transition Format

- Key: `"current_state,read_symbol"`
- Value: `["next_state", "write_symbol", "direction"]`
- Direction: `"L"` (left), `"R"` (right), or `"N"` (stay)

### Example: Binary Increment

```json
{
  "name": "Binary Increment",
  "initial_state": "right",
  "accept_states": ["halt"],
  "blank_symbol": "_",
  "transitions": {
    "right,0": ["right", "0", "R"],
    "right,1": ["right", "1", "R"],
    "right,_": ["add", "_", "L"],
    "add,0": ["halt", "1", "N"],
    "add,1": ["add", "0", "L"],
    "add,_": ["halt", "1", "N"]
  }
}
```

## Included Examples

1. **Binary Increment** - Increments a binary number by 1
2. **Palindrome Checker** - Checks if a binary string is a palindrome
3. **Unary Addition** - Adds two unary numbers (e.g., `111+11` = `11111`)
4. **Busy Beaver (3-state)** - The famous 3-state busy beaver
5. **Binary Double** - Doubles a binary number (appends 0)

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web UI |
| `/api/load` | POST | Load program and tape |
| `/api/step` | POST | Execute one step |
| `/api/run` | POST | Run to completion |
| `/api/reset` | POST | Reset machine |
| `/api/undo` | POST | Undo last step |
| `/api/redo` | POST | Redo step |
| `/api/examples` | GET | List examples |
| `/api/examples/<id>` | GET | Get specific example |

## License

MIT
