from __future__ import annotations

from datetime import datetime


ZONES = {
    1: "Central",
    2: "Midtown",
    3: "Downtown",
}


STATIONS_BY_ZONE = {
    "Central": sorted(
        [
            "Bylyn",
            "Centrala",
            "Frestin",
            "Jaun d",
            "Lomil",
            "Ninia",
            "Rede",
            "Soth",
            "Tallan",
            "Yaen",
        ]
    ),
    "Midtown": sorted(
        [
            "Agralle",
            "Docia",
            "Garion",
            "Oloadus",
            "Obelyn",
            "Quthiel",
            "Ralith",
            "Riclya",
            "Riladia",
            "Stonyam",
            "Wicyt",
        ]
    ),
    "Downtown": sorted(
        [
            "Adohad",
            "Brunad",
            "Ederif",
            "Elyot",
            "Erean",
            "Holmer",
            "Keivia",
            "Marend",
            "Perinad",
            "Pryn",
            "Ruril",
            "Ryall",
            "Vertwall",
            "Zord",
        ]
    ),
}

FARES_PER_ZONE = {
    "Adult": 2105,
    "Child": 1410,
    "Senior": 1025,
    "Student": 1750,
}


def print_stations_board() -> None:
    """Print zones and stations as a simple table-like output."""
    print("\n" + "=" * 70)
    print("CTA STATIONS BOARD (by zone, alphabetical)")
    print("=" * 70)

    for zone_id, zone_name in ZONES.items():
        print(f"\nZone {zone_id}: {zone_name}")
        print("-" * 70)
        stations = STATIONS_BY_ZONE[zone_name]

        cols = 3
        for i in range(0, len(stations), cols):
            row = stations[i : i + cols]
            print("  ".join(name.ljust(18) for name in row))


def get_int_in_range(prompt: str, min_value: int, max_value: int) -> int:
    """Get an integer between min_value and max_value (inclusive)."""
    while True:
        raw = input(prompt).strip()
        if not raw.isdigit():
            print("❌ Please enter a whole number.")
            continue

        value = int(raw)
        if value < min_value or value > max_value:
            print(f"❌ Please enter a number from {min_value} to {max_value}.")
            continue

        return value


def get_non_negative_int(prompt: str) -> int:
    """Get a non-negative integer (0 or more)."""
    while True:
        raw = input(prompt).strip()
        if raw == "":
            print("❌ Please enter a number (0 or more).")
            continue
        if not raw.isdigit():
            print("❌ Please enter a whole number (0 or more).")
            continue
        return int(raw)


def calculate_zones_travelled(start_zone: int, dest_zone: int) -> int:
    """
    Calculate zones travelled (including start and destination zones).
    Example: Zone 1 -> Zone 3 => 3 zones (1,2,3)
    """
    return abs(dest_zone - start_zone) + 1


def format_cents(cents: int) -> str:
    """Format cents as currency-like text (still showing cents)."""
    return f"{cents} cents"


def issue_voucher(start_zone: int, dest_zone: int, travellers: dict[str, int]) -> None:
    """Print the travel voucher with all required details."""
    zones_travelled = calculate_zones_travelled(start_zone, dest_zone)
    dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("\n" + "=" * 70)
    print("CTA TRAVEL VOUCHER")
    print("=" * 70)
    print(f"Issued: {dt}")
    print(f"Boarding zone: {ZONES[start_zone]} (Zone {start_zone})")
    print(f"Destination zone: {ZONES[dest_zone]} (Zone {dest_zone})")
    print(f"Total zones travelled: {zones_travelled}")

    print("\nTraveller summary and fares:")
    print("-" * 70)
    print(f"{'Category':<10}{'Qty':>6}{'Fare/Zone':>14}{'Zones':>8}{'Total':>14}")

    grand_total = 0
    total_travellers = 0

    for category in ["Adult", "Child", "Senior", "Student"]:
        qty = travellers.get(category, 0)
        fare_per_zone = FARES_PER_ZONE[category]
        category_total = qty * fare_per_zone * zones_travelled

        total_travellers += qty
        grand_total += category_total

        print(
            f"{category:<10}{qty:>6}{format_cents(fare_per_zone):>14}"
            f"{zones_travelled:>8}{format_cents(category_total):>14}"
        )

    print("-" * 70)
    print(f"Total travellers: {total_travellers}")
    print(f"Total fares paid: {format_cents(grand_total)}")
    print("=" * 70)


def main() -> None:
    """Main menu loop."""
    print("Welcome to the CTA Automated Ticketing System")

    while True:
        print_stations_board()

        print("\n" + "-" * 70)
        print("ZONE SELECTION MENU")
        print("-" * 70)
        for zone_id, zone_name in ZONES.items():
            print(f"{zone_id}. {zone_name}")

        start_zone = get_int_in_range("Select START zone (1-3): ", 1, 3)
        dest_zone = get_int_in_range("Select DESTINATION zone (1-3): ", 1, 3)

        print("\nEnter number of travellers in each category:")
        travellers = {
            "Adult": get_non_negative_int("Adults: "),
            "Child": get_non_negative_int("Children: "),
            "Senior": get_non_negative_int("Seniors: "),
            "Student": get_non_negative_int("Students: "),
        }

        if sum(travellers.values()) == 0:
            print("❌ You must have at least 1 traveller. Please try again.")
            continue

        issue_voucher(start_zone, dest_zone, travellers)

        again = input("\nIssue another voucher? (Y/N): ").strip().lower()
        if again != "y":
            print("Thank you. Program ended.")
            break


if __name__ == "__main__":
    main()
