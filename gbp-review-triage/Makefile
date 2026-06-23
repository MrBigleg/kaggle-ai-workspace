# ──────────────────────────────────────────────────────────────────────────────
# GBP Review Triage Agent – Developer Makefile
# ──────────────────────────────────────────────────────────────────────────────
# Prerequisites: Python >=3.11, uv, google-agents-cli
#
# NOTE  : On Windows without GNU Make, run the commands directly in PowerShell.
#         Each target's recipe is a single-line command you can copy-paste.
# ──────────────────────────────────────────────────────────────────────────────

.DEFAULT_GOAL := help

# ── Install ──────────────────────────────────────────────────────────────────
.PHONY: install
install: ## Install all project dependencies via agents-cli
	uv tool install google-agents-cli
	agents-cli install

# ── Lint / Format ────────────────────────────────────────────────────────────
.PHONY: lint
lint: ## Run ruff linter + type checker
	agents-cli lint

.PHONY: lint-fix
lint-fix: ## Auto-fix lint issues
	agents-cli lint --fix

# ── Unit Tests ───────────────────────────────────────────────────────────────
.PHONY: test
test: ## Run security unit tests
	uv run pytest tests/unit/test_security.py -v

# ── Playground ───────────────────────────────────────────────────────────────
.PHONY: playground
playground: ## Launch the ADK dev playground UI (http://localhost:8000)
	agents-cli playground --port 8000

# ── Evaluation ───────────────────────────────────────────────────────────────
.PHONY: eval-generate
eval-generate: ## Generate evaluation traces from the test dataset
	uv run agents-cli eval generate --dataset tests/eval/datasets/triage-dataset.json --output triage_traces/

.PHONY: eval-grade
eval-grade: ## Grade previously generated evaluation traces
	uv run agents-cli eval grade --traces triage_traces/

# ── Test Reviews (CLI one-shots) ─────────────────────────────────────────────
# These send sample review payloads to the agent via the CLI.
# The 5-star review takes the auto-reply path; the 3-star review triggers HITL.

.PHONY: test-5star
test-5star: ## Send a 5-star review (auto-reply path)
	uv run agents-cli run '{"review_id": "r_test_5", "location_id": "loc_bangkok_01", "rating": 5, "author_name": "Sarah T.", "comment": "Absolutely loved the fusion dishes! Best meal in Bangkok."}'

.PHONY: test-3star
test-3star: ## Send a 3-star review (flagged → HITL path)
	uv run agents-cli run '{"review_id": "r_test_3", "location_id": "loc_bangkok_02", "rating": 3, "author_name": "Tom R.", "comment": "Food was okay but the service was extremely slow and the oysters tasted off."}'

# ── Help ─────────────────────────────────────────────────────────────────────
.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
