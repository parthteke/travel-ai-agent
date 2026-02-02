# ✈️ Travel AI Agent

An AI-assisted travel itinerary planning application that generates trips based on **natural language input**, **budget constraints**, and **group size**.

This project was built as part of an academic requirement for **M.Sc. Computer Science (2nd Year)** and focuses on **practical system design**, not hype.

---

## 🚀 Features

- Accepts **natural language travel queries**
- Extracts trip details using NLP
- Recommends:
  - Transport (flight – budget-based)
  - Hotel accommodation
  - Tourist attractions
- Provides:
  - Budget breakdown
  - Cost per person
  - **Minimum budget estimation** if the trip is not feasible
- Interactive web UI using Streamlit

---

## 🧠 How It Works

1. User enters a query like:
# ✈️ Travel AI Agent

An AI-assisted travel itinerary planning application that generates trips based on **natural language input**, **budget constraints**, and **group size**.

This project was built as part of an academic requirement for **M.Sc. Computer Science (2nd Year)** and focuses on **practical system design**, not hype.

---

## 🚀 Features

- Accepts **natural language travel queries**
- Extracts trip details using NLP
- Recommends:
  - Transport (flight – budget-based)
  - Hotel accommodation
  - Tourist attractions
- Provides:
  - Budget breakdown
  - Cost per person
  - **Minimum budget estimation** if the trip is not feasible
- Interactive web UI using Streamlit

---

## 🧠 How It Works

1. User enters a query like:
PLAN A 3 DAYS TRIP FROM MUMBAI TO PUNE FOR3 PEOPLE UNDER 200000

2. NLP module extracts:
- Source
- Destination
- Days
- Budget
- Number of people
3. Business logic:
- Splits budget into transport and hotel portions
- Selects best available options from database
- Estimates minimum budget if required
4. Results are displayed via a Streamlit UI.

---
