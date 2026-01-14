import streamlit as st
from itinerary import plan_trip
from nlp import extract_trip_details

st.set_page_config(
    page_title="Travel AI Agent",
    page_icon="✈️",
    layout="centered"
)

st.title("✈️ Travel AI Agent")
st.markdown("Plan your trip and get minimum budget estimation.")

query = st.text_input(
    "Example: Plan a 3 day trip to Goa from Pune for 4 people under 20000"
)

if st.button("Plan Trip"):
    details = extract_trip_details(query)

    st.subheader("Extracted Details")
    st.json(details)

    required = ["source", "destination", "days", "budget", "people"]

    if not all(details.get(k) is not None for k in required):
        st.warning("Could not extract all required details.")
    else:
        plan = plan_trip(
            details["source"],
            details["destination"],
            details["days"],
            details["budget"],
            details["people"]
        )

        if plan["status"] == "failed":
            st.error(plan["reason"])
            st.warning(
                f"💰 Minimum budget required: ₹{plan['minimum_budget_required']}"
            )
            st.info(plan["suggestion"])

        else:
            st.success("Trip planned successfully!")

            st.subheader("✈️ Transport")
            st.json(plan["transport"])

            st.subheader("🏨 Hotel")
            hotel = plan["hotel"]
            st.write(f"Name: {hotel['name']}")
            st.write(f"Price per night: ₹{hotel['price_per_night']}")
            st.write(f"Total hotel cost: ₹{hotel['total_hotel_cost']}")
            st.write(f"Rating: ⭐ {hotel['rating']}")

            st.subheader("💰 Budget Summary")
            budget = plan["budget_summary"]
            st.write(f"Total Budget: ₹{plan['total_budget']}")
            st.write(f"Total Spent: ₹{budget['total_spent']}")
            st.write(f"Remaining Budget: ₹{budget['remaining_budget']}")
            st.write(f"Cost per Person: ₹{budget['cost_per_person']}")

            st.subheader("🎡 Attractions")
            for a in plan["attractions"]:
                st.write(f"- {a['name']} ({a['type']}) ⭐ {a['rating']}")
