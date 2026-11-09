import re
from urllib.parse import urlparse

URGENT = [
    "urgent", "immediately", "act now", "within 24 hours", "account suspended",
    "account blocked", "final warning", "limited time", "verify now", "avoid closure"
]
CREDENTIALS = [
    "password", "otp", "one time password", "pin", "cvv", "card number",
    "login details", "bank details", "recovery code"
]
MONEY = [
    "send money", "transfer now", "pay a fee", "processing fee", "gift card",
    "crypto wallet", "payment required", "claim your prize", "you won"
]
IMPERSONATION = [
    "customer support", "bank security team", "government department",
    "income tax department", "parcel delivery", "your bank", "account team"
]
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "cutt.ly", "ow.ly"}

def _score(signals):
    # Transparent weighted score with a cap; this is a heuristic, not a probability.
    return min(100, sum(weight for _, weight in signals))

def analyse_text(text):
    lowered = text.lower()
    found = []
    for phrase in URGENT:
        if phrase in lowered:
            found.append((f"Urgent or threatening language: “{phrase}”", 14))
            break
    for phrase in CREDENTIALS:
        if phrase in lowered:
            found.append((f"Requests or mentions sensitive credentials: “{phrase}”", 25))
            break
    for phrase in MONEY:
        if phrase in lowered:
            found.append((f"Payment or prize-related wording: “{phrase}”", 20))
            break
    for phrase in IMPERSONATION:
        if phrase in lowered:
            found.append((f"Possible organisation impersonation: “{phrase}”", 12))
            break
    if re.search(r"\bhttps?://", lowered):
        found.append(("Contains a clickable web link", 8))
    if re.search(r"\b(?:\d[ -]*?){13,19}\b", text):
        found.append(("Contains a number pattern resembling a payment-card number", 18))
    if text.count("!") >= 3 or text.isupper() and len(text) > 20:
        found.append(("Unusual pressure-style formatting", 8))

    score = _score(found)
    if score >= 65:
        summary = "Several common scam indicators are present. Do not click links or share information; verify through an official channel."
    elif score >= 35:
        summary = "Some warning signs are present. Pause and independently verify the sender and request."
    else:
        summary = "Few known warning signs were detected. This does not establish that the message is genuine."
    return {"score": score, "signals": [x[0] for x in found], "summary": summary}

def analyse_url(raw_url):
    candidate = raw_url.strip()
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", candidate):
        candidate = "https://" + candidate
    parsed = urlparse(candidate)
    host = (parsed.hostname or "").lower()
    found = []

    if parsed.scheme != "https":
        found.append(("Does not use HTTPS", 15))
    if not host:
        found.append(("Could not parse a valid hostname", 35))
    if host in SHORTENERS:
        found.append(("Uses a URL-shortening service that hides the destination", 25))
    if "@" in parsed.netloc:
        found.append(("Contains an @ symbol in the network location", 25))
    if host and re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", host):
        found.append(("Uses an IP address instead of a recognisable domain", 20))
    if host.count(".") >= 4:
        found.append(("Has an unusually deep subdomain structure", 12))
    if host.startswith("xn--") or ".xn--" in host:
        found.append(("Contains an internationalised/punycode domain label; inspect carefully", 12))
    if len(candidate) > 100:
        found.append(("Unusually long URL", 8))
    if any(word in host for word in ("login", "verify", "secure", "account", "update")):
        found.append(("Hostname contains a commonly abused trust-related word", 8))
    if parsed.query and len(parsed.query) > 80:
        found.append(("Contains a long query string", 5))

    score = _score(found)
    if score >= 65:
        summary = "This URL has multiple warning signs. Do not open it unless you independently confirm the exact domain."
    elif score >= 35:
        summary = "Treat this URL cautiously. Check the domain character by character and reach the organisation through its official website."
    else:
        summary = "Few basic URL warning signs were detected. The destination has not been verified as safe."
    return {"score": score, "signals": [x[0] for x in found], "summary": summary}
