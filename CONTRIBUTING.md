Contributing to misfans

Thanks for your interest. Quick guide:

- Fork the repo, make a topic branch, and open a PR to main.
- Run tests: python3 -m venv .venv && . .venv/bin/activate && pip install -e . && pip install -r requirements.txt && pytest
- Follow PEP8/ruff rules (CI runs ruff).
- For changes that touch installer or systemd, test on a Pi or in a VM first.
