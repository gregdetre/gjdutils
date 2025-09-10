"""Port management utilities for network servers.

Utilities for checking port availability, freeing occupied ports,
and managing network server processes.
"""

import os
import shutil
import signal
import subprocess
import time
from typing import List


def looks_like_addr_in_use(e: OSError) -> bool:
    """Detect EADDRINUSE across platforms using errno or message text.
    
    Args:
        e: The OSError exception to check
        
    Returns:
        True if the error indicates "address already in use"
    """
    try:
        err_no = getattr(e, "errno", None)
        if isinstance(err_no, int) and err_no in {48, 98, 10048}:
            return True
    except Exception:
        pass
    msg = str(e).lower()
    return "address already in use" in msg or "errno 48" in msg or "errno 98" in msg


def pids_listening_on_port(port: int) -> List[int]:
    """Return a list of PIDs that appear to be listening on the given TCP port.

    Prefers lsof; falls back to fuser if available.
    
    Args:
        port: The TCP port number to check
        
    Returns:
        List of process IDs listening on the port
    """
    pids: List[int] = []
    try:
        if shutil.which("lsof"):
            # Use LISTEN state to avoid client connections
            proc = subprocess.run(
                ["lsof", "-ti", f"tcp:{port}", "-sTCP:LISTEN"],
                capture_output=True,
                text=True,
                check=False,
            )
            for line in proc.stdout.splitlines():
                try:
                    pid = int(line.strip())
                    if pid not in pids:
                        pids.append(pid)
                except Exception:
                    pass
        if not pids and shutil.which("fuser"):
            # Try Linux-style fuser
            proc = subprocess.run(
                ["fuser", "-n", "tcp", str(port)],
                capture_output=True,
                text=True,
                check=False,
            )
            # Output may be like: "8000/tcp: 1234 5678"
            tokens = (proc.stdout or "").replace("/tcp:", " ").split()
            for tok in tokens:
                try:
                    pid = int(tok)
                    if pid not in pids:
                        pids.append(pid)
                except Exception:
                    pass
    except Exception:
        # Best-effort: ignore detection errors
        pass
    return pids


def kill_pids(pids: List[int], verbose: int = 0) -> None:
    """Kill a list of process IDs, trying SIGTERM first, then SIGKILL.
    
    Args:
        pids: List of process IDs to terminate
        verbose: Verbosity level (0=quiet, 1+=show warnings)
    """
    if not pids:
        return
    for sig in (signal.SIGTERM, signal.SIGKILL):
        for pid in list(pids):
            try:
                os.kill(pid, sig)
            except ProcessLookupError:
                # Already gone
                try:
                    pids.remove(pid)
                except ValueError:
                    pass
            except Exception:
                # Ignore permission or other errors
                pass
        # Brief wait and re-check
        time.sleep(0.2 if sig == signal.SIGTERM else 0.05)
        remaining = []
        for pid in pids:
            try:
                os.kill(pid, 0)
                remaining.append(pid)
            except Exception:
                pass
        pids[:] = remaining
        if not pids:
            break
    if verbose >= 1 and pids:
        print(f"Warning: some processes may still be using the port: {pids}")


def free_port_if_in_use(port: int, verbose: int = 0) -> None:
    """Free a port by killing any processes listening on it.
    
    Args:
        port: The TCP port number to free
        verbose: Verbosity level (0=quiet, 1+=show what's being killed)
    """
    pids = pids_listening_on_port(port)
    if pids:
        if verbose >= 1:
            print(f"Killing processes on port {port}: {pids}")
        kill_pids(pids, verbose)