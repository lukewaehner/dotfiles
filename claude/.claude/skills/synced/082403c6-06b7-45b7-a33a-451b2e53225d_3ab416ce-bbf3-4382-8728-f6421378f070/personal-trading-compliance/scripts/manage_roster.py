"""
manage_roster.py — read/edit the employee roster and detect unrostered filers.

The roster (references/roster.yaml) is CCO-owned; this script just makes edits safe and
consistent, and finds people who are filing but aren't on the list yet. It NEVER auto-adds
anyone — `detect-unrostered` only proposes; a human confirms with `add`.

Commands:
  list                                             show the roster
  add --name N --emails a@x,b@y [--thread "S"] [--broker "Fidelity:1234"] [--no-notify]
  update --name N [--add-email e] [--add-thread S] [--notify true|false]
  depart --name N                                  mark departed (kept for history, skipped in sweeps)
  detect-unrostered --filers filers.json [--out proposals.json]
        filers.json = [{"name":"Bob","address":"bob@meteoracapital.com","subject":"Bob – Pre-Clearance"}]

All paths default to the roster.yaml next to this script's references/ folder.
"""
from __future__ import annotations
import sys, os, argparse, json
sys.path.insert(0, os.path.dirname(__file__))
import yaml

DEFAULT_ROSTER = os.path.join(os.path.dirname(__file__), "..", "references", "roster.yaml")


def load_roster(path):
    if not os.path.exists(path):
        return {"employees": []}
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    data.setdefault("employees", [])
    return data


def save_roster(data, path):
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True, default_flow_style=False)


def known_addresses(data):
    addrs = set()
    for e in data.get("employees", []):
        for a in (e.get("emails") or []):
            if a:
                addrs.add(str(a).strip().lower())
    return addrs


def _find(data, name):
    for e in data["employees"]:
        if str(e.get("employee", "")).strip().lower() == name.strip().lower():
            return e
    return None


def cmd_list(data):
    if not data["employees"]:
        print("(roster is empty)")
        return
    for e in data["employees"]:
        st = e.get("status", "active")
        threads = ", ".join(t.get("subject", "") for t in (e.get("preclearance_threads") or []))
        print(f"- {e.get('employee')} [{st}] notify={e.get('notify')}")
        print(f"    emails: {', '.join(e.get('emails') or [])}")
        print(f"    threads: {threads or '(none)'}")


def cmd_add(data, args, path):
    if _find(data, args.name):
        print(f"'{args.name}' already exists — use `update`.")
        return
    entry = {
        "employee": args.name,
        "status": "active",
        "emails": [x.strip() for x in (args.emails or "").split(",") if x.strip()],
        "preclearance_threads": ([{"subject": args.thread, "conversation_id": ""}] if args.thread else []),
        "brokers": [],
        "exempt_accounts": [],
        "notify": not args.no_notify,
    }
    for b in (args.broker or "").split(";"):
        if b.strip():
            name, _, last4 = b.partition(":")
            entry["brokers"].append({"name": name.strip(), "account_last4": last4.strip()})
    data["employees"].append(entry)
    save_roster(data, path)
    print(f"Added {args.name}. Roster now has {len(data['employees'])} entries.")


def cmd_update(data, args, path):
    e = _find(data, args.name)
    if not e:
        print(f"'{args.name}' not found.")
        return
    if args.add_email:
        e.setdefault("emails", []).append(args.add_email.strip())
    if args.add_thread:
        e.setdefault("preclearance_threads", []).append({"subject": args.add_thread, "conversation_id": ""})
    if args.notify is not None:
        e["notify"] = str(args.notify).lower() in ("1", "true", "yes")
    save_roster(data, path)
    print(f"Updated {args.name}.")


def cmd_depart(data, args, path):
    e = _find(data, args.name)
    if not e:
        print(f"'{args.name}' not found.")
        return
    e["status"] = "departed"
    save_roster(data, path)
    print(f"Marked {args.name} departed (kept for history, skipped in sweeps).")


def cmd_detect(data, args):
    with open(args.filers, "r", encoding="utf-8") as f:
        filers = json.load(f)
    known = known_addresses(data)
    proposals, seen = [], set()
    for fl in filers:
        addr = str(fl.get("address", "")).strip().lower()
        if not addr or addr in known or addr in seen:
            continue
        seen.add(addr)
        proposals.append({"name": fl.get("name"), "address": fl.get("address"),
                          "sample_subject": fl.get("subject"), "first_seen": fl.get("first_seen")})
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(proposals, f, indent=2, ensure_ascii=False)
    if not proposals:
        print("No unrostered filers — everyone filing is on the roster.")
    else:
        print(f"{len(proposals)} UNROSTERED FILER(S) — confirm before processing their trades:")
        for p in proposals:
            print(f"  • {p['name'] or '(unknown)'} <{p['address']}>  subj: {p['sample_subject']}")
    return proposals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--roster", default=DEFAULT_ROSTER)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list")
    pa = sub.add_parser("add")
    pa.add_argument("--name", required=True); pa.add_argument("--emails", default="")
    pa.add_argument("--thread", default=""); pa.add_argument("--broker", default="")
    pa.add_argument("--no-notify", action="store_true")
    pu = sub.add_parser("update")
    pu.add_argument("--name", required=True); pu.add_argument("--add-email", default="")
    pu.add_argument("--add-thread", default=""); pu.add_argument("--notify", default=None)
    pd = sub.add_parser("depart"); pd.add_argument("--name", required=True)
    pdet = sub.add_parser("detect-unrostered")
    pdet.add_argument("--filers", required=True); pdet.add_argument("--out", default="")
    args = ap.parse_args()

    data = load_roster(args.roster)
    if args.cmd == "list":
        cmd_list(data)
    elif args.cmd == "add":
        cmd_add(data, args, args.roster)
    elif args.cmd == "update":
        cmd_update(data, args, args.roster)
    elif args.cmd == "depart":
        cmd_depart(data, args, args.roster)
    elif args.cmd == "detect-unrostered":
        cmd_detect(data, args)


if __name__ == "__main__":
    main()
