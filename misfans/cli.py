"""Simple CLI for misfans: run in foreground, check status, stop service."""
import argparse
import subprocess
import sys
from pathlib import Path

from .daemon import main as run_foreground


def status():
    # If systemd is present, show systemd status; otherwise show process info
    try:
        subprocess.run(["systemctl", "status", "misfans.service"], check=False)
    except FileNotFoundError:
        print("systemctl not found; run the daemon in foreground with: misfans run")


def stop():
    try:
        subprocess.run(["systemctl", "stop", "misfans.service"], check=False)
    except FileNotFoundError:
        print("systemctl not found; stop the foreground process with Ctrl-C")


def run():
    # Run in foreground (blocking)
    run_foreground()


def main():
    parser = argparse.ArgumentParser(prog="misfans")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("run", help="Run daemon in foreground (for debugging)")
    sub.add_parser("status", help="Show systemd service status if available")
    sub.add_parser("stop", help="Stop systemd service if available")

    args = parser.parse_args()
    if args.cmd == "run":
        run()
    elif args.cmd == "status":
        status()
    elif args.cmd == "stop":
        stop()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
