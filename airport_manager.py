"""
Airport Manager Module

Manages airport flight data including passengers, gates, and flight status.
Uses list, tuple, dictionary, and set data structures meaningfully.
"""

# =============================================================================
# DATA STRUCTURES
# =============================================================================

# Tuple: Immutable airport information (code, terminal, date)
AIRPORT_INFO = ("OUL", "1", "14-09-2026")

# Set: Allowed gates (unordered, unique, fast membership testing)
ALLOWED_GATES = {"A1", "A2", "A3", "A4", "B1", "B2"}

# Set: Restricted destinations (case-insensitive handling in functions)
RESTRICTED_DESTINATIONS = {"moscow", "pyongyang"}

# Dictionary: Flight data keyed by normalized flight number
# Each flight is a dictionary with destination, departure, gate, capacity, passengers (list)
FLIGHTS = {
    "AY450": {
        "destination": "Helsinki",
        "departure": "08:30",
        "gate": "A2",
        "capacity": 5,
        "passengers": ["Alice Wong", "David Kim", "Fatima Ali"],
    },
    "SK271": {
        "destination": "Stockholm",
        "departure": "10:15",
        "gate": "B1",
        "capacity": 4,
        "passengers": ["Chen Wei", "George Smith"],
    },
    "LH2491": {
        "destination": "Munich",
        "departure": "12:40",
        "gate": "A4",
        "capacity": 5,
        "passengers": ["Hana Lee", "Maria Garcia", "Noah Wilson"],
    },
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _normalize_flight_key(flight_number):
    """Normalize a flight number by stripping and converting to uppercase."""
    if flight_number is None:
        return None
    return flight_number.strip().upper()


def _normalize_name(name):
    """Normalize a passenger name by stripping and converting to lowercase."""
    if name is None:
        return None
    return name.strip().lower()


# =============================================================================
# REQUIRED FUNCTIONS
# =============================================================================

def find_flight(flight_number):
    """
    Find a flight by its number (case-insensitive).

    Args:
        flight_number: The flight number to look up.

    Returns:
        The normalized flight key (str) if found, otherwise None.
    """
    key = _normalize_flight_key(flight_number)
    if key is None:
        return None
    if key in FLIGHTS:
        return key
    return None


def passenger_exists(flight_number, passenger_name):
    """
    Check if a passenger exists on a given flight (case-insensitive).

    Args:
        flight_number: The flight number to check.
        passenger_name: The passenger name to search for.

    Returns:
        True if the passenger is on the flight, False otherwise.
    """
    key = find_flight(flight_number)
    if key is None:
        return False
    normalized = _normalize_name(passenger_name)
    if normalized is None:
        return False
    return any(_normalize_name(p) == normalized for p in FLIGHTS[key]["passengers"])


def check_in_passenger(flight_number, passenger_name):
    """
    Check in a passenger to a flight.

    Args:
        flight_number: The flight number.
        passenger_name: The passenger name to check in.

    Returns:
        One of: OK, FLIGHT_NOT_FOUND, EMPTY_NAME, DUPLICATE, FULL, RESTRICTED
    """
    key = find_flight(flight_number)
    if key is None:
        return "FLIGHT_NOT_FOUND"

    # Check for empty or whitespace-only name
    if passenger_name is None or _normalize_name(passenger_name) == "":
        return "EMPTY_NAME"

    flight = FLIGHTS[key]

    # Check restricted destination
    if flight["destination"].strip().lower() in RESTRICTED_DESTINATIONS:
        return "RESTRICTED"

    # Check for duplicate passenger
    if passenger_exists(key, passenger_name):
        return "DUPLICATE"

    # Check capacity
    if len(flight["passengers"]) >= flight["capacity"]:
        return "FULL"

    # All checks passed — add passenger (preserve original formatting, stripped)
    flight["passengers"].append(passenger_name.strip())
    return "OK"


def remove_passenger(flight_number, passenger_name):
    """
    Remove a passenger from a flight.

    Args:
        flight_number: The flight number.
        passenger_name: The passenger name to remove.

    Returns:
        One of: OK, FLIGHT_NOT_FOUND, PASSENGER_NOT_FOUND
    """
    key = find_flight(flight_number)
    if key is None:
        return "FLIGHT_NOT_FOUND"

    normalized = _normalize_name(passenger_name)
    if normalized is None:
        return "PASSENGER_NOT_FOUND"

    passengers = FLIGHTS[key]["passengers"]
    for i, p in enumerate(passengers):
        if _normalize_name(p) == normalized:
            del passengers[i]
            return "OK"

    return "PASSENGER_NOT_FOUND"


def change_gate(flight_number, new_gate):
    """
    Change the gate for a flight.

    Args:
        flight_number: The flight number.
        new_gate: The new gate (must be in ALLOWED_GATES).

    Returns:
        One of: OK, FLIGHT_NOT_FOUND, INVALID_GATE
    """
    key = find_flight(flight_number)
    if key is None:
        return "FLIGHT_NOT_FOUND"

    if new_gate not in ALLOWED_GATES:
        return "INVALID_GATE"

    FLIGHTS[key]["gate"] = new_gate
    return "OK"


def flight_status(flight_number):
    """
    Get the status of a flight based on passenger count vs capacity.

    Args:
        flight_number: The flight number.

    Returns:
        One of: AVAILABLE, ALMOST FULL, FULL
    """
    key = find_flight(flight_number)
    if key is None:
        return None

    flight = FLIGHTS[key]
    count = len(flight["passengers"])
    capacity = flight["capacity"]

    if count >= capacity:
        return "FULL"
    if count >= capacity - 1:
        return "ALMOST FULL"
    return "AVAILABLE"


def sorted_manifest(flight_number):
    """
    Get a sorted copy of the passenger list for a flight.

    Args:
        flight_number: The flight number.

    Returns:
        A new sorted list of passenger names, or None if flight not found.
    """
    key = find_flight(flight_number)
    if key is None:
        return None
    return sorted(FLIGHTS[key]["passengers"])


def total_passengers():
    """
    Get the total number of passengers across all flights.

    Returns:
        Integer total passenger count.
    """
    return sum(len(flight["passengers"]) for flight in FLIGHTS.values())


def any_full_flight():
    """
    Check if any flight is at full capacity.

    Returns:
        True if at least one flight is full, False otherwise.
    """
    return any(
        len(flight["passengers"]) >= flight["capacity"]
        for flight in FLIGHTS.values()
    )


def all_flights_have_passengers():
    """
    Check if all flights have at least one passenger.

    Returns:
        True if every flight has at least one passenger, False otherwise.
    """
    return all(len(flight["passengers"]) > 0 for flight in FLIGHTS.values())