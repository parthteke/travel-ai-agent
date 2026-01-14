import math
from hotel_logic import choose_best_hotel
from flight_logic import get_cheapest_flight
from attractions import get_top_attractions


def plan_trip(source, destination, days, total_budget, people):
    # -----------------------------
    # 1. BUDGET SPLIT (FIXED RULE)
    # -----------------------------
    transport_budget = total_budget * 0.4
    hotel_budget = total_budget * 0.6

    max_price_per_person = transport_budget / people

    # -----------------------------
    # 2. TRANSPORT (ESTIMATED)
    # -----------------------------
    flight = get_cheapest_flight(source, destination, max_price_per_person)

    if "message" in flight:
        # Estimate minimum transport cost if no flight found
        min_transport_cost = transport_budget * 1.2
        transport = {"message": "No flight found under budget"}
    else:
        min_transport_cost = flight["price"] * people
        transport = {
            "mode": "Flight",
            "source": flight["source"],
            "destination": flight["destination"],
            "price_per_person": flight["price"],
            "total_price": min_transport_cost,
            "airline": flight["airline"]
        }

    # -----------------------------
    # 3. HOTEL
    # -----------------------------
    rooms_needed = math.ceil(people / 2)

    hotel = choose_best_hotel(destination, hotel_budget)

    if "message" in hotel:
        minimum_required = min_transport_cost + hotel_budget

        return {
            "status": "failed",
            "reason": "Budget too low to plan this trip.",
            "minimum_budget_required": round(minimum_required),
            "suggestion": (
                f"Minimum budget required (transport + hotel) "
                f"is approximately ₹{round(minimum_required)}."
            )
        }

    total_hotel_cost = hotel["price"] * days * rooms_needed

    # -----------------------------
    # 4. MINIMUM BUDGET CHECK
    # -----------------------------
    minimum_required = min_transport_cost + total_hotel_cost

    if total_budget < minimum_required:
        return {
            "status": "failed",
            "reason": "Budget too low to plan this trip.",
            "minimum_budget_required": round(minimum_required),
            "suggestion": (
                f"Minimum budget required (transport + hotel) "
                f"is approximately ₹{round(minimum_required)}."
            )
        }

    # -----------------------------
    # 5. ATTRACTIONS
    # -----------------------------
    attractions = get_top_attractions(destination, limit=3)

    # -----------------------------
    # 6. BUDGET SUMMARY
    # -----------------------------
    total_spent = min_transport_cost + total_hotel_cost
    remaining_budget = total_budget - total_spent
    cost_per_person = total_spent / people

    return {
        "status": "success",
        "source": source,
        "destination": destination,
        "days": days,
        "people": people,
        "total_budget": total_budget,

        "transport": transport,

        "hotel": {
            "name": hotel["name"],
            "location": destination,
            "price_per_night": hotel["price"],
            "rooms_needed": rooms_needed,
            "total_hotel_cost": total_hotel_cost,
            "rating": hotel["rating"]
        },

        "budget_summary": {
            "transport_cost": min_transport_cost,
            "hotel_cost": total_hotel_cost,
            "total_spent": total_spent,
            "remaining_budget": remaining_budget,
            "cost_per_person": round(cost_per_person, 2)
        },

        "attractions": attractions
    }
