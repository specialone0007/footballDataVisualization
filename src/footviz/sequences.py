"""Shot sequences: the chain of on-ball actions by the shooting team that led to a shot.

Walk backwards from the shot while the possession stays with the shooting team and no earlier
shot by the same team is crossed (a rebound starts a new sequence), keeping the team's Pass,
Carry and Dribble events. The first non-shooter in that chain (closest to the shot) is the
assister; everyone earlier is build-up.
"""

from __future__ import annotations

from dataclasses import dataclass

from footviz.match import Match

ON_BALL = ("Pass", "Carry", "Dribble")


@dataclass(frozen=True)
class Action:
    id: str
    type: str
    player: str
    x: float
    y: float


@dataclass(frozen=True)
class ShotSequence:
    index: int  # position in Match.shots()
    team: str
    shooter: str
    minute: int
    second: int
    period: int
    xg: float
    outcome: str
    x: float
    y: float
    end_x: float | None
    end_y: float | None
    build_up: tuple[Action, ...]  # chronological, excluding the shot

    @property
    def label(self) -> str:
        clock = f"{self.minute:02d}:{self.second:02d}"
        return f"{clock} {self.shooter} · {self.outcome} · xG {self.xg:.2f}"

    @property
    def assister(self) -> str | None:
        for a in reversed(self.build_up):
            if a.player != self.shooter:
                return a.player
        return None

    def role_of(self, player: str) -> str | None:
        """'Shot', 'Assist', 'Build-up' or None."""
        if player == self.shooter:
            return "Shot"
        if player == self.assister:
            return "Assist"
        if any(a.player == player for a in self.build_up):
            return "Build-up"
        return None


def shot_sequences(match: Match) -> list[ShotSequence]:
    events = match.events
    by_index = {e["index"]: e for e in events}
    out: list[ShotSequence] = []
    shots = match.shots()
    for i, s in shots.iterrows():
        team = s.team
        chain: list[Action] = []
        idx = int(s["index"]) - 1
        while idx in by_index:
            e = by_index[idx]
            if e["possession_team"]["name"] != team:
                break
            if e["type"]["name"] == "Shot" and e["team"]["name"] == team:
                break  # a rebound: this shot's build-up starts after the previous one
            if e["team"]["name"] == team and e["type"]["name"] in ON_BALL and "location" in e:
                chain.append(Action(e["id"], e["type"]["name"], e["player"]["name"],
                                    float(e["location"][0]), float(e["location"][1])))
            idx -= 1
        out.append(ShotSequence(
            index=int(i), team=team, shooter=s.player, minute=int(s.minute), second=int(s.second),
            period=int(s.period), xg=float(s.xg), outcome=s.outcome, x=float(s.x), y=float(s.y),
            end_x=s.end_x, end_y=s.end_y, build_up=tuple(reversed(chain)),
        ))
    return out


def involvement(sequences: list[ShotSequence], player: str) -> list[tuple[ShotSequence, str]]:
    """Every sequence a player took part in, with their role."""
    out = []
    for seq in sequences:
        role = seq.role_of(player)
        if role is not None:
            out.append((seq, role))
    return out
