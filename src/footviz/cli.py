"""footviz command line.

  footviz info   <events.json>                    teams, score, xG, lineups
  footviz shots  <events.json>                    every shot sequence with roles
  footviz render <events.json> --out DIR          all figures for the match
  footviz fetch  <match_id> --out FILE            download a match from StatsBomb open data
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt

from footviz import plots
from footviz.match import Match, fetch_events, load_events
from footviz.sequences import shot_sequences


def _safe(name: str) -> str:
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in name)


def cmd_info(a: argparse.Namespace) -> int:
    m = Match(load_events(a.events))
    score, xg = m.score(), m.xg()
    for t in m.teams:
        print(f"{t}: {score[t]} goals, {xg[t]:.2f} xG, formation {m.formation(t)}")
        for p in m.lineups[t]:
            print(f"   {p.jersey:>2}  {p.position:<22} {p.name}")
    print(f"{len(m.events)} events, {len(m.shots())} shots")
    return 0


def cmd_shots(a: argparse.Namespace) -> int:
    m = Match(load_events(a.events))
    for seq in shot_sequences(m):
        chain = " → ".join(f"{x.player} ({x.type})" for x in seq.build_up) or "(none)"
        print(f"[{seq.index:>2}] {seq.team:<20} {seq.label}")
        print(f"      build-up: {chain}")
    return 0


def cmd_render(a: argparse.Namespace) -> int:
    m = Match(load_events(a.events))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    seqs = shot_sequences(m)
    written = 0

    def save(fig, name: str) -> None:
        nonlocal written
        fig.savefig(out / f"{_safe(name)}.png", dpi=a.dpi, bbox_inches="tight")
        plt.close(fig)
        written += 1

    save(plots.xg_timeline(m), "xg-timeline")
    save(plots.xg_shot_map(m), "xg-shot-map")
    for t in m.teams:
        save(plots.average_positions(m, t, True), f"avg-positions-{t}-in-possession")
        save(plots.average_positions(m, t, False), f"avg-positions-{t}-out-of-possession")
        save(plots.key_actions_heatmap(m, t, seqs), f"key-actions-{t}")
    for seq in seqs:
        save(plots.shot_sequence(m, seq),
             f"shot-{seq.index:02d}-{seq.minute:02d}{seq.second:02d}-{seq.team}-{seq.outcome}")
    if a.heatmaps:
        for t in m.teams:
            for p in m.lineups[t]:
                for action in a.heatmaps:
                    if len(m.player_actions(p.name, action)) >= 3:
                        save(plots.action_heatmap(m, p.name, action),
                             f"heatmap-{t}-{p.jersey:02d}-{p.name}-{action}")
    print(f"wrote {written} figures to {out}")
    return 0


def cmd_fetch(a: argparse.Namespace) -> int:
    events = fetch_events(a.match_id)
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(events), encoding="utf-8")
    print(f"wrote {len(events)} events to {a.out}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="footviz", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("info", help="teams, score, xG, lineups")
    s.add_argument("events")
    s.set_defaults(fn=cmd_info)
    s = sub.add_parser("shots", help="every shot sequence with its build-up")
    s.add_argument("events")
    s.set_defaults(fn=cmd_shots)
    s = sub.add_parser("render", help="write all figures for a match")
    s.add_argument("events")
    s.add_argument("--out", default="figures")
    s.add_argument("--dpi", type=int, default=130)
    s.add_argument("--heatmaps", nargs="*", metavar="ACTION",
                   help="also render per-player heatmaps for these action types, "
                        "e.g. --heatmaps Pass 'Ball Receipt*' Pressure")
    s.set_defaults(fn=cmd_render)
    s = sub.add_parser("fetch")
    s.add_argument("match_id", type=int)
    s.add_argument("--out", required=True)
    s.set_defaults(fn=cmd_fetch)

    a = p.parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
