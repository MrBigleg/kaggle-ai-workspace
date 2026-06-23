# Setup & Local Development

> **Source:** [Vibecode Ambient Expense Agent Codelab](https://codelabs.developers.google.com/vibecode-ambient-expense-agent)  
> These steps follow the canonical tutorial. Adapt agent names/folders for the GBP remixes in this repo.

---

## Prerequisites

1. **Python 3.11+** with `uv` package manager
2. **Antigravity IDE** — install from [antigravity.google/docs/home](https://antigravity.google/docs/home)
3. **Google AI Studio API key** (easier) OR a Google Cloud project (for Vertex AI)

---

## Step 1 — Install Google Agents CLI

```bash
uvx google-agents-cli setup
```

Verify installation:

```bash
agents-cli info
```

This activates skills including `adk-scaffold`, `google-agents-cli-workflow`, and `google-agents-cli-eval`.

---

## Step 2 — Create Project Folder

```bash
mkdir <agent-folder-name>
cd <agent-folder-name>
```

Open the folder in Antigravity IDE, then use the `adk-scaffold` skill to initialize the ADK starter template.

---

## Step 3 — Authentication

Create a `.env` file in the project root. Choose one option:

**Option A — Google AI Studio (recommended for local dev):**

```bash
GOOGLE_API_KEY=your_key_here
```

Get a key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).

**Option B — Google Cloud project (for Cloud Run / Agent Runtime):**

```bash
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

---

## Step 4 — Project Structure

Every agent in this repo follows this layout:

```
{agent-folder}/
├── expense_agent/          # rename to match your agent
│   ├── agent.py            # ADK 2.0 graph definition (nodes + edges)
│   ├── config.py           # thresholds, model name, business rules
│   └── fast_api_app.py     # FastAPI app — mounts ADK, exposes Pub/Sub endpoint
├── tests/
│   └── eval/
│       ├── datasets/
│       │   └── basic-dataset.json
│       ├── generate_traces.py
│       └── eval_config.yaml
├── pyproject.toml
├── Makefile
├── .env
└── README.md
```

---

## Step 5 — Install Dependencies

```bash
make install
# equivalent to: uv sync
```

---

## Step 6 — Run Locally

Two terminals are required:

**Terminal 1 — Interactive ADK Playground (port 8080):**

```bash
make playground
# equivalent to: uv run python -m adk.dev.server
```

Open: `http://localhost:8080/dev-ui/`

**Terminal 2 — Ambient event server:**

```bash
make run-server
# equivalent to: uv run python -m uvicorn expense_agent.fast_api_app:app --port 8080
```

---

## Step 7 — Test the Workflow

### Auto-approval test (trigger under threshold)

```bash
curl -s http://localhost:8080/apps/expense_agent/trigger/pubsub \
  -H "Content-Type: application/json" \
  -d '{"message":{"data":"<base64-encoded-json>"},"subscription":"test-sub"}'
```

Then inspect the session in the dev UI:  
`http://localhost:8080/dev-ui/?app=expense_agent&userId=test-sub`

---

## Step 8 — Evaluation

### Generate traces

```bash
make generate-traces
# equivalent to: uv run python tests/eval/generate_traces.py
```

### Grade with LLM-as-judge

```bash
make grade
# equivalent to: agents-cli grade --config tests/eval/eval_config.yaml
```

Results appear in `artifacts/grade_results/`.

---

## Makefile Reference

```makefile
install:
    uv sync

playground:
    uv run python -m adk.dev.server

run-server:
    uv run python -m uvicorn expense_agent.fast_api_app:app --port 8080

generate-traces:
    uv run python tests/eval/generate_traces.py

grade:
    agents-cli grade --config tests/eval/eval_config.yaml
```

---

## Key Technical Notes

- **ADK 2.0 Graph API** — uses function nodes, edges, and `RequestInput` (not 1.x `SequentialAgent`)
- **FastAPI mount** — automatically provides `/apps/<agent_name>/trigger/pubsub` endpoint
- **Pub/Sub handling** — auto base64-decodes messages, isolates sessions, assigns subscription name as `userId`
- **Telemetry** — set `otel_to_cloud=False` for local testing
- **Security nodes** — insert before any LLM call on high-value or untrusted input to redact PII and catch prompt injection

---

## Environment Variables (GBP Remix Additions)

These are specific to the GBP agent remixes and supplement the standard `.env` above:

```bash
GBP_API_KEY=your_key
GBP_CLIENT_ID=your_client_id
GBP_CLIENT_SECRET=your_secret
SLACK_BOT_TOKEN=xoxb-your-token
SLACK_CHANNEL_ID=C12345
FIRESTORE_PROJECT_ID=your_project
```

---

## Cleanup

```bash
# Stop servers
Ctrl+C

# Remove credentials
# Delete API keys at console.cloud.google.com/apis/credentials
rm .env

# Uninstall CLI
uv tool uninstall google-agents-cli
```
