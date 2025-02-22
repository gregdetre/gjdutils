import pytest
from pathlib import Path
from gjdutils.cli.check_git_clean import check_git_clean
from gjdutils.shell import fatal_error_msg
from gjdutils.cmd import run_cmd


@pytest.fixture
def temp_git_repo(tmp_path):
    """Create a temporary git repo for testing."""
    # Initialize git repo
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir(parents=True, exist_ok=True)
    run_cmd("git init", cwd=str(repo_path))
    run_cmd("git config user.email 'test@example.com'", cwd=str(repo_path))
    run_cmd("git config user.name 'Test User'", cwd=str(repo_path))

    # Create and commit an initial file
    initial_file = repo_path / "initial.txt"
    initial_file.write_text("initial content")
    run_cmd("git add initial.txt", cwd=str(repo_path))
    run_cmd("git commit -m 'Initial commit'", cwd=str(repo_path))

    return repo_path


def test_clean_repo(temp_git_repo, monkeypatch):
    """Test check_git_clean with a clean repository."""
    monkeypatch.chdir(temp_git_repo)
    check_git_clean()  # Should not raise any errors


def test_unstaged_changes(temp_git_repo, monkeypatch, capsys):
    """Test check_git_clean detects unstaged changes."""
    monkeypatch.chdir(temp_git_repo)

    # Create an unstaged change
    (temp_git_repo / "initial.txt").write_text("modified content")

    with pytest.raises(SystemExit):
        check_git_clean()

    captured = capsys.readouterr()
    assert "Unstaged changes present" in captured.out


def test_staged_changes(temp_git_repo, monkeypatch, capsys):
    """Test check_git_clean detects staged but uncommitted changes."""
    monkeypatch.chdir(temp_git_repo)

    # Create and stage a new file
    new_file = temp_git_repo / "new.txt"
    new_file.write_text("new content")
    run_cmd("git add new.txt", cwd=str(temp_git_repo))

    with pytest.raises(SystemExit):
        check_git_clean()

    captured = capsys.readouterr()
    assert "Uncommitted staged changes present" in captured.out


def test_untracked_files(temp_git_repo, monkeypatch, capsys):
    """Test check_git_clean detects untracked files."""
    monkeypatch.chdir(temp_git_repo)

    # Create an untracked file
    untracked_file = temp_git_repo / "untracked.txt"
    untracked_file.write_text("untracked content")

    with pytest.raises(SystemExit):
        check_git_clean()

    captured = capsys.readouterr()
    assert "Untracked files present" in captured.out
