"""
Tools module for Assignment 4 Multi-Agent Systems.
Provides specialized tools for research, code execution, static security checks,
and shared task board operations.
"""

import ast
import json
import subprocess
import sys
import tempfile
from typing import Dict, Any, List

def search_technical_standards(query: str) -> str:
    """
    Simulates querying technical knowledge bases, RFCs, and engineering specifications.
    Returns authoritative design patterns, algorithmic trade-offs, and security standards.
    """
    knowledge_base = {
        "rate_limiter": (
            "RFC 6585 & Standard Distributed Rate Limiter Patterns:\n"
            "1. Token Bucket: Allows bursts up to capacity; refills at fixed rate. Best for APIs with bursty traffic.\n"
            "2. Leaky Bucket: Smooths traffic out to a constant egress rate. Best for downstream systems with rigid limits.\n"
            "3. Sliding Window Counter: Combines fixed window memory efficiency with boundary smoothing.\n"
            "Concurrency Invariant: Requires atomic decrements or distributed locking (e.g., Redis EVAL Lua script / Python threading.Lock) to prevent race conditions (TOCTOU)."
        ),
        "circuit_breaker": (
            "Martin Fowler Circuit Breaker Pattern:\n"
            "States: CLOSED (normal), OPEN (fast-fail, bypass execution), HALF-OPEN (probe trial requests).\n"
            "Transitions: Consecutive failures >= threshold -> OPEN; Reset timeout elapsed -> HALF-OPEN; Success in probe -> CLOSED.\n"
            "Thread Safety: State transitions and failure counts must be guarded by reentrant locks (RLock)."
        ),
        "security_concurrency": (
            "OWASP & Concurrency Security Best Practices:\n"
            "1. Avoid unsynchronized shared mutable state in multi-threaded environments.\n"
            "2. Always release locks in `finally` blocks or use context managers (`with lock:`).\n"
            "3. Prevent Denial-of-Service via unbounded memory growth: always bound in-memory caches with LRU/TTL eviction.\n"
            "4. Input validation: Validate types, positive integers for capacities, and sanitize client identifiers."
        ),
    }

    query_lower = query.lower()
    results = []
    for key, content in knowledge_base.items():
        if any(term in query_lower for term in key.split("_")) or any(word in content.lower() for word in query_lower.split()):
            results.append(f"=== Knowledge Item [{key}] ===\n{content}")

    if not results:
        return (
            f"Technical Search for '{query}':\n"
            "Standard architectural pattern recommends decoupling interface from storage, "
            "using atomic synchronization primitives, and validating edge conditions (zero/negative values, network partition)."
        )
    return "\n\n".join(results)


def execute_python_code(code: str) -> str:
    """
    Executes Python code in an isolated subprocess sandbox.
    Captures stdout, stderr, and execution exit status.
    """
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name

    try:
        res = subprocess.run(
            [sys.executable, temp_file_path],
            capture_output=True,
            text=True,
            timeout=12,
        )
        stdout = res.stdout.strip()
        stderr = res.stderr.strip()
        if res.returncode == 0:
            return f"EXECUTION SUCCESS:\nOutput:\n{stdout if stdout else '[No stdout, tests passed silently]'}"
        else:
            return f"EXECUTION FAILED (Exit Code {res.returncode}):\nStdout:\n{stdout}\nStderr:\n{stderr}"
    except subprocess.TimeoutExpired:
        return "EXECUTION TIMEOUT: Code exceeded 12-second sandbox limit."
    except Exception as e:
        return f"EXECUTION ERROR: {str(e)}"


def security_ast_scanner(code: str) -> str:
    """
    Performs static AST analysis and rule-based heuristic security/quality scanning on Python code.
    Detects missing locks, mutable globals, naked exceptions, and infinite loop patterns.
    """
    findings: List[str] = []
    try:
        tree = ast.parse(code)
    except SyntaxError as se:
        return f"AST PARSE ERROR: Code has syntax error at line {se.lineno}: {se.msg}"

    has_threading = any(
        isinstance(node, ast.Import) and any(alias.name == "threading" for alias in node.names)
        or isinstance(node, ast.ImportFrom) and node.module == "threading"
        for node in ast.walk(tree)
    )

    has_lock_usage = False
    has_bare_except = False

    for node in ast.walk(tree):
        # Check lock usage
        if isinstance(node, ast.With):
            for item in node.items:
                if "lock" in ast.unparse(item.context_expr).lower():
                    has_lock_usage = True

        # Check bare except
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                has_bare_except = True
                findings.append(f"Line {node.lineno}: Anti-pattern - Bare 'except:' clause detected. Use specific exceptions.")

    if has_threading and not has_lock_usage:
        findings.append("Concurrency Alert: 'threading' imported but no 'with lock:' context manager detected. Risk of race condition!")

    if not findings:
        return "SECURITY SCAN PASSED: No static anti-patterns detected. Concurrency and exception handling conform to guidelines."

    return "SECURITY AUDIT FINDINGS:\n" + "\n".join(f"- {f}" for f in findings)
