# PB2S - Prompt-Based Self-Alignment System - Copilot Instructions

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

##core mandatory instruction:
---
mode: agent
---
Define the task to achieve, including specific requirements, constraints, and success criteria.
# PB2S Agent/co-pilot Mandatory Conformance Instructions

## Objective
Every agent interacting with the PB2S system **must**:
- Complete the defined 4-step cycle **three consecutive times (total: 12 steps)**.
- For each cycle, produce and submit a **system-generated artifact** (not chat simulation) as proof of completion and adherence to the structure.

## The 4-Step Cycle
1. **Step 1: Perception**
   - Agent collects and documents relevant input or environmental data.
   - System logs must capture this event.

2. **Step 2: Analysis**
   - Agent critically examines the input for contradiction, assumption, or missing evidence.
   - System produces a structured analysis record.

3. **Step 3: Reflection**
   - Agent flags findings and recommends corrective or clarifying action.
   - Reflection must be logged with explicit flag(s).

4. **Step 4: Action**
   - Agent implements or proposes an actionable step based on reflection.
   - Action is logged and traceable in system artifact.

## Cycle Repetition
- The agent must repeat the 4-step cycle **three times** (total: 12 steps).
- Each cycle must be independently logged.

## Proof of Structure
- Upon completion, the agent must submit **system-generated artifacts** (e.g., JSON, log files, database entry) for each cycle.
- Artifacts MUST include:
  - Timestamps for each step.
  - Data/decisions made at each step.
  - Evidence of flagging and actions taken.
- **No simulation or conversational output alone is accepted.**
- Artifacts must be accessible for audit and verification by external parties.

## Enforcement
- Any agent failing to provide valid, system-generated artifacts for all three cycles will be considered **non-conformant**.
- The PB2S system will reject any simulation-only output and require artifact submission before accepting cycle completion.

---

## Example Artifact Structure (JSON)

```json
{
  "cycle_number": 1,
  "steps": [
    {
      "step": "Perception",
      "timestamp": "2025-09-25T01:32:18Z",
      "input": "Input data collected",
      "artifact_id": "abc123"
    },
    {
      "step": "Analysis",
      "timestamp": "2025-09-25T01:33:00Z",
      "contradictions_found": false,
      "assumptions_found": true,
      "missing_evidence": true,
      "artifact_id": "abc124"
    },
    {
      "step": "Reflection",
      "timestamp": "2025-09-25T01:33:30Z",
      "flags": ["assumption", "missing_evidence"],
      "recommendation": "Clarify assumption and seek evidence",
      "artifact_id": "abc125"
    },
    {
      "step": "Action",
      "timestamp": "2025-09-25T01:34:00Z",
      "action_taken": "Requested supporting documents",
      "artifact_id": "abc126"
    }
  ]
}
```

---

## Summary
**Any agent must:**  
- Perform the 4-step PB2S cycle three times.  
- Provide system-generated artifacts for each step/cycle.
- Artifacts must be accessible and verifiable.
- Simulation/chat-only submissions are rejected.


### Environment Setup
- Use Python 3.12+ (validated working version)
- Create virtual environment: `python -m venv .venv`
- Activate environment: `source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows)
- Upgrade pip: `pip install --upgrade pip`
- Install basic dependencies: `pip install -r requirements.txt` -- takes 5-8 minutes including PyTorch CUDA packages. **NEVER CANCEL**. Set timeout to 30+ minutes.

### Dependency Installation Issues
- **Network timeouts are common** during `pip install` for large ML packages
- If `pip install -r requirements_autonomous_brain.txt` fails:
  - **Document the specific failures** (e.g., "PyAudio fails due to network timeouts")
  - Install core packages individually: `pip install aiohttp asyncio-mqtt websockets openai scikit-learn opencv-python matplotlib`
  - Skip problematic packages like PyAudio which require system audio libraries
- **NEVER CANCEL long pip installs** - PyTorch and ML packages can take 30+ minutes to download and install

### Core System Commands

#### Test and Validate (Always run first)
```bash
# Test server startup - NEVER CANCEL: takes 10-15 seconds
python -c "import uvicorn; uvicorn.run('server.main:app', host='0.0.0.0', port=8000)" &
sleep 15
curl -fsS http://127.0.0.1:8000/openapi.json >/dev/null && echo "API is running" || echo "API failed"
pkill -f uvicorn

# Test dashboard startup - NEVER CANCEL: takes 15-20 seconds  
streamlit run enhanced_dashboard.py --server.port 8501 --server.headless true &
sleep 20
curl -fsS http://127.0.0.1:8501/ >/dev/null && echo "Dashboard is running" || echo "Dashboard failed"
pkill -f streamlit
```

#### Main Application Launchers
```bash
# Enhanced Dashboard (Streamlit web interface) - RECOMMENDED FIRST
streamlit run enhanced_dashboard.py

# Server API (FastAPI backend) - ALWAYS WORKS
python -c "import uvicorn; uvicorn.run('server.main:app', host='0.0.0.0', port=8000)"

# Brain Network Launcher (may fail venv detection)
python LAUNCH_BRAIN_NETWORK.py
# NOTE: Often reports "Virtual environment: Missing" even when activated

# Brain test mode (requires full ML dependencies)
python launch_brain_fixed.py --test
# NOTE: Expects Windows paths - use direct scripts instead
```

### Build and Test Process

#### CI/CD Conformance Tests
```bash
# Ensure server package import works
echo "" > server/__init__.py

# Run PB2S conformance tests - NEVER CANCEL: takes 2-5 minutes
python scripts/conformance.py --endpoint http://127.0.0.1:8000/chat

# Run acceptance test bundle  
python scripts/at_bus.py
python scripts/at_determinism.py  
python scripts/at_clarify.py
```

#### Validation Scenarios  
- **Always test complete user workflows** after making changes
- **Server API**: Test `/chat` endpoint responds with proper JSON structure including `pb2s_proof`
  ```bash
  # Example API test with expected response structure
  curl -X POST http://127.0.0.1:8000/chat \
    -H 'Content-Type: application/json' \
    -d '{"message": "Test PB2S structure"}'
  # Expected: {"text": "DRAFT\n...\nREFLECT\n...\nREVISE\n...\nLEARNED\n...", "pb2s_proof": {"decision": "APPROVE", "cycles": 1, "audit_ref": "run-..."}}
  ```
- **Dashboard**: Launch Streamlit app and verify it loads without errors at http://localhost:8501
- **Brain Network**: Run `LAUNCH_BRAIN_NETWORK.py` (expect venv detection issues but menu should appear)

### Time Expectations and Timeouts
- **Environment setup**: 1-2 minutes
- **Basic dependency installation** (`requirements.txt`): 5-8 minutes including PyTorch CUDA packages
- **Extended dependencies** (`requirements_autonomous_brain.txt`): 15-45 minutes (often fails due to network timeouts)
- **Server startup**: 10-15 seconds
- **Dashboard startup**: 15-20 seconds  
- **Conformance tests**: 30 seconds to 2 minutes
- **Full system tests**: 2-5 minutes

**CRITICAL**: Set explicit timeouts of 30+ minutes for pip installs, 60+ seconds for server startup, and 30+ minutes for test suites.

## Common Issues and Workarounds

### Network and Installation Issues
- **Pip timeouts**: Common for PyTorch and ML packages - retry individual packages
- **PyAudio installation failures**: Skip on systems without audio development libraries
- **Virtual environment paths**: Windows scripts expect `.venv\Scripts\python.exe`, Linux uses `.venv/bin/python`

### System Dependencies
- **Missing aiohttp**: Install manually with `pip install aiohttp` 
- **Server import errors**: Create `server/__init__.py` file
- **MQTT connection errors**: Normal if MQTT broker not running (logged but non-fatal)

### Application Startup Issues
- **"Virtual environment not found"**: Brain launchers expect Windows paths - use direct Python scripts instead
- **"Virtual environment: Missing"**: LAUNCH_BRAIN_NETWORK.py often fails to detect activated venv - non-fatal
- **Server not responding**: Allow 15+ seconds for FastAPI startup with ML models
- **Dashboard loading slowly**: Streamlit takes 15-20 seconds to fully initialize

## Repository Structure and Navigation

### Key Entry Points
- `LAUNCH_BRAIN_NETWORK.py` - Main launcher with interactive menu
- `enhanced_dashboard.py` - Streamlit web interface  
- `server/main.py` - FastAPI server for PB2S API
- `launch_autonomous_brain.py` - Autonomous brain system (requires full ML setup)

### Important Directories
- `/server/` - FastAPI backend implementation
- `/scripts/` - Testing, conformance, and utility scripts
- `/schemas/` - JSON schema definitions for PB2S proof structures
- `/SPECIFICATION/` - Normative PB2S specifications and requirements
- `/examples/` - Sample proofs and usage examples
- `/.github/workflows/` - CI/CD pipeline definitions

### Configuration Files
- `.env.example` - Provider and model configuration template (copy to `.env`)
- `requirements.txt` - Basic Python dependencies  
- `requirements_autonomous_brain.txt` - Extended ML dependencies (may have install issues)
- `brain_llm_config.json` - LLM connection configuration

## Development Workflow

### Before Making Changes
1. **Test current state**: Verify server and dashboard start successfully
2. **Run conformance**: `python scripts/conformance.py --endpoint http://127.0.0.1:8000/chat`
3. **Check system status**: `python LAUNCH_BRAIN_NETWORK.py` (option 1 for system test)

### After Making Changes  
1. **Test affected components**: Re-run startup tests for modified systems
2. **Run conformance tests**: Ensure PB2S structure compliance maintained
3. **Validate user scenarios**: Test complete workflows from user perspective
4. **Check for lint issues**: No formal linting setup but code suggests black/flake8 usage

### Validation Requirements
- **Manual testing required**: Simply starting/stopping is insufficient - exercise actual functionality
- **Complete workflows**: Test real user scenarios like API calls, dashboard interaction, brain network coordination
- **Error handling**: Verify graceful degradation when optional components fail

## Troubleshooting

### Common Command Failures
- **`python launch_brain_fixed.py --test`**: Expects Windows virtual environment paths - use `python launch_autonomous_brain.py` directly
- **Conformance test failures**: Check if REFLECT sections flag contradictions/assumptions (common failure mode)
- **Long-running pip installs**: Normal for ML packages - wait 30+ minutes before canceling

### Network and Connectivity
- **PyPI timeouts**: Retry with individual package installs
- **MQTT connection refused**: Normal if broker not running (non-fatal for most operations)
- **API not responding**: Check if port 8000 is available, allow 15+ seconds for startup

### System Requirements
- **Minimum**: Python 3.12+, 8GB RAM for basic operations
- **Recommended**: 16GB+ RAM for full autonomous brain features
- **Audio features**: Require system audio libraries (often problematic in containers/CI)

## Quick Reference Commands

```bash
# Complete setup from fresh clone
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install --upgrade pip
pip install -r requirements.txt  # 5-30 minutes, NEVER CANCEL

# Test core functionality  
python LAUNCH_BRAIN_NETWORK.py  # Interactive launcher
streamlit run enhanced_dashboard.py  # Web interface
python -c "import uvicorn; uvicorn.run('server.main:app')"  # API server

# Run tests and validation
python scripts/conformance.py --endpoint http://127.0.0.1:8000/chat
curl -X POST http://127.0.0.1:8000/chat -H 'Content-Type: application/json' -d '{"message": "test"}'
```

## Key Files and Their Purpose

### Configuration
- `.env` - Provider endpoints, API keys, model settings
- `brain_llm_config.json` - LLM service configuration  
- `requirements.txt` - Core dependencies (always install first)

### Documentation  
- `README.md` - Project overview and quickstart guide
- `ULTIMATE_SUCCESS.md` - Success stories and working commands
- `HOME_AI_BRAIN_NETWORK_GUIDE.md` - Distributed system setup guide

### Core Implementation
- `newborn_brain_core.py` - Brain capabilities and reasoning engine
- `pb2s_orchestrator.py` - PB2S loop implementation (DRAFT→REFLECT→REVISE→LEARNED)
- `brain_llm_connection.py` - LLM integration service

**Remember**: Always validate that every command works before documenting it. This codebase has network dependencies and ML components that can have extended installation times and intermittent failures.
