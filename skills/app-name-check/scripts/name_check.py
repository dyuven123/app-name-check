#!/usr/bin/env python3
"""Check whether an App Store search is still free to use as an app name.

Usage: name_check.py "sky map" --country us
Counts, in the first 25 App Store results, the apps whose name starts with the
search and the apps that have it elsewhere in the name. Uses Apple's public
iTunes Search API. No dependencies, no key.
"""
import argparse
import json
import re
import sys
import unicodedata
import urllib.parse
import urllib.request


def normalize(text):
    text = unicodedata.normalize("NFKD", text.casefold())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"[^\w]+", " ", text).strip()


def position(name, term):
    """Return 'head', 'mid' or None for where the term sits in the name."""
    name, term = f" {normalize(name)} ", f" {normalize(term)} "
    index = name.find(term)
    if index < 0:
        return None
    return "head" if index == 0 else "mid"


def verdict(results, head, mid):
    if results < 5:
        return "check", "Too few results to judge. Look at the store by hand."
    if head:
        return "taken", f"{len(head)} app(s) start their name with it. Expect a much harder climb."
    if len(mid) >= 2:
        return "free, crowded", f"Nobody starts with it, but {len(mid)} apps have it mid-name. That cuts the odds of the top 3 by more than half."
    if mid:
        return "free, one rival", "Nobody starts with it, and one app has it mid-name."
    return "free", "No app in the first 25 results has it in its name. Take it if people really search it."


def search(term, country):
    query = urllib.parse.urlencode({"term": term, "country": country, "entity": "software", "limit": 25})
    request = urllib.request.Request(f"https://itunes.apple.com/search?{query}", headers={"User-Agent": "app-name-check/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)["results"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("term")
    parser.add_argument("--country", default="us", help="two-letter App Store country code")
    args = parser.parse_args()
    try:
        apps = search(args.term, args.country.lower())
    except Exception as error:
        sys.exit(f"Could not reach the iTunes Search API: {error}")
    rows = [{"place": i + 1, "name": a["trackName"], "ratings": a.get("userRatingCount", 0), "in_name": position(a["trackName"], args.term)} for i, a in enumerate(apps)]
    head = [r for r in rows if r["in_name"] == "head"]
    mid = [r for r in rows if r["in_name"] == "mid"]
    call, why = verdict(len(rows), head, mid)
    print(json.dumps({"term": args.term, "country": args.country.upper(), "results": len(rows), "starts_with_it": len(head), "mid_name": len(mid), "call": call, "why": why, "named_apps": head + mid, "first_place": rows[0] if rows else None}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
