#!/usr/bin/env python3
import csv, os, datetime

# -------------------------------------------------------------
# PATHS
# -------------------------------------------------------------
ROOT = os.path.dirname(os.path.dirname(__file__))
SITE = os.path.join(ROOT, "site_src")
CONTENT = os.path.join(SITE, "content")
os.makedirs(CONTENT, exist_ok=True)

# -------------------------------------------------------------
# HELPERS
# -------------------------------------------------------------
def md_front(title, slug_basename, full_url, desc):
    """Generate YAML-style front matter."""
    return f"""---
title: "{title}"
slug: "{slug_basename}"
url: "{full_url}"
description: "{desc}"
date: {datetime.date.today().isoformat()}
draft: false
---
"""

def section(header, body):
    """Return markdown section."""
    return f"\n\n## {header}\n\n{body}\n"

def build_compare(a, b, avatar):
    """Comparison intro text."""
    return (
        f"**Quick take:** For {avatar}, choose **{a}** if you value granular scaling "
        f"and cost control; choose **{b}** for simpler management and edge caching.\n"
    )

def cta_block(vendors):
    """Call-to-action button block."""
    out = []
    for v in vendors:
        out.append(
            f'- [Start {v} now]([[AFFILIATE_{v.upper()}]]'
            f'?utm_source=hub&utm_medium=button&utm_campaign=stack_select)'
        )
    return "\n".join(out)

# -------------------------------------------------------------
# PAGE GENERATION LOGIC
# -------------------------------------------------------------
def write_page(row):
    """Create a markdown page from a CSV row."""
    kw = row["keyword"]
    it = row["intent_type"]
    slug = row["target_url_slug"].strip().strip("/")  # e.g., compare/cloudways-vs-kinsta
    avatar = row["avatar"]
    angle = row["angle"]

    # Path & directories
    path = os.path.join(CONTENT, f"{slug}.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Front matter data
    slug_basename = slug.split("/")[-1]
    full_url = f"/{slug}/"
    title = kw
    desc = f"{kw} for {avatar} — {angle}."
    body = md_front(title, slug_basename, full_url, desc)

    # ---- Compare intent ----
    if it == "compare" and " vs " in kw:
        a, b = [x.strip() for x in kw.split(" vs ")]
        body += section("Summary verdict", build_compare(a, b, avatar))
        body += section(
            "TL;DR table",
            "| Feature | "
            + a
            + " | "
            + b
            + " |\n|---|---|---|\n| CDN | Yes | Yes |\n| Backups | Yes | Yes |\n| Price | Lower @ low scale | Higher @ start |",
        )
        body += section(
            "When to choose each",
            f"- Pick **{a}**: lower entry price and granular scale.\n"
            f"- Pick **{b}**: managed simplicity and edge caching.",
        )
        body += section(
            "10-minute setup",
            "1) Sign up host\n2) Point domain A record\n3) Install WordPress\n"
            "4) Install GeneratePress\n5) Add ShortPixel & RankMath\n6) Add cache\n7) Test PageSpeed.",
        )
        body += section(
            "Costs & risks",
            "- Hosting billed monthly; plugin renewals yearly.\n"
            "- Beware oversizing server too early.",
        )
        body += section("Start here", cta_block([a, b]))

    # ---- Best intent ----
    elif it == "best":
        body += section(
            "Summary verdict", f"For {avatar}: fast, low-bloat stack focused on {angle}."
        )
        body += section(
            "Top picks",
            "- Cloudways + GeneratePress\n"
            "- Kinsta + GeneratePress\n"
            "- ShortPixel + RankMath\n"
            "- Umami analytics",
        )
        body += section("Copy settings", "See hub for JSON presets.")
        body += section(
            "Start here", cta_block(["Cloudways", "Kinsta", "GeneratePress"])
        )

    # ---- Pricing intent ----
    elif it == "pricing":
        body += section(
            "How pricing works",
            "Breakdown of tiers, overages, and add-ons. Start small; scale later.",
        )
        body += section(
            "Examples", "- 10k visits/mo → DO 1GB ok\n- 50k+ → increase RAM/CPU"
        )
        body += section("Start here", cta_block(["Cloudways"]))

    # ---- Fix intent ----
    elif it == "fix":
        body += section(
            "Fix in 10 minutes",
            "1) GeneratePress\n2) Lazy load images\n3) Compress with ShortPixel\n"
            "4) Delay non-critical JS\n5) Cache",
        )
        body += section(
            "Validation",
            "Run PageSpeed Insights. Target LCP < 2.5s, CLS < 0.1.",
        )
        body += section("Tools", cta_block(["ShortPixel", "WP Rocket"]))

    # ---- Fallback ----
    else:
        body += "\nContent coming soon."

    # Write to file
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)

# -------------------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------------------
if __name__ == "__main__":
    csv_path = os.path.join(ROOT, "data", "keywords_master.csv")
    with open(csv_path, newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            write_page(row)
    print("✅ Pages generated successfully.")
