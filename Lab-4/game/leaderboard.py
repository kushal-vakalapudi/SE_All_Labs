import json
from pathlib import Path

LEADERBOARD_PATH = Path(__file__).resolve().parent.parent / "leaderboard.json"
MAX_ENTRIES = 5


def load_leaderboard(path=LEADERBOARD_PATH):
    path = Path(path)
    if not path.exists():
        return []

    with path.open(encoding="utf-8") as file:
        entries = json.load(file)

    if not isinstance(entries, list):
        raise ValueError("Leaderboard JSON must contain a list.")

    for entry in entries:
        if (
            not isinstance(entry, dict)
            or not isinstance(entry.get("time"), (int, float))
            or not isinstance(entry.get("difficulty"), str)
        ):
            raise ValueError("Leaderboard contains an invalid entry.")

    return sorted(entries, key=lambda entry: entry["time"])[:MAX_ENTRIES]


def record_time(elapsed, difficulty, path=LEADERBOARD_PATH):
    if elapsed < 0:
        raise ValueError("Completion time cannot be negative.")

    entries = load_leaderboard(path)
    entries.append({"time": round(elapsed, 2), "difficulty": difficulty})
    entries.sort(key=lambda entry: entry["time"])
    entries = entries[:MAX_ENTRIES]

    path = Path(path)
    with path.open("w", encoding="utf-8") as file:
        json.dump(entries, file, indent=2)
        file.write("\n")

    return entries
