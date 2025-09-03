#!/usr/bin/env bash
set -e

POSTGRES_CMD="docker compose up -d postgres"
BACKEND_CMD="uvicorn backend.interface.api.main:app --host 0.0.0.0 --port 8000 --reload"
FRONTEND_CMD="npx --prefix frontend ng serve --proxy-config proxy.conf.json --project cicero_client --configuration=development"
VENV_ACTIVATE="source .venv/bin/activate"
SESSION="cicero_dev"

# start postgres
$POSTGRES_CMD

# if tmux available -> create/attach session (quiet)
if command -v tmux >/dev/null 2>&1; then
  if ! tmux has-session -t "$SESSION" 2>/dev/null; then
    tmux new-session -d -s "$SESSION" -n backend "bash -lc '$VENV_ACTIVATE && exec $BACKEND_CMD'"
    tmux new-window -t "$SESSION" -n frontend "$FRONTEND_CMD"
    tmux new-window -t "$SESSION" -n postgres "docker compose logs -f postgres"
  fi
  tmux attach -t "$SESSION"
  exit 0
fi

# fallback: run backend (blocks)
$BACKEND_CMD

# run frontend (only if backend exits)
$FRONTEND_CMD