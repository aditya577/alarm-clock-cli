# Python CLI Alarm Clock

A minimal CLI alarm clock written in Python. It supports one-time alarms using absolute or relative scheduling and prints a console alert when the alarm fires.

## MVP scope

- Set a single alarm from the command line
- Support absolute time formats: `HH:MM` and `HH:MM:SS`
- Support relative delays: `+M`, `+5m`, `+1h30m`
- Support immediate alarm: `now`
- Display a message and terminal bell when the alarm rings
- No persistence, no UI, no database

## Architecture

- `alarm_clock.py`: CLI entrypoint and scheduler
- `parse_alarm_time()`: converts user input into a target `datetime`
- `run_alarm()`: waits until the target time and prints the alert
- `tests/test_alarm_clock.py`: validation of input parsing and scheduling logic

## File structure

- `alarm_clock.py`
- `tests/test_alarm_clock.py`
- `README.md`

## Usage

Run an absolute alarm:

```bash
python alarm_clock.py 08:30
```

Run a relative alarm:

```bash
python alarm_clock.py +10
python alarm_clock.py +1h30m
```

Set a custom message:

```bash
python alarm_clock.py +5 -m "Meeting starts now"
```

Trigger immediately:

```bash
python alarm_clock.py now
```

## Timezone

The alarm clock uses **local system time** by default, which matches your system's timezone settings. This ensures alarms trigger at the time you expect on your local clock.

To test with a different timezone, use the `TZ` environment variable:

```bash
TZ=Asia/Kolkata python alarm_clock.py 15:30
TZ=America/New_York python alarm_clock.py 15:30
TZ=Europe/London python alarm_clock.py 15:30
TZ=Asia/Tokyo python alarm_clock.py 15:30
```

The alarm will respect your local timezone, including daylight saving time transitions.

## Edge cases

- Invalid time formats are rejected with a clear error
- Past absolute times roll over to the next day
- Relative delays must be positive
- Empty alarm input is rejected
- Keyboard interrupt cancels the waiting alarm cleanly

## Testing strategy

- Use unit tests for parsing and scheduling logic
- Keep scheduler side effects isolated by testing `parse_alarm_time()` and `seconds_until()`
- Validate absolute and relative input forms
- Confirm correct rollover for next-day absolute alarms
- Run tests with Python's built-in `unittest`

## Future scope

- Add multiple alarms in one session
- Add optional snooze support
- Add a `--quiet` mode or logging
- Add sound playback or desktop notification support (still CLI-only)
- Add a wrapper script or package entrypoint for easy installation
