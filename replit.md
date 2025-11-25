# Turing Machine Simulator

## Overview
A web-based educational Turing machine simulator that helps users understand how the simplest computer works. Features an interactive onboarding tutorial that teaches users to add 1 to a binary number.

**Project Type:** Flask web application with Python backend  
**Current State:** Fully functional and running  
**Last Updated:** November 25, 2025

## Recent Changes
- November 25, 2025: Imported from GitHub and configured for Replit environment
  - Changed port from 8080 to 5000 for Replit compatibility
  - Installed Python 3.11 and Flask dependencies
  - Configured workflow for web preview
  - Added deployment configuration

## Project Architecture

### Backend (Python/Flask)
- **app.py** - Main Flask application with API endpoints
- **turing_machine.py** - Core Turing machine implementation
- **history.py** - Undo/redo history management
- **examples.py** - Example programs and onboarding lessons

### Frontend
- **templates/index.html** - Main web interface
- **static/script.js** - JavaScript for UI interactions
- **static/style.css** - Styling

### Key Features
- Interactive tape visualization with head position
- Step-by-step execution or continuous run mode
- Undo/redo functionality with state history
- Educational onboarding tutorial (8 lessons)
- Multiple example programs (binary increment, palindrome checker, etc.)
- Adjustable execution speed
- Real-time state visualization

## API Endpoints
- `GET /` - Main web UI
- `POST /api/load` - Load program and tape
- `POST /api/step` - Execute one step
- `POST /api/run` - Run until halt or max steps
- `POST /api/reset` - Reset machine
- `POST /api/undo` - Undo last step
- `POST /api/redo` - Redo step
- `GET /api/lessons` - Get onboarding lessons
- `GET /api/examples` - List example programs
- `GET /api/examples/<id>` - Get specific example

## Development
- Server runs on port 5000 with debug mode enabled
- Flask automatically reloads on code changes
- Host: 0.0.0.0 (accessible via Replit webview)

## Dependencies
- Flask 3.1.2 (web framework)
- Python 3.11

## User Preferences
None yet - this is a fresh import.
