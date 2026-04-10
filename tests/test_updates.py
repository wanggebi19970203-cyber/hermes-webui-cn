"""
Targeted regression tests for self-update logic.
"""

from api import updates


def test_run_git_includes_stderr_on_failure(monkeypatch, tmp_path):
    class _Result:
        stdout = ""
        stderr = "fatal: not possible to fast-forward"
        returncode = 1

    def fake_run(*args, **kwargs):
        return _Result()

    monkeypatch.setattr(updates.subprocess, "run", fake_run)

    out, ok = updates._run_git(["pull", "--ff-only"], tmp_path)

    assert ok is False
    assert out == "fatal: not possible to fast-forward"


def test_apply_update_uses_plain_pull_when_upstream_exists(monkeypatch, tmp_path):
    repo = tmp_path / "agent-repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    monkeypatch.setattr(updates, "_AGENT_DIR", repo)

    calls = []

    def fake_run_git(args, cwd, timeout=10):
        calls.append(tuple(args))
        if args == ["rev-parse", "--abbrev-ref", "@{upstream}"]:
            return "origin/master", True
        if args == ["status", "--porcelain"]:
            return "", True
        if args == ["pull", "--ff-only"]:
            return "Already up to date.", True
        raise AssertionError(f"Unexpected git call: {args}")

    monkeypatch.setattr(updates, "_run_git", fake_run_git)

    result = updates._apply_update_inner("agent")

    assert result["ok"] is True
    assert ("pull", "--ff-only") in calls
    assert ("pull", "--ff-only", "origin/master") not in calls


def test_apply_update_falls_back_to_origin_default_branch(monkeypatch, tmp_path):
    repo = tmp_path / "webui-repo"
    repo.mkdir()
    (repo / ".git").mkdir()
    monkeypatch.setattr(updates, "REPO_ROOT", repo)

    calls = []

    def fake_run_git(args, cwd, timeout=10):
        calls.append(tuple(args))
        if args == ["rev-parse", "--abbrev-ref", "@{upstream}"]:
            return "", False
        if args == ["symbolic-ref", "refs/remotes/origin/HEAD"]:
            return "refs/remotes/origin/main", True
        if args == ["status", "--porcelain"]:
            return "", True
        if args == ["pull", "--ff-only", "origin", "main"]:
            return "Updating abc..def", True
        raise AssertionError(f"Unexpected git call: {args}")

    monkeypatch.setattr(updates, "_run_git", fake_run_git)

    result = updates._apply_update_inner("webui")

    assert result["ok"] is True
    assert ("pull", "--ff-only", "origin", "main") in calls


def test_check_repo_fetches_the_upstream_remote(monkeypatch, tmp_path):
    repo = tmp_path / "forked-repo"
    repo.mkdir()
    (repo / ".git").mkdir()

    calls = []

    def fake_run_git(args, cwd, timeout=10):
        calls.append(tuple(args))
        if args == ["rev-parse", "--abbrev-ref", "@{upstream}"]:
            return "fork/main", True
        if args == ["fetch", "fork", "--quiet"]:
            return "", True
        if args == ["rev-list", "--count", "HEAD..fork/main"]:
            return "2", True
        if args == ["rev-parse", "--short", "HEAD"]:
            return "aaa0001", True
        if args == ["rev-parse", "--short", "fork/main"]:
            return "bbb0002", True
        raise AssertionError(f"Unexpected git call: {args}")

    monkeypatch.setattr(updates, "_run_git", fake_run_git)

    result = updates._check_repo(repo, "agent")

    assert result == {
        "name": "agent",
        "behind": 2,
        "current_sha": "aaa0001",
        "latest_sha": "bbb0002",
        "branch": "fork/main",
    }
    assert ("fetch", "fork", "--quiet") in calls
