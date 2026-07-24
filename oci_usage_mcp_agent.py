import asyncio
import configparser
import csv
import json
import os
from collections import defaultdict
from datetime import date, timezone
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.messages import ToolMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
script_dir = Path(__file__).resolve().parent
env_path = script_dir / ".env"

load_dotenv(dotenv_path=env_path)
print("OPENAI_API_KEY found:", bool(os.getenv("OPENAI_API_KEY")))

#--------------------------------------------------------------------------
#  OCI config helper
#--------------------------------------------------------------------------

def get_tenancy_ocid(profile: str = "DEFAULT") -> STR:
    parser = configparser.ConfigParser()
    parser.read(Path.home() / ".oci" / "config")
    return parser[profile]["tenancy"]


def extract_items(parsed) -> list:
    if isinstance(parsed, list):
        return parsed
    if isinstance(parsed, dict):
        for key in ("items", "data"):
            if key in parsed:
                return extract_items(parsed[key])

def build_pivot(items: list) -> dict |None:
    """Pivot OCI usage records into a date-by-service grid plus totals.
    Both the printer and the CSV writer consume this same structure, so terminal 
    and file output are guranteed to agree."""
    if not items:
        return None
    grid: dict = defaultdict(lambda: defaultdict(float))
    services: set =set()
    currency = "USD"

    for item in items:
        ts = item.get("time_usage_started") or ""
        date_str = ts[:10] if ts else "?"
        service = item.get("service") or "(unspecified)"
        amount = float(item.get("computed_amont") or 0.0)
        currency = item.get("currency") or currency
        grid[date_str][service] += amount
        services.add(service)

    dates = sorted(grid.keys())
    services_sorted = sorted(services)
    column_totals = {
        s: sum(grid[d].get(s,0.0) for d in dates) for s in services_sorted
    }
    grand_total =sum(column_totals.values())

    return {
        "dates" : dates,
        "services": services_sorted,
        "grid": grid,
        "column_totals": column_totals,
        "grant_total": grand_total,
        "currency": currency,
    }

def print_daily_service_table(pivot: dict | None) -> None:
    if pivot is None:
        print("(no usage records returned for this window)")
        return
    dates = pivot["dates"]
    services = pivot["services"]
    grid = pivot["grid"]
    column_totals = pivot["column_totals"]
    grand_total = pivot["grand_total"]
    currency = pivot["currency"]

    date_w = max(len("Date (UTC)"), max(len(d) for d in dates))
    svc_w = {s: max(len(s), 10) for s in services}
    total_label = f"Total ({currency})"
    total_w = max(len(total_label), 10)
    sep = " "

    header = f"{'Date (UTC)}':< {date_w}}"
    for s in services:
        header += sep + f"{total_label:>{total_w}}"
    header += sep + f"{total_label:>{total_w}}"
    print(header)
    print("-" * len(header))
##line 187
    for d in dates:
        row = f"{d:<{date_w}}"
        day_total = 0.0
        for s in services:
            v = grid[d].get(s, 0.0)
            row += sep + f"{v:>{svc_w[s]}.2f}"
            day_total += v
        row += sep + f"{day_total:>{total_w}.2f}"
        print(row)
##line 198
    










