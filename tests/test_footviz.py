from pathlib import Path

import matplotlib.figure
import pytest

from footviz import Match, load_events, plots, shot_sequences
from footviz.sequences import involvement

DATA = Path(__file__).resolve().parents[1] / "data" / "mancity-chelsea-fawsl-2018-19.json"


@pytest.fixture(scope="module")
def match() -> Match:
    return Match(load_events(DATA))


@pytest.fixture(scope="module")
def seqs(match):
    return shot_sequences(match)


def test_teams_and_lineups(match):
    assert match.teams == ("Manchester City WFC", "Chelsea LFC")
    for t in match.teams:
        assert len(match.lineups[t]) == 11
        assert len({p.jersey for p in match.lineups[t]}) == 11
    assert match.opponent("Chelsea LFC") == "Manchester City WFC"
    with pytest.raises(KeyError):
        match.opponent("Arsenal")


def test_score_and_xg(match):
    assert match.score() == {"Manchester City WFC": 2, "Chelsea LFC": 2}
    xg = match.xg()
    assert all(0 < v < 5 for v in xg.values())
    # 34 Shot events in the file; one has no statsbomb_xg and is dropped
    assert len(match.shots()) == 33


def test_located_frame(match):
    df = match.located()
    assert df.x.between(0, 120).all() and df.y.between(0, 80).all()
    assert set(df.team.unique()) == set(match.teams)
    assert "Shot" in df.type.unique()


def test_average_positions(match):
    for t in match.teams:
        for phase in (True, False):
            ap = match.average_positions(t, phase)
            assert len(ap) == 11, (t, phase)
            assert ap.n.min() > 0
    # goalkeeper should be the deepest player in possession
    ap = match.average_positions("Manchester City WFC", True)
    assert ap.loc[ap.position == "Goalkeeper", "x"].iloc[0] == ap.x.min()


def test_shot_sequences(match, seqs):
    assert len(seqs) == len(match.shots())
    for s in seqs:
        assert s.team in match.teams
        assert 0 <= s.xg <= 1
        assert all(a.player for a in s.build_up)
        # build-up is chronological: no action after the shot
        assert s.role_of(s.shooter) == "Shot"
        if s.assister:
            assert s.role_of(s.assister) == "Assist"
    assert any(s.build_up for s in seqs), "at least one shot should have a build-up"


def test_involvement_roles(match, seqs):
    scorer = next(s.shooter for s in seqs if s.outcome == "Goal")
    inv = involvement(seqs, scorer)
    assert any(role == "Shot" for _, role in inv)
    assert all(role in {"Shot", "Assist", "Build-up"} for _, role in inv)


def test_clock():
    m = Match.__new__(Match)  # clock does not touch state
    assert Match.clock(m, 1, 10, 30) == 10.5
    assert Match.clock(m, 2, 45, 0) == 45.0
    assert Match.clock(m, 2, 44, 0) == 45.0  # never before the second-half origin
    assert Match.clock(m, 2, 70, 15) == 70.25


@pytest.mark.parametrize("maker", [
    lambda m, s: plots.xg_timeline(m),
    lambda m, s: plots.xg_shot_map(m),
    lambda m, s: plots.average_positions(m, m.teams[0], True),
    lambda m, s: plots.average_positions(m, m.teams[1], False),
    lambda m, s: plots.key_actions_heatmap(m, m.teams[0], s),
    lambda m, s: plots.shot_sequence(m, next(x for x in s if x.build_up)),
    lambda m, s: plots.action_heatmap(m, m.lineups[m.teams[0]][5].name, "Pass"),
])
def test_every_plot_returns_a_figure(match, seqs, maker):
    fig = maker(match, seqs)
    assert isinstance(fig, matplotlib.figure.Figure)
    assert fig.axes
    matplotlib.pyplot.close(fig)


def test_bad_events_file(tmp_path):
    p = tmp_path / "x.json"
    p.write_text("{}")
    with pytest.raises(ValueError):
        load_events(p)
