#!/usr/bin/env python
"""
bbc_cli_cheatsheet_builder.py

Generate a PHP cheatsheet for DBUG IDLE CLI rituals.
"""

from pathlib import Path
import textwrap

RITUALS = [
    {
        "name": "bugworld enter",
        "category": "environment",
        "description": "Enter BUGWORLD and land in DBUG IDLE (BUG SWITCH = OFF).",
        "example": "tiangan bugworld enter"
    },
    {
        "name": "bugworld exit",
        "category": "environment",
        "description": "Exit BUGWORLD. Requires closed session and no active roles.",
        "example": "tiangan bugworld exit"
    },
    {
        "name": "session open",
        "category": "session",
        "description": "Open a new DBUG IDLE session and start logging.",
        "example": "tiangan session open"
    },
    {
        "name": "session close",
        "category": "session",
        "description": "Close the current session and finalize the log.",
        "example": "tiangan session close"
    },
    {
        "name": "session status",
        "category": "session",
        "description": "Show current session ID, roles, and BUG SWITCH state.",
        "example": "tiangan session status"
    },
    {
        "name": "role list",
        "category": "role",
        "description": "List available admin roles in DBUG IDLE.",
        "example": "tiangan role list"
    },
    {
        "name": "role assume <role>",
        "category": "role",
        "description": "Assume a named admin role (requires secrets/keys).",
        "example": "tiangan role assume adminp"
    },
    {
        "name": "role release <role>",
        "category": "role",
        "description": "Release a previously assumed role.",
        "example": "tiangan role release adminp"
    },
    {
        "name": "role whoami",
        "category": "role",
        "description": "Show which roles the current actor holds.",
        "example": "tiangan role whoami"
    },
    {
        "name": "biba show",
        "category": "safety",
        "description": "Show the Best Index of Banned Actions (BIBA).",
        "example": "tiangan biba show"
    },
    {
        "name": "babi show <identity>",
        "category": "safety",
        "description": "Show banned actions for a given identity (BABI).",
        "example": "tiangan babi show adminx"
    },
    {
        "name": "babr check <response>",
        "category": "safety",
        "description": "Dry-run a response through BABR to check if it is banned.",
        "example": "tiangan babr check \"proposed response text\""
    },
    {
        "name": "biba update",
        "category": "safety",
        "description": "Update BIBA entries (admin-only).",
        "example": "tiangan biba update"
    },
    {
        "name": "log show",
        "category": "logging",
        "description": "Show the current session log.",
        "example": "tiangan log show"
    },
    {
        "name": "log annotate <text>",
        "category": "logging",
        "description": "Append an annotation to the session log.",
        "example": "tiangan log annotate \"note text\""
    },
]


def build_php_cheatsheet(rituals):
    rows = []
    for r in rituals:
        rows.append(f"""
        <tr>
          <td><code>{r['name']}</code></td>
          <td>{r['category']}</td>
          <td>{r['description']}</td>
          <td><code>{r['example']}</code></td>
        </tr>
        """.strip())

    table_rows = "\n".join(rows)

    php_content = textwrap.dedent(f"""\
    <?php
    // Auto-generated CLI ritual cheatsheet for DBUG IDLE (BUG SWITCH = OFF)
    ?>
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Tiangan CLI Ritual Cheatsheet — DBUG IDLE</title>
      <style>
        body {{ font-family: system-ui, sans-serif; padding: 2rem; background: #0b0b10; color: #f5f5f5; }}
        h1 {{ margin-bottom: 1rem; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid #444; padding: 0.5rem; vertical-align: top; }}
        th {{ background: #111827; }}
        code {{ background: #111827; padding: 0.1rem 0.25rem; border-radius: 3px; }}
      </style>
    </head>
    <body>
      <h1>Tiangan CLI Ritual Cheatsheet — DBUG IDLE (BUG SWITCH = OFF)</h1>
      <p>All rituals below operate within BUGWORLD, governed by the BBC BOOK, with the BUG SWITCH toggled OFF.</p>
      <table>
        <thead>
          <tr>
            <th>Command</th>
            <th>Category</th>
            <th>Description</th>
            <th>Example</th>
          </tr>
        </thead>
        <tbody>
        {table_rows}
        </tbody>
      </table>
    </body>
    </html>
    """)

    return php_content


def main():
    root = Path(__file__).resolve().parent.parent  # assume script lives in a subdir
    target = root / "cli_ritual_cheatsheet.php"
    content = build_php_cheatsheet(RITUALS)
    target.write_text(content, encoding="utf-8")
    print(f"Generated {target}")


if __name__ == "__main__":
    main()
