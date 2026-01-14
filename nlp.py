# nlp_parser.py
import spacy
import re
import difflib

nlp = spacy.load("en_core_web_sm")

# Optional: pass in a list of known cities (e.g. from your DB) to disambiguate
DEFAULT_KNOWN_CITIES = [
    "Pune","Goa","Mumbai","Delhi","Jaipur","Hyderabad","Chennai",
    "Bangalore","Kolkata","Manali","Nagpur","Bengaluru"
]

def _normalize_city(name):
    return " ".join(name.split()).title()

def _closest_city_match(name, known_cities, cutoff=0.6):
    # use difflib to find a close known-city match
    name = name.strip()
    matches = difflib.get_close_matches(name, known_cities, n=1, cutoff=cutoff)
    return matches[0] if matches else None

def _pull_after_preposition(text_lower, prep):
    """
    Return the word(s) after a preposition like 'from' or 'to' using regex fallback.
    This returns the first match (greedy until next preposition or number).
    """
    pattern = rf"{prep}\s+([a-zA-Z\s]+?)(?:\s+(?:to|from|for|under|₹|\d|$))"
    m = re.search(pattern, text_lower)
    if m:
        return m.group(1).strip().title()
    return None

def extract_trip_details(text, known_cities=None, debug=False):
    """
    Robust extractor:
      - returns dict: {source, destination, days, budget, people}
      - known_cities: optional list to match city names against (recommended)
      - debug: if True, returns extra diagnostics under key '_debug'
    """
    if known_cities is None:
        known_cities = DEFAULT_KNOWN_CITIES

    doc = nlp(text)
    text_lower = text.lower()
    
    transport_pref = None

    if "train" in text_lower:
      transport_pref = "train"
    elif "flight" in text_lower or "plane" in text_lower or "air" in text_lower:
     transport_pref = "flight"

    source = None
    destination = None
    days = None
    budget = None
    people = None
    debug_info = {"ents": [(ent.text, ent.label_) for ent in doc.ents], "candidates": []}

    # --- days ---
    m_days = re.search(r"(\d+)\s*(?:-|\s)?\s*(?:day|days|night|nights)", text_lower)
    if m_days:
        days = int(m_days.group(1))

    # --- budget (₹ or plain numbers) ---
    m_budget = re.search(r"(?:₹\s?|\brs\.?\s?)?(\d{3,7})", text.replace(",", ""))
    if m_budget:
        budget = int(re.sub(r"[^\d]", "", m_budget.group(0)))

    # --- people extraction ---
    m_people = re.search(r"(\d+)\s*(people|persons|friends|members|guests|person)", text_lower)
    if m_people:
        people = int(m_people.group(1))
    else:
        # also handle "for 2" pattern
        m_for = re.search(r"for\s+(\d+)\b", text_lower)
        if m_for:
            people = int(m_for.group(1))
    if not people:
        people = 1

    # --- collect spaCy GPEs (city candidates) ---
    ents = [ent.text for ent in doc.ents if ent.label_ in ("GPE", "LOC")]
    debug_info["candidates"].extend(ents)

    # --- rule-based patterns (explicit) ---
    # Case A: "from X to Y"
    m = re.search(r"from\s+([a-zA-Z\s]+?)\s+to\s+([a-zA-Z\s]+)", text_lower)
    if m:
        src = _normalize_city(m.group(1))
        dst = _normalize_city(m.group(2))
        # optionally align to known cities
        src_match = _closest_city_match(src, known_cities) or src
        dst_match = _closest_city_match(dst, known_cities) or dst
        source, destination = src_match, dst_match

    # Case B: "to Y from X"  (your problematic input)
    if not source and not destination:
        m2 = re.search(r"to\s+([a-zA-Z\s]+?)\s+from\s+([a-zA-Z\s]+)", text_lower)
        if m2:
            dst = _normalize_city(m2.group(1))
            src = _normalize_city(m2.group(2))
            src_match = _closest_city_match(src, known_cities) or src
            dst_match = _closest_city_match(dst, known_cities) or dst
            source, destination = src_match, dst_match

    # Case C: "X to Y" simple pattern (e.g. "Pune to Goa")
    if not source and not destination:
        m3 = re.search(r"([A-Za-z\s]+)\s+to\s+([A-Za-z\s]+)", text)
        if m3:
            a = _normalize_city(m3.group(1))
            b = _normalize_city(m3.group(2))
            a_match = _closest_city_match(a, known_cities) or a
            b_match = _closest_city_match(b, known_cities) or b
            source, destination = a_match, b_match

    # Case D: use spaCy ents but decide order using nearby prepositions
    if not source and not destination and ents:
        # if sentence contains 'from' -> find which ent occurs after 'from'
        if "from" in text_lower:
            after_from = _pull_after_preposition(text_lower, "from")
            if after_from:
                src_candidate = _closest_city_match(after_from, known_cities) or _normalize_city(after_from)
                source = src_candidate
                # destination: pick an ent that is not source
                for e in ents:
                    e_norm = _normalize_city(e)
                    if e_norm != source:
                        destination = _closest_city_match(e_norm, known_cities) or e_norm
                        break
        # if sentence contains 'to' -> prefer the ent after 'to' as destination
        if not destination and "to" in text_lower:
            after_to = _pull_after_preposition(text_lower, "to")
            if after_to:
                dst_candidate = _closest_city_match(after_to, known_cities) or _normalize_city(after_to)
                destination = dst_candidate
                # source: choose another ent
                for e in ents:
                    e_norm = _normalize_city(e)
                    if e_norm != destination:
                        source = _closest_city_match(e_norm, known_cities) or e_norm
                        break

    # Final fallback: if spaCy gave two ents, guess order using word positions:
    if not (source and destination) and len(ents) >= 2:
        # map ent -> index
        ent_positions = {ent.text: text.find(ent.text) for ent in doc.ents if ent.label_ in ("GPE","LOC")}
        sorted_ents = sorted(ent_positions.items(), key=lambda kv: kv[1])
        if len(sorted_ents) >= 2:
            a, b = _normalize_city(sorted_ents[0][0]), _normalize_city(sorted_ents[1][0])
            source = _closest_city_match(a, known_cities) or a
            destination = _closest_city_match(b, known_cities) or b

    # One-city case
    if not destination and len(ents) == 1:
        destination = _closest_city_match(_normalize_city(ents[0]), known_cities) or _normalize_city(ents[0])

    # normalize results
    if source:
        source = _normalize_city(source)
    if destination:
        destination = _normalize_city(destination)

    result = {
        "source": source,
        "destination": destination,
        "days": days,
        "budget": budget,
        "people": people
    }
    if debug:
        result["_debug"] = debug_info
    return result

