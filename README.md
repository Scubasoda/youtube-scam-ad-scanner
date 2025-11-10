# YouTube Scam Ad Scanner (prototype)

A private Python prototype to scan YouTube ads (landing pages and ad text) for common scam indicators.

Goals
- Provide a lightweight, extensible scanner for detecting likely scam ads.
- Focus on analyzing ad landing pages and ad copy using heuristics and simple ML-ready features.

Quick start
1. Create a virtualenv and install dependencies:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

2. Run basic checks on a URL:

    python -m src.scanner --url "https://example.com/suspicious-offer"

Project structure
- README.md - this file
- LICENSE - MIT license
- requirements.txt - Python dependencies
- src/scanner.py - main scanner implementation and CLI
- tests/ - unit tests

Design notes
- The scanner is intentionally small and heuristic-first: keyword checks, domain heuristics, landing-page characteristics, and link analysis.
- Future work: browser extension to capture ads, Selenium-based ad capture, machine learning models trained on labeled ads, report submission to platforms.