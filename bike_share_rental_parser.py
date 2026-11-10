def parse_ride_duration(text):
    """
    Converts a ride duration written as HH:MM into minutes.
    Hardened against unexpected/invalid inputs: handles None, empty strings,
    type errors, missing colons, non-numeric values, negative numbers, etc.
    Returns the duration in minutes, or None if the input is invalid.
    """
    if not isinstance(text, str):
        return None

    cleaned = text.strip()
    if not cleaned or ':' not in cleaned:
        return None

    parts = cleaned.split(':')
    if len(parts) != 2:
        return None

    try:
        hours = int(parts[0].strip())
        minutes = int(parts[1].strip())
        if hours < 0 or minutes < 0:
            return None
        return hours * 60 + minutes
    except (ValueError, TypeError):
        return None


def format_station_code(code):
    """
    Formats a station code as ZONE-NUMBER, e.g. 'a12' -> 'A-12'.
    Hardened against unexpected/invalid inputs: handles None, empty strings,
    type errors, whitespace, etc.
    Returns the formatted station code, or None if the input is invalid.
    """
    if not isinstance(code, str):
        return None

    cleaned = code.strip().upper()
    if not cleaned:
        return None

    if len(cleaned) == 1:
        return cleaned

    return cleaned[0] + '-' + cleaned[1:]


def parse_ride_log(line):
    """
    Parses 'bike_type,minutes,subscriber' into a tuple.
    Hardened against unexpected/invalid inputs: handles None, empty strings,
    type errors, malformed rows, non-integer minutes, etc.
    Returns (bike_type, minutes, is_subscriber), or None if the input is invalid.
    """
    if not isinstance(line, str):
        return None

    cleaned = line.strip()
    if not cleaned:
        return None

    parts = cleaned.split(',')
    if len(parts) != 3:
        return None

    bike_type = parts[0].strip()
    minutes_raw = parts[1].strip()
    sub_raw = parts[2].strip().lower()

    if not bike_type:
        return None

    try:
        minutes = int(minutes_raw)
        if minutes < 0:
            return None
    except (ValueError, TypeError):
        return None

    is_subscriber = sub_raw in ('yes', 'true', '1')
    return bike_type, minutes, is_subscriber


def main():
    print("==== Running parse_ride_duration ====")
    value = input("Enter a ride duration as HH:MM (e.g. 01:15): ")
    print("Duration in minutes:", parse_ride_duration(value))

    print("\n==== Running format_station_code ====")
    value = input("Enter a station code (e.g. a12): ")
    print("Formatted station code:", format_station_code(value))

    print("\n==== Running parse_ride_log ====")
    value = input("Enter a ride log line as type,minutes,subscriber (e.g. electric,45,yes): ")
    print("Parsed ride log:", parse_ride_log(value))


if __name__ == "__main__":
    main()
