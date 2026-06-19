#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
import time
from datetime import datetime, timedelta

TIME_FORMATS = ["%H:%M", "%H:%M:%S"]


def parse_relative_delta(token: str) -> timedelta:
    token = token.strip().lower()
    if token.isdigit():
        return timedelta(minutes=int(token))

    match = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?", token)
    if not match:
        raise ValueError(
            "Relative alarm must be a positive number like '+10', '+5m', or '+1h30m'."
        )

    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    total = timedelta(hours=hours, minutes=minutes)
    if total <= timedelta(0):
        raise ValueError("Relative alarm must be greater than zero.")
    return total


def parse_alarm_time(value: str, now: datetime | None = None) -> datetime:
    if now is None:
        now = datetime.now().astimezone().replace(tzinfo=None)

    raw = value.strip()
    if not raw:
        raise ValueError("Alarm time cannot be empty.")

    if raw.lower() == "now":
        return now.replace(microsecond=0)

    if raw.startswith("+"):
        delta = parse_relative_delta(raw[1:])
        return (now + delta).replace(microsecond=0)

    for fmt in TIME_FORMATS:
        try:
            parsed = datetime.strptime(raw, fmt)
            target = now.replace(
                hour=parsed.hour,
                minute=parsed.minute,
                second=parsed.second if fmt == "%H:%M:%S" else 0,
                microsecond=0,
            )
            if target <= now:
                target += timedelta(days=1)
            return target
        except ValueError:
            continue

    raise ValueError(
        "Invalid alarm format. Use 'HH:MM', 'HH:MM:SS', '+M', '+5m', '+1h30m', or 'now'."
    )


def seconds_until(target: datetime, now: datetime | None = None) -> int:
    if now is None:
        now = datetime.now().astimezone().replace(tzinfo=None)
    delta = target - now
    return max(0, int(delta.total_seconds()))


def format_target(target: datetime) -> str:
    return target.strftime("%Y-%m-%d %H:%M:%S")


def run_alarm(target: datetime, message: str) -> int:
    seconds = seconds_until(target)
    print(f"Alarm set for {format_target(target)}. Waiting {seconds} second(s)...")
    try:
        while seconds > 0:
            time.sleep(min(seconds, 60))
            seconds = seconds_until(target)
    except KeyboardInterrupt:
        print("\nAlarm cancelled.")
        return 1

    print("\n\aALARM: " + message)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Minimal CLI alarm clock. Set a one-time alarm by absolute time or relative delay."
    )
    parser.add_argument(
        "alarm",
        help="Alarm time: 'HH:MM', 'HH:MM:SS', '+M', '+5m', '+1h30m', or 'now'.",
    )
    parser.add_argument(
        "-m",
        "--message",
        default="Wake up!",
        help="Text to print when the alarm fires.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        target = parse_alarm_time(args.alarm)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    return run_alarm(target, args.message)


if __name__ == "__main__":
    raise SystemExit(main())
