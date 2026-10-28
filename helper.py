#!/usr/bin/env python3
"""
helper.py -- Offline CLI study helper tool for Full Stack Java Programming (FSJP).

Usage:
  python helper.py fsjp <exp_num> [file|all]
  python helper.py <exp_num> [file|all]
  python helper.py list
  python helper.py show  [subject] <topic_num> [file|all]
  python helper.py write [subject] <topic_num> [filename|folder]
  python helper.py copy  [subject] <topic_num> [file|all]

For FSJP experiments (Q1 to Q16), you can specify '1', 'exp1', or 'exp 1'.
"""

import sys
import os
import re
import json
import subprocess

# -----------------------------------------------------------------------------
#  DATA -- Loaded dynamically from data.json
# -----------------------------------------------------------------------------

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

def _load_subjects():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[warn] Could not load data.json: {e}")
    return {"fsjp": {}}

SUBJECTS = _load_subjects()
EXPERIMENT_SUBJECTS = ("fsjp",)
DEFAULT_SUBJECT = "fsjp"

DIVIDER = "=" * 60


def _valid_subjects():
    return sorted(SUBJECTS.keys()) if SUBJECTS else ["fsjp"]


def _valid_topics(subject=DEFAULT_SUBJECT):
    s = _resolve_subject(subject)
    if not s or s not in SUBJECTS:
        return []
    keys = [k for k in SUBJECTS[s].keys() if k.isdigit()]
    return sorted(keys, key=int)


def _resolve_subject(raw):
    """Return the canonical subject key or None."""
    if not raw:
        return DEFAULT_SUBJECT
    raw_str = str(raw).strip().lower()
    for s in SUBJECTS:
        if s.lower() == raw_str:
            return s
    if raw_str in ("fsjp", "java", "fullstack", "fullstackjava", "subject3", "sub3", "s3"):
        return "fsjp"
    return None


def _resolve_topic(subject, raw):
    """Return the canonical topic key or None."""
    s = _resolve_subject(subject) or DEFAULT_SUBJECT
    if not s or s not in SUBJECTS:
        return None
    topics = SUBJECTS[s]
    raw_str = str(raw).strip().lower()

    if raw_str in topics:
        return raw_str

    cleaned = re.sub(r"^(exp|experiment|topic|q)[\s_\-]*", "", raw_str)
    if cleaned in topics:
        return cleaned

    cleaned_num = cleaned.lstrip("0") or "0"
    if cleaned_num in topics:
        return cleaned_num

    return None


def _normalize_args(args):
    """
    Handle split arguments such as:
      ['fsjp', 'exp', '1'] -> ['fsjp', 'exp1']
      ['exp', '1'] -> ['fsjp', 'exp1']
    """
    if len(args) >= 3 and args[1].lower() in ("exp", "experiment", "topic", "q"):
        return [args[0], f"exp{args[2]}"] + args[3:]
    if len(args) >= 2 and args[0].lower() in ("exp", "experiment", "topic", "q"):
        return [f"exp{args[1]}"] + args[2:]
    return args


def _get_topic(subject, topic_num):
    """Validated lookup; prints error and exits on bad input."""
    s = _resolve_subject(subject) or DEFAULT_SUBJECT
    if s not in SUBJECTS:
        print(f"[error] Unknown subject: '{subject}'")
        print(f"        Valid subjects: {', '.join(_valid_subjects())}")
        sys.exit(1)
    t = _resolve_topic(s, topic_num)
    if t is None:
        label = "experiment" if s in EXPERIMENT_SUBJECTS else "topic"
        print(f"[error] Unknown {label} identifier: '{topic_num}' for subject '{s}'")
        valid_items = [f"exp{k}" for k in _valid_topics(s)]
        print(f"        Valid {label}s: {', '.join(valid_items)} (or 1..{len(valid_items)})")
        sys.exit(1)
    return SUBJECTS[s][t]


def _copy_to_clipboard(text):
    """Try multiple clipboard strategies; degrade gracefully."""
    platform = sys.platform
    try:
        if platform == "win32":
            proc = subprocess.Popen(["clip"], stdin=subprocess.PIPE, shell=True)
            proc.communicate(input=text.encode("utf-16"))
            if proc.returncode == 0:
                return True
        elif platform == "darwin":
            proc = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            proc.communicate(input=text.encode("utf-8"))
            if proc.returncode == 0:
                return True
        else:
            for cmd in (["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]):
                try:
                    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                    proc.communicate(input=text.encode("utf-8"))
                    if proc.returncode == 0:
                        return True
                except FileNotFoundError:
                    continue
    except Exception:
        pass

    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()
        root.after(300, root.destroy)
        root.mainloop()
        return True
    except Exception:
        pass

    return False


_LANGUAGE_LABELS = {
    "java": "JAVA",
    "html": "HTML",
    "css": "CSS",
    "js": "JAVASCRIPT",
    "javascript": "JAVASCRIPT",
    "jsp": "JSP",
    "sql": "SQL",
    "xml": "XML",
}


def _language_label(language):
    text = str(language or "").strip()
    return _LANGUAGE_LABELS.get(text.lower(), text.upper() or "TEXT")


def _topic_files(topic):
    """Return a topic's files as [{name, language, code}, ...]."""
    files = topic.get("files")
    if isinstance(files, list) and files:
        return files
    return [{
        "name": topic.get("filename", ""),
        "language": topic.get("language", "java"),
        "code": topic.get("code", ""),
    }]


def _line_count(code):
    return len(code.strip("\n").splitlines())


def _resolve_file(files, raw):
    """Resolve a 1-based number or file name. Returns index, -1 for all, or None."""
    if raw is None:
        return None
    text = str(raw).strip()
    if text.lower() == "all":
        return -1
    if text.isdigit():
        number = int(text)
        if 1 <= number <= len(files):
            return number - 1
        return None
    lower = text.lower()
    for index, item in enumerate(files):
        name = str(item.get("name", ""))
        if name.lower() == lower or os.path.basename(name).lower() == lower:
            return index
    return None


def _print_file_index(subject, topic_key, topic, files):
    display_id = f"Exp {int(topic_key):02d}" if (topic_key and str(topic_key).isdigit()) else topic_key
    print(f"[{display_id}] {topic.get('title', '')}")
    print(f"{len(files)} files:\n")
    for index, item in enumerate(files, 1):
        name = item.get("name") or f"file{index}"
        language = _language_label(item.get("language", ""))
        lines = _line_count(item.get("code", ""))
        print(f"  {index}. {name:<32} {language:<12} {lines:>3} lines")


def _print_files(files):
    for index, item in enumerate(files, 1):
        if index > 1:
            print()
        print(f"===== {index}. {item.get('name') or f'file{index}'} =====")
        print(item.get("code", "").strip("\n"))


# -----------------------------------------------------------------------------
#  COMMANDS
# -----------------------------------------------------------------------------

def cmd_list(args):
    """
    list           -> list all experiments in fsjp
    list <subject> -> list experiments in that subject
    """
    subject = args[0] if len(args) > 0 else DEFAULT_SUBJECT
    s = _resolve_subject(subject)
    if s is None or s not in SUBJECTS:
        print(f"[error] Unknown subject: '{subject}'")
        print(f"        Valid subjects: {', '.join(_valid_subjects())}")
        sys.exit(1)

    topics = SUBJECTS[s]
    label = "Experiments"

    print(DIVIDER)
    print(f"  {label} in '{s}' (Full Stack Java Programming)")
    print(DIVIDER)
    for num in _valid_topics(s):
        title = topics[num].get("title", "")
        prefix = f"Exp {int(num):02d}"
        files = _topic_files(topics[num])
        suffix = f" ({len(files)} files)" if len(files) > 1 else ""
        print(f"  [{prefix}]  {title}{suffix}")
    print(DIVIDER)


def cmd_show(args):
    """show [subject] <topic_num> [file|all] -- Outputs code."""
    args = _normalize_args(args)
    if not args:
        print("[error] Usage: python helper.py [show] <exp_num> [file|all]")
        print("               python helper.py [show] fsjp <exp_num> [file|all]")
        sys.exit(1)

    if len(args) == 1:
        raw_subject = DEFAULT_SUBJECT
        raw_topic = args[0]
        file_arg = None
    elif _resolve_subject(args[0]):
        raw_subject = args[0]
        raw_topic = args[1]
        file_arg = args[2] if len(args) >= 3 else None
    else:
        raw_subject = DEFAULT_SUBJECT
        raw_topic = args[0]
        file_arg = args[1] if len(args) >= 2 else None

    s = _resolve_subject(raw_subject) or DEFAULT_SUBJECT
    t = _resolve_topic(s, raw_topic)
    topic = _get_topic(s, raw_topic)

    files = _topic_files(topic)

    if len(files) > 1:
        selector = file_arg
        if selector is None:
            if sys.stdin.isatty():
                _print_file_index(s, t, topic, files)
                print()
                try:
                    raw_file = input(f"Select file (1-{len(files)}, all) [1]: ").strip()
                    selector = raw_file or "1"
                except (EOFError, KeyboardInterrupt):
                    print()
                    return
            else:
                _print_file_index(s, t, topic, files)
                print(f"\nPass '1'..'{len(files)}' or 'all' to print contents.")
                return

        chosen = _resolve_file(files, selector)
        if chosen is None:
            print(f"[error] Unknown file '{selector}' for {s} experiment {int(t):02d}.")
            _print_file_index(s, t, topic, files)
            sys.exit(1)

        if chosen == -1:
            _print_files(files)
        else:
            print(files[chosen].get("code", "").strip("\n"))
        return

    code = files[0].get("code", "").strip()
    if code:
        print(code)
    else:
        print("// (no code yet)")


def cmd_write(args):
    """write [subject] <topic_num> [filename|folder]"""
    args = _normalize_args(args)
    if not args:
        print("[error] Usage: python helper.py write [subject] <exp_num> [filename|folder]")
        sys.exit(1)

    if len(args) == 1:
        raw_subject = DEFAULT_SUBJECT
        raw_topic = args[0]
        dest_arg = None
    elif _resolve_subject(args[0]):
        raw_subject = args[0]
        raw_topic = args[1]
        dest_arg = args[2] if len(args) >= 3 else None
    else:
        raw_subject = DEFAULT_SUBJECT
        raw_topic = args[0]
        dest_arg = args[1] if len(args) >= 2 else None

    s = _resolve_subject(raw_subject) or DEFAULT_SUBJECT
    t = _resolve_topic(s, raw_topic)
    topic = _get_topic(s, raw_topic)
    files = _topic_files(topic)

    if len(files) > 1:
        folder = dest_arg or f"{s}_exp_{t}"
        written = []
        try:
            for item in files:
                name = str(item.get("name") or "file.txt").replace("\\", "/")
                parts = [part for part in name.split("/") if part]
                if not parts or name.startswith("/") or ":" in parts[0] or ".." in parts:
                    raise ValueError(f"unsafe file name: {name}")
                target = os.path.join(folder, *parts)
                parent = os.path.dirname(target)
                if parent:
                    os.makedirs(parent, exist_ok=True)
                with open(target, "w", encoding="utf-8") as fh:
                    fh.write(item.get("code", "").strip("\n") + "\n")
                written.append(target)
        except (OSError, ValueError) as exc:
            print(f"[error] Could not write files: {exc}")
            sys.exit(1)
        print(f"[ok] Wrote {len(written)} files to '{folder}'")
        for path in written:
            print(f"     {path}")
        return

    filename = dest_arg or files[0].get("name") or f"{s}_exp_{t}.java"
    code = files[0].get("code", "")

    try:
        parent = os.path.dirname(filename)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(filename, "w", encoding="utf-8") as fh:
            fh.write(code.strip() + "\n")
        print(f"[ok] Code written to '{filename}'")
    except OSError as exc:
        print(f"[error] Could not write file: {exc}")
        sys.exit(1)


def cmd_copy(args):
    """copy [subject] <topic_num> [file|all]"""
    args = _normalize_args(args)
    if not args:
        print("[error] Usage: python helper.py copy [subject] <exp_num> [file|all]")
        sys.exit(1)

    if len(args) == 1:
        raw_subject = DEFAULT_SUBJECT
        raw_topic = args[0]
        file_arg = None
    elif _resolve_subject(args[0]):
        raw_subject = args[0]
        raw_topic = args[1]
        file_arg = args[2] if len(args) >= 3 else None
    else:
        raw_subject = DEFAULT_SUBJECT
        raw_topic = args[0]
        file_arg = args[1] if len(args) >= 2 else None

    s = _resolve_subject(raw_subject) or DEFAULT_SUBJECT
    t = _resolve_topic(s, raw_topic)
    topic = _get_topic(s, raw_topic)
    files = _topic_files(topic)

    if len(files) > 1:
        selector = file_arg
        if selector is None:
            if sys.stdin.isatty():
                _print_file_index(s, t, topic, files)
                print()
                try:
                    raw_file = input(f"Select file to copy (1-{len(files)}, all) [1]: ").strip()
                    selector = raw_file or "1"
                except (EOFError, KeyboardInterrupt):
                    print()
                    return
            else:
                selector = "1"

        chosen = _resolve_file(files, selector)
        if chosen is None:
            print(f"[error] Unknown file '{selector}' for {s} experiment {int(t):02d}.")
            sys.exit(1)

        if chosen == -1:
            text = "\n\n".join(
                f"===== {index}. {item.get('name') or f'file{index}'} =====\n"
                f"{item.get('code', '').strip(chr(10))}"
                for index, item in enumerate(files, 1)
            )
            label = f"{len(files)} files"
        else:
            text = files[chosen].get("code", "").strip("\n")
            label = files[chosen].get("name") or f"file {chosen + 1}"

        if not text.strip():
            print("[warn] The selected file is empty - nothing to copy.")
            return

        success = _copy_to_clipboard(text + "\n")
        if success:
            print(f"[ok] {label} from '{s}' experiment {int(t):02d} copied to clipboard.")
        else:
            print("[warn] Could not access clipboard.")
            print("       Here is the code snippet:\n")
            print(text)
        return

    code = files[0].get("code", "")
    if not code.strip():
        print(f"[warn] The code block for experiment {int(t):02d} is empty - nothing to copy.")
        return

    success = _copy_to_clipboard(code.strip() + "\n")
    display_id = f"Exp {int(t):02d}"

    if success:
        print(f"[ok] Code for '{s}' {display_id} copied to clipboard.")
    else:
        print("[warn] Could not access clipboard.")
        print("       Here is the code snippet:\n")
        print(code)


# -----------------------------------------------------------------------------
#  ENTRY POINT
# -----------------------------------------------------------------------------

USAGE = """\
helper.py -- Offline CLI study helper tool for Full Stack Java Programming (FSJP).

Usage:
  python helper.py fsjp <exp_num> [file|all]
  python helper.py <exp_num> [file|all]
  python helper.py list
  python helper.py show  [subject] <topic_or_exp> [file|all]
  python helper.py write [subject] <topic_or_exp> [filename|folder]
  python helper.py copy  [subject] <topic_or_exp> [file|all]

For FSJP experiments (Q1 to Q16), specify '1', 'exp1', 'exp 1', or 'q1'.
For multi-file experiments (Exp 8, Exp 11), pass a file number or 'all'.
"""

COMMANDS = {
    "list":  cmd_list,
    "show":  cmd_show,
    "write": cmd_write,
    "copy":  cmd_copy,
}


def main():
    argv = sys.argv[1:]

    if not argv or argv[0] in ("-h", "--help"):
        print(USAGE)
        sys.exit(0)

    cmd = argv[0].lower()
    rest = argv[1:]

    if cmd in ("show", "code", "get"):
        cmd_show(rest)
    elif cmd in COMMANDS:
        COMMANDS[cmd](rest)
    elif _resolve_subject(cmd):
        # Direct: python helper.py fsjp 6
        cmd_show([cmd] + rest)
    elif _resolve_topic(DEFAULT_SUBJECT, cmd):
        # Direct number shortcut: python helper.py 6
        cmd_show([DEFAULT_SUBJECT, cmd] + rest)
    else:
        print(f"[error] Unknown command or experiment: '{cmd}'")
        print(f"        Valid commands: {', '.join(COMMANDS)}")
        print()
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
