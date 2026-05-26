"""
Mission Control telemetry updater.

Fetches recent activity from the GitHub API and patches the three SVG assets
(hud-header.svg, trajectory.svg, telemetry.svg) in place.

Stdlib only. Designed to run inside .github/workflows/telemetry.yml.
"""

from __future__ import annotations

import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

USER = os.environ.get("GH_USER", "yash-vks-chauhan")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
MISSION_START = dt.date(2023, 8, 1)  # SRM B.Tech start

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"


def api(path: str) -> object:
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "mission-control-telemetry",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def fetch_events() -> list[dict]:
    events: list[dict] = []
    for page in range(1, 4):  # up to 300 events
        try:
            chunk = api(f"/users/{USER}/events/public?per_page=100&page={page}")
        except urllib.error.HTTPError as e:
            print(f"events page {page} failed: {e}", file=sys.stderr)
            break
        if not chunk:
            break
        events.extend(chunk)
    return events


def fetch_repos() -> list[dict]:
    repos: list[dict] = []
    for page in range(1, 4):
        try:
            chunk = api(f"/users/{USER}/repos?per_page=100&page={page}&type=owner&sort=pushed")
        except urllib.error.HTTPError as e:
            print(f"repos page {page} failed: {e}", file=sys.stderr)
            break
        if not chunk:
            break
        repos.extend(chunk)
    return repos


def aggregate_languages(repos: list[dict]) -> dict[str, int]:
    totals: dict[str, int] = {}
    for r in repos:
        if r.get("fork"):
            continue
        try:
            langs = api(f"/repos/{USER}/{r['name']}/languages")
        except urllib.error.HTTPError:
            continue
        for k, v in langs.items():
            totals[k] = totals.get(k, 0) + int(v)
    return totals


def parse_iso(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00"))


def t_plus_label(today: dt.date) -> str:
    """Mission elapsed time as Yy Mm Dd."""
    years = today.year - MISSION_START.year
    months = today.month - MISSION_START.month
    days = today.day - MISSION_START.day
    if days < 0:
        months -= 1
        # borrow days from previous month
        prev_month = (today.replace(day=1) - dt.timedelta(days=1))
        days += prev_month.day
    if months < 0:
        years -= 1
        months += 12
    return f"{years}y {months}m {days}d"


def relative_pretty(then: dt.datetime, now: dt.datetime) -> str:
    delta = now - then
    sec = int(delta.total_seconds())
    if sec < 60:
        return f"{sec}s ago"
    if sec < 3600:
        return f"{sec // 60}m ago"
    if sec < 86400:
        return f"{sec // 3600}h ago"
    return f"{sec // 86400}d ago"


def daily_commit_counts(events: list[dict], now: dt.datetime, days: int = 30) -> list[int]:
    counts = [0] * days
    cutoff = now - dt.timedelta(days=days)
    for ev in events:
        if ev.get("type") != "PushEvent":
            continue
        when = parse_iso(ev["created_at"])
        if when < cutoff:
            continue
        commits = ev.get("payload", {}).get("commits") or []
        # exclude merge / auto-bot-ish commits would go here; trusting all for now
        idx = days - 1 - (now.date() - when.date()).days
        if 0 <= idx < days:
            counts[idx] += len(commits)
    return counts


def latest_commits(events: list[dict], n: int = 5) -> list[dict]:
    out: list[dict] = []
    for ev in events:
        if ev.get("type") != "PushEvent":
            continue
        when = parse_iso(ev["created_at"])
        repo = (ev.get("repo") or {}).get("name", "")
        repo_short = repo.split("/", 1)[-1] if "/" in repo else repo
        commits = ev.get("payload", {}).get("commits") or []
        # newest commit in the push first
        for c in reversed(commits):
            sha = (c.get("sha") or "")[:7]
            msg = (c.get("message") or "").splitlines()[0]
            out.append({"when": when, "repo": repo_short, "sha": sha, "msg": msg})
            if len(out) >= n:
                return out
    return out


def build_bars_block(counts: list[int]) -> str:
    """Produce the inner <g id='tel-bars'> markup."""
    n = len(counts)
    chart_y_bottom = 220
    chart_y_top = 50
    chart_h = chart_y_bottom - chart_y_top  # 170
    x_start = 46
    bar_w = 18
    step = 22

    mx = max(counts) if any(counts) else 1
    avg = sum(counts) / n if n else 0
    var = sum((c - avg) ** 2 for c in counts) / n if n else 0
    std = var ** 0.5
    anom_threshold = avg + 2 * std if std > 0 else mx + 1

    pieces = []
    for i, c in enumerate(counts):
        x = x_start + i * step
        if mx <= 0:
            h = 0
        else:
            h = round((c / mx) * chart_h)
        y = chart_y_bottom - h
        is_zero = c == 0
        is_anom = c >= anom_threshold and c > 0
        if is_zero:
            fill, opacity = "#6E7681", "0.3"
        elif is_anom:
            fill, opacity = "#F59E0B", "1"
        else:
            opacity = f"{0.5 + 0.4 * (c / mx):.2f}" if mx else "0.5"
            fill = "#38BDF8"
        origin_x = x + bar_w / 2
        pieces.append(
            f'      <g style="transform-origin: {origin_x:g}px {chart_y_bottom}px" class="bar" transform="translate({x} 0)">'
            f'<rect width="{bar_w}" height="{h}" y="{y}" fill="{fill}" opacity="{opacity}"/></g>'
        )
    return "\n".join(pieces)


def patch_block(svg: str, tag: str, elem_id: str, new_inner: str) -> str:
    """Replace the inner content of <{tag} id='{elem_id}' ...>...</{tag}>."""
    pattern = re.compile(
        rf'(<{tag}\b[^>]*\bid="{re.escape(elem_id)}"[^>]*>)(.*?)(</{tag}>)',
        re.DOTALL,
    )
    if not pattern.search(svg):
        print(f"WARN: no <{tag} id='{elem_id}'> found", file=sys.stderr)
        return svg
    return pattern.sub(lambda m: m.group(1) + new_inner + m.group(3), svg, count=1)


def replace_region(svg: str, sentinel: str, new_inner: str) -> str:
    """Replace the content between `<!--SENTINEL:BEGIN-->` and `<!--SENTINEL:END-->`."""
    pattern = re.compile(
        rf'(<!--{sentinel}:BEGIN-->)(.*?)(<!--{sentinel}:END-->)',
        re.DOTALL,
    )
    if not pattern.search(svg):
        print(f"WARN: no sentinel region {sentinel}", file=sys.stderr)
        return svg
    return pattern.sub(lambda m: m.group(1) + "\n" + new_inner + "\n    " + m.group(3), svg, count=1)


def patch_attr(svg: str, tag: str, elem_id: str, attr: str, new_value: str) -> str:
    """Replace attr='...' for <{tag} id='{elem_id}'>."""
    # Find the tag, then replace the attr inside it.
    tag_pattern = re.compile(
        rf'(<{tag}\b[^>]*\bid="{re.escape(elem_id)}"[^>]*?>)',
    )
    m = tag_pattern.search(svg)
    if not m:
        print(f"WARN: no <{tag} id='{elem_id}'> for attr {attr}", file=sys.stderr)
        return svg
    opening = m.group(1)
    if re.search(rf'\b{attr}="[^"]*"', opening):
        new_opening = re.sub(rf'\b{attr}="[^"]*"', f'{attr}="{new_value}"', opening)
    else:
        new_opening = opening[:-1] + f' {attr}="{new_value}">'
    return svg[: m.start()] + new_opening + svg[m.end():]


def update_hud(commits_30d: int, last_push: dt.datetime | None, now: dt.datetime) -> None:
    path = ASSETS / "hud-header.svg"
    svg = path.read_text(encoding="utf-8")
    svg = patch_block(svg, "text", "hud-elapsed", t_plus_label(now.date()))
    svg = patch_block(svg, "tspan", "hud-commits", str(commits_30d))
    last = relative_pretty(last_push, now) if last_push else "no recent"
    svg = patch_block(svg, "tspan", "hud-lastpush", last)
    path.write_text(svg, encoding="utf-8")


def update_trajectory(now: dt.datetime) -> None:
    path = ASSETS / "trajectory.svg"
    svg = path.read_text(encoding="utf-8")
    label = now.strftime("%b %Y")
    svg = patch_block(svg, "text", "traj-now", label)
    path.write_text(svg, encoding="utf-8")


def update_telemetry(counts: list[int], langs: dict[str, int], repos: list[dict],
                     log: list[dict], now: dt.datetime) -> None:
    path = ASSETS / "telemetry.svg"
    svg = path.read_text(encoding="utf-8")

    # updated timestamp
    svg = patch_block(svg, "tspan", "tel-updated", now.strftime("%Y-%m-%d %H:%MZ"))

    # bars (sentinel-delimited region)
    new_bars = build_bars_block(counts)
    svg = replace_region(svg, "BARS",
                         '    <g id="tel-bars">\n' + new_bars + '\n    </g>')

    # languages: top 4 + Other
    total = sum(langs.values()) or 1
    ordered = sorted(langs.items(), key=lambda kv: kv[1], reverse=True)
    top4 = ordered[:4]
    other = sum(v for _, v in ordered[4:])
    rows: list[tuple[str, float]] = [(k, v / total * 100) for k, v in top4]
    if other > 0 and len(ordered) > 4:
        rows.append(("Other", other / total * 100))
    while len(rows) < 5:
        rows.append(("--", 0.0))

    max_bar = 330
    new_langs_inner = build_langs_block(rows, max_bar)
    svg = replace_region(svg, "LANGS",
                         '    <g id="tel-langs" class="mono" font-size="10" transform="translate(14 44)">\n'
                         + new_langs_inner + '\n    </g>')

    # stats
    repo_count = len([r for r in repos if not r.get("fork")])
    star_count = sum(int(r.get("stargazers_count") or 0) for r in repos if not r.get("fork"))
    cmt_total = sum(counts)  # over last 30d window
    svg = patch_block(svg, "text", "tel-stat-repos", str(repo_count))
    svg = patch_block(svg, "text", "tel-stat-stars", str(star_count))
    svg = patch_block(svg, "text", "tel-stat-commits", str(cmt_total))

    # log
    for i in range(5):
        entry = log[i] if i < len(log) else None
        if entry:
            t_label = relative_pretty(entry["when"], now)
            sha = entry["sha"] or "-------"
            repo = entry["repo"] or "--"
            msg = entry["msg"] or "--"
            if len(msg) > 60:
                msg = msg[:57] + "..."
        else:
            t_label = "--:--"
            sha = "-------"
            repo = "--"
            msg = "--"
        svg = patch_block(svg, "text", f"tel-log-t{i+1}", t_label)
        svg = patch_block(svg, "text", f"tel-log-s{i+1}", sha)
        svg = patch_block(svg, "text", f"tel-log-r{i+1}", esc(repo))
        svg = patch_block(svg, "text", f"tel-log-m{i+1}", esc(msg))

    path.write_text(svg, encoding="utf-8")


def build_langs_block(rows: list[tuple[str, float]], max_bar: int) -> str:
    out = []
    for i, (name, pct) in enumerate(rows):
        w = round((pct / 100.0) * max_bar)
        op = max(0.3, 1 - 0.15 * i)
        y_offset = i * 30
        out.append(
            f'      <g transform="translate(0 {y_offset})">\n'
            f'        <text class="text">{esc(name)}</text>\n'
            f'        <text x="344" y="0" text-anchor="end" class="cyan" id="tel-l{i+1}-pct">{pct:.1f}%</text>\n'
            f'        <rect x="0"  y="6" width="330" height="6" fill="#0B0F14" stroke="#1F2937"/>\n'
            f'        <rect x="0"  y="6" width="{w}"  height="6" fill="#38BDF8" id="tel-l{i+1}-bar" opacity="{op:.2f}"/>\n'
            f'      </g>'
        )
    return "\n".join(out)


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )


def main() -> None:
    now = dt.datetime.now(dt.timezone.utc)

    print(f"== mission-control telemetry tick @ {now.isoformat()} ==")
    events = fetch_events()
    print(f"events fetched: {len(events)}")
    repos = fetch_repos()
    print(f"repos fetched:  {len(repos)}")
    langs = aggregate_languages(repos)
    print(f"languages:      {sorted(langs.items(), key=lambda kv: -kv[1])[:6]}")

    counts = daily_commit_counts(events, now)
    last_push = max(
        (parse_iso(ev["created_at"]) for ev in events if ev.get("type") == "PushEvent"),
        default=None,
    )
    log = latest_commits(events)

    update_hud(sum(counts), last_push, now)
    update_trajectory(now)
    update_telemetry(counts, langs, repos, log, now)
    print("== telemetry assets patched ==")


if __name__ == "__main__":
    main()
