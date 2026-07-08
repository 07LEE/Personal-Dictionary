"""CLI interface for Personal-Dictionary management."""

import argparse
import os
import sys


def _get_dict_path():
    """Returns the absolute path to custom_dict.txt."""
    return os.path.join(os.path.dirname(__file__), "custom_dict.txt")


def _load_entries(dict_path):
    """Loads all dictionary entries as a list of (word, tag, score) tuples."""
    entries = []
    with open(dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            word = parts[0]
            tag = parts[1] if len(parts) > 1 else 'NNG'
            score = float(parts[2]) if len(parts) > 2 else 1.0
            entries.append((word, tag, score))
    return entries


def _load_header(dict_path):
    """Loads comment lines from the top of the dictionary file."""
    header = []
    with open(dict_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#'):
                header.append(line)
            else:
                break
    return header


def _save_entries(dict_path, entries):
    """Saves dictionary entries to file, preserving header comments."""
    header = _load_header(dict_path)
    with open(dict_path, 'w', encoding='utf-8') as f:
        for line in header:
            f.write(line)
        for word, tag, score in entries:
            f.write(f"{word} {tag} {score}\n")


def cmd_add(args):
    """Adds a word to the dictionary with duplicate detection."""
    dict_path = _get_dict_path()
    entries = _load_entries(dict_path)
    existing = {e[0] for e in entries}

    if args.word in existing:
        print(f"Duplicate: '{args.word}' already exists.")
        return 1

    entries.append((args.word, args.tag, args.score))
    _save_entries(dict_path, entries)
    print(f"Added: {args.word} {args.tag} {args.score}")
    return 0


def cmd_list(args):
    """Lists all dictionary entries."""
    dict_path = _get_dict_path()
    entries = _load_entries(dict_path)

    if args.sort:
        entries.sort(key=lambda e: e[0])

    for word, tag, score in entries:
        print(f"{word:<35} {tag} {score}")
    print(f"\nTotal: {len(entries)} entries")
    return 0


def cmd_search(args):
    """Searches for entries matching the query."""
    dict_path = _get_dict_path()
    entries = _load_entries(dict_path)

    query = args.query.lower()
    matches = [(w, t, s) for w, t, s in entries if query in w.lower()]

    if not matches:
        print(f"No matches for '{args.query}'")
        return 1

    for word, tag, score in matches:
        print(f"{word:<35} {tag} {score}")
    print(f"\nFound: {len(matches)} matches")
    return 0


def cmd_sort(args):
    """Sorts dictionary entries in-place."""
    dict_path = _get_dict_path()
    entries = _load_entries(dict_path)
    entries.sort(key=lambda e: e[0])
    _save_entries(dict_path, entries)
    print(f"Sorted {len(entries)} entries.")
    return 0


def cmd_check(args):
    """Checks for duplicate entries."""
    dict_path = _get_dict_path()
    entries = _load_entries(dict_path)

    seen = {}
    duplicates = []
    for word, tag, score in entries:
        if word in seen:
            duplicates.append((word, tag, score))
        else:
            seen[word] = (tag, score)

    if duplicates:
        print(f"Found {len(duplicates)} duplicate(s):")
        for word, tag, score in duplicates:
            print(f"  {word} {tag} {score}")
        return 1

    print(f"No duplicates. ({len(entries)} entries)")
    return 0


def main():
    """Entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="personal_dict",
        description="Personal Dictionary CLI for Kiwi morphological analyzer"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Add a word to the dictionary")
    p_add.add_argument("word", help="Word to add")
    p_add.add_argument("--tag", default="NNG", help="POS tag (default: NNG)")
    p_add.add_argument("--score", type=float, default=1.0,
                       help="Priority score (default: 1.0)")

    p_list = sub.add_parser("list", help="List all entries")
    p_list.add_argument("--sort", action="store_true",
                        help="Sort alphabetically")

    p_search = sub.add_parser("search", help="Search for a word")
    p_search.add_argument("query", help="Search query (substring match)")

    sub.add_parser("sort", help="Sort entries in-place")
    sub.add_parser("check", help="Check for duplicates")

    args = parser.parse_args()
    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "search": cmd_search,
        "sort": cmd_sort,
        "check": cmd_check,
    }
    sys.exit(commands[args.command](args))


if __name__ == "__main__":
    main()
