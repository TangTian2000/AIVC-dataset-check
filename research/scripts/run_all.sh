#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
# Cached frozen sources are required. Optional refresh: python research/scripts/fetch_resources.py
python research/scripts/index_sources.py
python research/scripts/analyze_metadata.py
python research/scripts/build_inventory.py
python research/scripts/build_reports.py
python research/scripts/plot_design.py
python -m unittest discover -s research/tests -v
