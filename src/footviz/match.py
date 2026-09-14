"""Load a StatsBomb events file and expose the handful of views the plots need.

StatsBomb coordinates: x in [0, 120] left→right, y in [0, 80] top→bottom, always given from
the perspective of the team performing the action (each team attacks left→right). `Match`
keeps that convention; plots that show both teams on one pitch flip the second team.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from urllib.request import urlopen

import pandas as pd

OPEN_DATA = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{}.json"
PITCH_LENGTH, PITCH_WIDTH = 120.0, 80.0


def load_events(path: str | Path) -> list[dict]:
    with Path(path).open(encoding="utf-8") as f:
        events = json.load(f)
    if not isinstance(events, list) or not events or "type" not in events[0]:
        raise ValueError(f"{path} does not look like a StatsBomb events file")
    return events


def fetch_events(match_id: int, cache_dir: str | Path | None = None) -> list[dict]:
    """Download one match from the StatsBomb open-data repository (optionally cached)."""
    if cache_dir is not None:
        cached = Path(cache_dir) / f"{match_id}.json"
        if cached.exists():
            return load_events(cached)
    raw = urlopen(OPEN_DATA.format(match_id), timeout=120).read()  # noqa: S310
    if cache_dir is not None:
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        (Path(cache_dir) / f"{match_id}.json").write_bytes(raw)
    return json.loads(raw)


@dataclass(frozen=True)
class Player:
    name: str
    jersey: int
    position: str


@dataclass
class Match:
    events: list[dict]
    teams: tuple[str, str] = field(init=False)
    lineups: dict[str, list[Player]] = field(init=False)

    def __post_init__(self) -> None:
        starting = [e for e in self.events if e["type"]["name"] == "Starting XI"]
        if len(starting) != 2:
            raise ValueError("expected exactly two Starting XI events")
        self.teams = (starting[0]["team"]["name"], starting[1]["team"]["name"])
        self.lineups = {
            e["team"]["name"]: [
                Player(p["player"]["name"], p["jersey_number"], p["position"]["name"])
                for p in e["tactics"]["lineup"]
            ]
            for e in starting
        }

    # ---- lookups -----------------------------------------------------------------
    def opponent(self, team: str) -> str:
        self._check_team(team)
        return self.teams[1] if team == self.teams[0] else self.teams[0]

    def jersey(self, team: str, player: str) -> int | None:
        for p in self.lineups[team]:
            if p.name == player:
                return p.jersey
        return None

    def formation(self, team: str) -> int:
        self._check_team(team)
        for e in self.events:
            if e["type"]["name"] == "Starting XI" and e["team"]["name"] == team:
                return int(e["tactics"]["formation"])
        raise KeyError(team)

    def _check_team(self, team: str) -> None:
        if team not in self.teams:
            raise KeyError(f"{team!r} not in this match; teams are {self.teams}")

    # ---- tabular views ---------------------------------------------------------------
    def located(self) -> pd.DataFrame:
        """One row per event that has a player and a location."""
        rows = []
        for e in self.events:
            if "player" not in e or "location" not in e:
                continue
            rows.append({
                "id": e["id"],
                "index": e["index"],
                "period": e["period"],
                "minute": e["minute"],
                "second": e["second"],
                "team": e["team"]["name"],
                "possession_team": e["possession_team"]["name"],
                "player": e["player"]["name"],
                "type": e["type"]["name"],
                "x": float(e["location"][0]),
                "y": float(e["location"][1]),
            })
        return pd.DataFrame(rows)

    def shots(self) -> pd.DataFrame:
        rows = []
        for e in self.events:
            if e["type"]["name"] != "Shot" or "statsbomb_xg" not in e.get("shot", {}):
                continue
            end = e["shot"].get("end_location", [None, None])
            rows.append({
                "id": e["id"],
                "index": e["index"],
                "period": e["period"],
                "minute": e["minute"],
                "second": e["second"],
                "team": e["team"]["name"],
                "player": e["player"]["name"],
                "x": float(e["location"][0]),
                "y": float(e["location"][1]),
                "end_x": float(end[0]) if end[0] is not None else None,
                "end_y": float(end[1]) if end[1] is not None else None,
                "xg": float(e["shot"]["statsbomb_xg"]),
                "outcome": e["shot"]["outcome"]["name"],
                "goal": e["shot"]["outcome"]["name"] == "Goal",
            })
        return pd.DataFrame(rows).sort_values("index", ignore_index=True)

    def score(self) -> dict[str, int]:
        s = self.shots()
        return {t: int(s[(s.team == t) & s.goal].shape[0]) for t in self.teams}

    def xg(self) -> dict[str, float]:
        s = self.shots()
        return {t: float(s.loc[s.team == t, "xg"].sum()) for t in self.teams}

    def average_positions(self, team: str, in_possession: bool) -> pd.DataFrame:
        """Mean event location per starting player, split by whether their team had the ball."""
        self._check_team(team)
        df = self.located()
        df = df[df.team == team]
        df = df[(df.possession_team == team) == in_possession]
        starters = {p.name: p for p in self.lineups[team]}
        df = df[df.player.isin(starters)]
        agg = df.groupby("player")[["x", "y"]].mean().reset_index()
        agg["jersey"] = agg.player.map(lambda n: starters[n].jersey)
        agg["position"] = agg.player.map(lambda n: starters[n].position)
        agg["n"] = df.groupby("player").size().reindex(agg.player).to_numpy()
        return agg.sort_values("jersey", ignore_index=True)

    def player_actions(self, player: str, action: str | None = None) -> pd.DataFrame:
        df = self.located()
        df = df[df.player == player]
        if action is not None:
            df = df[df.type == action]
        return df.reset_index(drop=True)

    def action_types(self, player: str) -> list[str]:
        df = self.located()
        return sorted(df.loc[df.player == player, "type"].unique().tolist())

    def clock(self, period: int, minute: int, second: int) -> float:
        """Match minute on a continuous 0..90+ axis (period 2 starts at 45 even if
        first-half stoppage time ran long)."""
        m = minute + second / 60
        if period == 2:
            m = max(m, 45.0)
        return m
