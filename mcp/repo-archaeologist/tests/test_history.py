import subprocess
from pathlib import Path

import pytest
from analyzers import history


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


@pytest.fixture
def tiny_repo(tmp_path: Path) -> Path:
    """A throwaway git repo with two commits to one file — fully deterministic."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "tester@example.com")
    _git(repo, "config", "user.name", "Tester")

    f = repo / "a.py"
    f.write_text("x = 1\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "first commit")

    f.write_text("x = 1\ny = 2\n")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "second commit")
    return repo


def test_blame_story_counts_commits_and_authors(tiny_repo: Path):
    story = history.git_blame_story(tiny_repo, "a.py")
    assert story["commit_count"] == 2
    assert story["authors"][0]["name"] == "Tester"
    assert story["authors"][0]["commits"] == 2
    assert story["last_commit"]["date"] == story["first_commit"]["date"]  # same day


def test_explain_commit_range(tiny_repo: Path):
    result = history.explain_commit_range(tiny_repo, "HEAD~1", "HEAD")
    assert result["commit_count"] == 1
    assert result["commits"][0]["subject"] == "second commit"
    assert "a.py" in result["files_changed"]


def test_git_error_on_bad_ref(tiny_repo: Path):
    with pytest.raises(history.GitError):
        history.explain_commit_range(tiny_repo, "nonexistent", "HEAD")
