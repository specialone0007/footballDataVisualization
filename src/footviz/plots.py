"""The six match visualisations. Every function returns a matplotlib Figure; nothing is saved
here. Pitches come from mplsoccer with StatsBomb coordinates.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from mplsoccer import Pitch  # noqa: E402

from footviz.match import PITCH_LENGTH, PITCH_WIDTH, Match  # noqa: E402
from footviz.sequences import ShotSequence  # noqa: E402

TEAM_COLOURS = ("#1f77b4", "#d62728")
OUTCOME_MARKERS = {"Goal": ("*", 420), "Saved": ("o", 160), "Blocked": ("X", 160),
                   "Off T": ("s", 130), "Post": ("P", 160), "Wayward": ("s", 130),
                   "Saved Off Target": ("o", 160), "Saved to Post": ("o", 160)}
PITCH_KW = dict(pitch_type="statsbomb", pitch_color="#f6f6f4", line_color="#555555",
                linewidth=1.2)


def _pitch(**kw) -> tuple[Pitch, Figure, plt.Axes]:
    pitch = Pitch(**PITCH_KW, **kw)
    fig, ax = pitch.draw(figsize=(9, 6.2))
    return pitch, fig, ax


def _flip(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return PITCH_LENGTH - x, PITCH_WIDTH - y


# ------------------------------------------------------------------------------------------ 1
def average_positions(match: Match, team: str, in_possession: bool) -> Figure:
    df = match.average_positions(team, in_possession)
    pitch, fig, ax = _pitch()
    colour = TEAM_COLOURS[match.teams.index(team)]
    pitch.scatter(df.x, df.y, s=df.n.clip(lower=40) * 3 + 300, ax=ax, color=colour, alpha=0.85,
                  edgecolors="white", linewidth=1.5, zorder=3)
    for _, r in df.iterrows():
        ax.annotate(str(r.jersey), (r.x, r.y), ha="center", va="center", color="white",
                    fontsize=11, fontweight="bold", zorder=4)
    phase = "in possession" if in_possession else "out of possession"
    ax.set_title(f"{team} · average positions {phase}\nformation {match.formation(team)} · "
                 f"marker size ∝ number of events · attacking →", loc="left", fontsize=11)
    return fig


# ------------------------------------------------------------------------------------------ 2
def action_heatmap(match: Match, player: str, action: str) -> Figure:
    df = match.player_actions(player, action)
    pitch, fig, ax = _pitch()
    if len(df) >= 3:
        pitch.kdeplot(df.x, df.y, ax=ax, fill=True, levels=40, thresh=0.03, cmap="Reds",
                      alpha=0.85, zorder=1)
    pitch.scatter(df.x, df.y, ax=ax, s=18, color="#222222", alpha=0.7, zorder=3)
    team = next((t for t in match.teams if match.jersey(t, player) is not None), "")
    ax.set_title(f"{player} ({team}) · {action} · {len(df)} events · attacking →",
                 loc="left", fontsize=11)
    return fig


# ------------------------------------------------------------------------------------------ 3
def shot_sequence(match: Match, seq: ShotSequence) -> Figure:
    pitch, fig, ax = _pitch()
    jersey = {p.name: p.jersey for p in match.lineups[seq.team]}
    subs = {}

    def number(player: str) -> str:
        if player in jersey:
            return str(jersey[player])
        subs.setdefault(player, f"S{len(subs) + 1}")
        return subs[player]

    pts = [(a.x, a.y, a.type, a.player) for a in seq.build_up]
    pts.append((seq.x, seq.y, "Shot", seq.shooter))
    styles = {"Pass": dict(ls=":", color="#8e44ad"), "Carry": dict(ls="-", color="#7f8c8d"),
              "Dribble": dict(ls="-.", color="#2980b9")}
    for (x0, y0, t, _), (x1, y1, _, _) in zip(pts, pts[1:], strict=False):
        ax.plot([x0, x1], [y0, y1], lw=2, zorder=2, **styles.get(t, styles["Carry"]))
    if seq.end_x is not None:
        ax.plot([seq.x, seq.end_x], [seq.y, seq.end_y], color="#c0392b", lw=2.2, zorder=2)
        marker, size = OUTCOME_MARKERS.get(seq.outcome, ("s", 130))
        pitch.scatter(seq.end_x, seq.end_y, ax=ax, marker=marker, s=size, color="#c0392b",
                      edgecolors="white", zorder=4)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    pitch.scatter(xs, ys, ax=ax, s=380, color="#1f77b4", edgecolors="white", linewidth=1.5,
                  zorder=3)
    for x, y, _, player in pts:
        ax.annotate(number(player), (x, y), ha="center", va="center", color="white",
                    fontsize=10, fontweight="bold", zorder=5)
    handles = [plt.Line2D([], [], **styles["Pass"], lw=2, label="pass"),
               plt.Line2D([], [], **styles["Carry"], lw=2, label="carry"),
               plt.Line2D([], [], **styles["Dribble"], lw=2, label="dribble"),
               plt.Line2D([], [], color="#c0392b", lw=2, label="shot")]
    ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.01), ncol=4,
              fontsize=8, frameon=False)
    ax.set_title(f"{seq.team} · shot at {seq.minute:02d}:{seq.second:02d} · {seq.shooter} · "
                 f"{seq.outcome} · xG {seq.xg:.2f}\n"
                 f"{len(seq.build_up)} on-ball actions before the shot · numbers are shirts"
                 + (" · " + ", ".join(f"{v} = {k}" for k, v in subs.items()) if subs else ""),
                 loc="left", fontsize=10)
    return fig


# ------------------------------------------------------------------------------------------ 4
def xg_timeline(match: Match) -> Figure:
    shots = match.shots()
    fig, ax = plt.subplots(figsize=(9, 4.6))
    score, xg = match.score(), match.xg()
    for i, team in enumerate(match.teams):
        s = shots[shots.team == team]
        t = [0.0] + [match.clock(r.period, r.minute, r.second) for r in s.itertuples()]
        cum = [0.0] + s.xg.cumsum().tolist()
        end = max(match.clock(r.period, r.minute, r.second) for r in shots.itertuples()) + 2
        ax.step(t + [end], cum + [cum[-1]], where="post", color=TEAM_COLOURS[i], lw=2.2,
                label=f"{team}  {score[team]} goals · {xg[team]:.2f} xG")
        goal_pos = [k for k, g in enumerate(s.goal) if g]  # positions within this team's shots
        ax.scatter([t[k + 1] for k in goal_pos], [cum[k + 1] for k in goal_pos],
                   marker="*", s=260, color=TEAM_COLOURS[i], edgecolors="black", zorder=5)
    ax.axvline(45, color="#bbbbbb", ls="--", lw=1)
    ax.set_xlabel("match minute")
    ax.set_ylabel("cumulative expected goals")
    ax.set_xlim(0, None)
    ax.set_ylim(0, None)
    ax.grid(alpha=0.3)
    ax.spines[["top", "right"]].set_visible(False)
    ax.legend(loc="upper left", frameon=False)
    ax.set_title("xG race · ★ = goal", loc="left", fontsize=11)
    fig.tight_layout()
    return fig


# ------------------------------------------------------------------------------------------ 5
def xg_shot_map(match: Match) -> Figure:
    shots = match.shots()
    pitch, fig, ax = _pitch()
    score, xg = match.score(), match.xg()
    for i, team in enumerate(match.teams):
        s = shots[shots.team == team]
        x, y = s.x.to_numpy(), s.y.to_numpy()
        if i == 1:
            x, y = _flip(x, y)
        for goal in (False, True):
            m = s.goal.to_numpy() == goal
            pitch.scatter(x[m], y[m], s=s.xg.to_numpy()[m] * 1800 + 30, ax=ax,
                          color=TEAM_COLOURS[i], alpha=0.55 if not goal else 0.95,
                          marker="o" if not goal else "*", edgecolors="black", linewidth=0.6,
                          zorder=3 + goal, label=None)
        for xi, yi, v, goal in zip(x, y, s.xg, s.goal, strict=True):
            if v >= 0.25 or goal:  # label only the big chances and the goals
                ax.annotate(f"{v:.2f}", (xi, yi), ha="left", va="center", fontsize=7.5,
                            xytext=(9, 0), textcoords="offset points", zorder=6,
                            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none",
                                      alpha=0.8))
    left = f"← {match.teams[0]}  {score[match.teams[0]]} ({xg[match.teams[0]]:.2f} xG)"
    right = f"{match.teams[1]}  {score[match.teams[1]]} ({xg[match.teams[1]]:.2f} xG) →"
    ax.set_title(f"{left}      {right}\nmarker area ∝ xG · ★ = goal · each team shoots towards "
                 f"the far goal", loc="left", fontsize=11)
    return fig


# ------------------------------------------------------------------------------------------ 6
def key_actions_heatmap(match: Match, team: str, sequences: list[ShotSequence],
                        last_n: int = 2) -> Figure:
    """Where the shot, the assist and the pass before it happened, for one team."""
    xs, ys = [], []
    for seq in sequences:
        if seq.team != team:
            continue
        xs.append(seq.x)
        ys.append(seq.y)
        for a in seq.build_up[-last_n:]:
            xs.append(a.x)
            ys.append(a.y)
    pitch, fig, ax = _pitch()
    if len(xs) >= 3:
        pitch.kdeplot(xs, ys, ax=ax, fill=True, levels=40, thresh=0.03, cmap="Reds", alpha=0.85)
    pitch.scatter(xs, ys, ax=ax, s=18, color="#222222", alpha=0.7, zorder=3)
    n_seq = sum(s.team == team for s in sequences)
    ax.set_title(f"{team} · shots and the {last_n} actions before them · {n_seq} sequences, "
                 f"{len(xs)} events · attacking →", loc="left", fontsize=11)
    return fig
