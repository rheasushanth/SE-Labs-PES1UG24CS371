"""Campus Shuttle Timetable & Fleet Tracker.

Logs passenger counts per trip, works out average loads, flags
under-used routes and syncs the fleet data to a JSON file.
"""

import json
import secrets
from datetime import datetime

# Global state
routes = {"R1": {"name": "Main Gate - Library", "trips": []},
          "R2": {"name": "Hostel - Sports Complex", "trips": []},
          "R3": {"name": "Admin Block - Metro", "trips": []}}
MIN_CAPACITY = 10
DRIVERS = ["Prakash", "Leela", "Imran", "Tom"]


def add_trip_log(route_id, passenger_count, logs=None):
    """Record a trip's passenger count and return the updated log list."""
    if logs is None:
        logs = []
    if route_id not in routes:
        raise KeyError(f"Unknown route: {route_id}")
    if not isinstance(passenger_count, int) or isinstance(passenger_count,
                                                          bool):
        raise TypeError("Passenger count must be a whole number")
    if passenger_count < 0:
        raise ValueError("Passenger count cannot be negative")
    routes[route_id]["trips"].append(passenger_count)
    logs.append(f"{datetime.now()}: {route_id} carried {passenger_count}")
    return logs


def remove_route(route_id):
    """Delete a route if it exists. Returns True if it was removed."""
    return routes.pop(route_id, None) is not None


def average_load(route_id):
    """Return the average passengers per trip, or None if unavailable."""
    route = routes.get(route_id)
    if route is None or not route["trips"]:
        return None
    trips = route["trips"]
    return sum(trips) / len(trips)


def underused_routes():
    """Return the IDs of routes whose average load is below MIN_CAPACITY."""
    flagged = []
    for route_id in routes:
        avg = average_load(route_id)
        if avg is not None and avg < MIN_CAPACITY:
            flagged.append(route_id)
    return flagged


def assign_driver():
    """Pick a driver at random."""
    return secrets.choice(DRIVERS)


def sync_fleet_data(file="fleet.json"):
    """Write the route data to a JSON file and load it back."""
    with open(file, "w", encoding="utf-8") as out:
        json.dump(routes, out)
    with open(file, encoding="utf-8") as src:
        loaded = json.load(src)
    routes.clear()
    routes.update(loaded)


def safe_log(route_id, passenger_count):
    """Log a trip, printing a message instead of crashing on bad data."""
    try:
        add_trip_log(route_id, passenger_count)
    except (KeyError, TypeError, ValueError) as err:
        print(f"Rejected trip for {route_id} ({passenger_count!r}): {err}")


def main():
    """Run a short demo of the shuttle tracker."""
    safe_log("R1", 32)
    safe_log("R1", 28)
    safe_log("R2", 4)
    safe_log("R2", -6)
    safe_log("R3", "full")
    print("Driver for R1:", assign_driver())
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))
    sync_fleet_data()
    remove_route("R3")
    choice = input("Route to look up (Enter for R2): ").strip() or "R2"
    if choice in routes:
        print("Trips on", choice, ":", routes[choice]["trips"])
    else:
        print("No such route:", choice)
    r3_avg = average_load("R3")
    print("R3 average:", r3_avg if r3_avg is not None else "no data")


if __name__ == "__main__":
    main()
