#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple


def _is_missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        v = value.strip()
        return v == "" or v.lower() in {"null", "none", "na", "n/a"}
    return False


def _try_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if not isinstance(value, str):
        return None
    raw = value.strip()
    if raw == "":
        return None
    normalized = raw.replace(",", "")
    try:
        x = float(normalized)
    except ValueError:
        return None
    if math.isnan(x) or math.isinf(x):
        return None
    return x


@dataclass
class RunningStats:
    count: int = 0
    mean: float = 0.0
    m2: float = 0.0
    min: Optional[float] = None
    max: Optional[float] = None

    def add(self, x: float) -> None:
        self.count += 1
        self.min = x if self.min is None else min(self.min, x)
        self.max = x if self.max is None else max(self.max, x)

        delta = x - self.mean
        self.mean += delta / self.count
        delta2 = x - self.mean
        self.m2 += delta * delta2

    def to_dict(self) -> Dict[str, Any]:
        if self.count == 0:
            return {"count": 0}
        variance = self.m2 / (self.count - 1) if self.count > 1 else 0.0
        stddev = math.sqrt(variance)
        return {
            "count": self.count,
            "min": self.min,
            "max": self.max,
            "mean": self.mean,
            "stddev": stddev,
        }


def _summarize_records(
    records: Iterable[Dict[str, Any]],
    *,
    max_rows: int,
    sample_size: int,
) -> Dict[str, Any]:
    row_count = 0
    columns: List[str] = []
    missing_counts: Dict[str, int] = {}
    stats: Dict[str, RunningStats] = {}
    sample: List[Dict[str, Any]] = []

    def ensure_columns(row: Dict[str, Any]) -> None:
        nonlocal columns
        if columns:
            return
        columns = list(row.keys())
        for col in columns:
            missing_counts[col] = 0
            stats[col] = RunningStats()

    for row in records:
        if row_count >= max_rows:
            break
        ensure_columns(row)
        row_count += 1

        if len(sample) < sample_size:
            sample.append(row)

        for col in columns:
            val = row.get(col)
            if _is_missing(val):
                missing_counts[col] = missing_counts.get(col, 0) + 1
                continue
            x = _try_float(val)
            if x is None:
                continue
            stats.setdefault(col, RunningStats()).add(x)

    numeric_stats = {col: st.to_dict() for col, st in stats.items() if st.count > 0}

    return {
        "rows": row_count,
        "columns": columns,
        "missing": missing_counts,
        "numeric": numeric_stats,
        "sample": sample,
        "truncated": row_count >= max_rows,
    }


def _load_json_records(path: str) -> Tuple[str, Iterable[Dict[str, Any]]]:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read().strip()
        if text == "":
            return ("json", iter(()))
        if text[0] == "[":
            data = json.loads(text)
            if isinstance(data, list):
                return ("json", (row for row in data if isinstance(row, dict)))
            return ("json", iter(()))
        if text[0] == "{":
            data = json.loads(text)
            if isinstance(data, dict):
                return ("json", iter((data,)))
            return ("json", iter(()))

    return ("json", iter(()))


def _load_jsonl_records(path: str) -> Tuple[str, Iterable[Dict[str, Any]]]:
    def gen() -> Iterable[Dict[str, Any]]:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(obj, dict):
                    yield obj

    return ("jsonl", gen())


def _load_csv_records(path: str, delimiter: str) -> Tuple[str, Iterable[Dict[str, Any]]]:
    def gen() -> Iterable[Dict[str, Any]]:
        with open(path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                yield row

    return ("csv", gen())


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize a CSV/TSV/JSON file for quick analysis.")
    parser.add_argument("path", help="Path to the input file (csv/tsv/json/jsonl).")
    parser.add_argument("--max-rows", type=int, default=10000, help="Maximum number of rows to scan.")
    parser.add_argument("--sample-size", type=int, default=5, help="Number of sample rows to include.")
    args = parser.parse_args()

    path = os.path.expanduser(args.path)
    if not os.path.exists(path):
        print(json.dumps({"error": "file_not_found", "path": path}, ensure_ascii=False))
        return 2

    ext = os.path.splitext(path)[1].lower()
    try:
        if ext == ".tsv":
            fmt, records = _load_csv_records(path, "\t")
        elif ext == ".csv":
            fmt, records = _load_csv_records(path, ",")
        elif ext == ".jsonl":
            fmt, records = _load_jsonl_records(path)
        elif ext == ".json":
            fmt, records = _load_json_records(path)
        else:
            print(json.dumps({"error": "unsupported_extension", "path": path, "ext": ext}, ensure_ascii=False))
            return 2

        summary = _summarize_records(records, max_rows=args.max_rows, sample_size=args.sample_size)
        out = {
            "file": os.path.abspath(path),
            "format": fmt,
            **summary,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    except Exception as e:
        print(json.dumps({"error": "exception", "message": str(e)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

