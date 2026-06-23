# Google Business Profile (GBP) Review Triage Agent

This is a local prototype of an ambient GBP review triage agent. The agent uses the **Agent Development Kit (ADK) 2.0** graph-based `Workflow` API to automatically reply to positive reviews or flag problematic reviews for human intervention.

## 📂 Project Structure

```
gbp-review-triage/
├── app/                      # Core agent code
│   ├── agent.py              # Main graph Workflow logic (nodes, edges, HITL)
│   ├── fast_api_app.py       # FastAPI application wrapper with local SQLite sessions
│   ├── models.py             # Pydantic schemas (ReviewInput, LocationProfile, TriageResult)
│   └── app_utils/            # App telemetry and utilities
├── tests/                    # Evaluation configurations and test datasets
│   └── eval/
│       ├── eval_config.yaml  # Metric definitions (response quality, turn count)
│       └── datasets/
│           └── triage-dataset.json  # Mock review test cases
├── reviews.json              # Sample GBP review mock dataset
├── .env                      # Local authentication configurations (GCP vs AI Studio)
├── pyproject.toml            # Project dependencies and linting tool configuration
└── README.md                 # This file
```

---

## ⚙️ Prerequisites & Installation

1. **Python & uv**: Ensure you have Python >= 3.11 and the `uv` package manager installed.
2. **Install agents-cli**:
   ```bash
   uv tool install google-agents-cli
   ```
3. **Install Dependencies**:
   Run from the project root directory:
   ```bash
   agents-cli install
   ```

---

## 🔑 Authentication Setup

Before running the agent, set up authentication in the `.env` file at the root of the project:

### Option 1: Google Cloud (Vertex AI) - *Recommended*
1. Authenticate your local shell using Google Cloud SDK:
   ```bash
   gcloud auth application-default login
   ```
2. Configure `.env` with your project ID:
   ```env
   GOOGLE_CLOUD_PROJECT="your-google-cloud-project-id"
   GOOGLE_CLOUD_LOCATION="us-east1"
   GOOGLE_GENAI_USE_VERTEXAI="True"
   ```

### Option 2: Google AI Studio (Gemini Developer API)
1. Generate an API key in [Google AI Studio](https://aistudio.google.com/).
2. Edit your `.env` file to supply the key and disable Vertex AI mode:
   ```env
   GEMINI_API_KEY="your-ai-studio-api-key"
   GOOGLE_GENAI_USE_VERTEXAI="False"
   ```

---

## 🔄 Running and Resuming Sessions (Standalone Mode)

Local session state is persisted on disk inside a local SQLite database file (`sessions.db`). This allows local sessions to survive server restarts, idle timeouts, and separate execution commands.

### Running with a One-Off Prompt
Execute a quick query via the CLI:
```bash
agents-cli run "Test prompt"
```

### Starting and Persisting Conversations
Use `--session-id` to resume and maintain conversational context.

1. **Start a new session**:
   ```bash
   uv run agents-cli run --session-id "session_123" "{\"review_id\": \"r001\", \"location_id\": \"loc_bangkok_01\", \"rating\": 5, \"author_name\": \"Sarah T.\", \"comment\": \"Great meal!\"}"
   ```
2. **Resume/Query the same session**:
   ```bash
   uv run agents-cli run --session-id "session_123" "Do you remember my rating?"
   ```

### Web-Based Interactive Playground
Launch a local development playground to test the agent visually via a web browser:
```bash
agents-cli playground
```
This starts the local FastAPI server and launches the interactive web interface. Any conversations started here will persist inside `sessions.db`.

---

## 📊 Evaluation & Testing

Systematic validation is performed using evaluation datasets and metrics (LLM-as-a-judge) rather than static pytest assertions.

### How Offline HITL Evaluation Works
The evaluation runner executes tests in a non-interactive, single-turn mode. If a review is flagged, the agent would normally pause and yield a `RequestInput` to wait for a human. To prevent the evaluation runner from crashing/hanging during this offline phase, the agent automatically detects the evaluation run environment and auto-approves (`human_response = "APPROVE"`) the flagged review.

### Running the Evaluation Suite
1. **Generate traces**:
   ```bash
   uv run agents-cli eval generate --dataset tests/eval/datasets/triage-dataset.json --output triage_traces/
   ```
2. **Grade the generated traces**:
   ```bash
   uv run agents-cli eval grade --traces triage_traces/
   ```


---

## 🔒 Security Validation: PII Redaction & Prompt-Injection Defense

To protect sensitive data and prevent unauthorized instruction overrides, we have integrated a local security validation layer at the entrance of the agent workflow.

For detailed design, implementation, and test execution details, see the [Security Checkpoint Walkthrough](../docs/superpowers/walkthroughs/2026-06-23-gbp-security-checkpoint.md).

### Key Protections
1. **PII Redaction**: US Social Security Numbers (`[REDACTED_SSN]`) and Credit Card numbers (`[REDACTED_CC]`) are scrubbed using regular expressions and Luhn algorithm validation.
2. **Prompt-Injection Defense**: Scans input comments for command-override patterns and routes them directly to the human flag queue (`flag_for_human`), bypassing all LLM API generations.

### Running Security Validation Tests
Execute the unit tests verifying safety heuristics and security checkpoint routing:
```bash
uv run pytest tests/unit/test_security.py
```

---

## 🛠️ Code Quality
To check code format, types, and styles, run:
```bash
agents-cli lint
```
To auto-fix style and import formatting:
```bash
agents-cli lint --fix
```
