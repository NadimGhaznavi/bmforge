"""Regression fixtures for the documented native Fail2ban journal filter.

Offline checks use the 1.1.x formatJournalEntry prefix shape, not a substitute
for the required fail2ban-regex test on a real systemd journal.
"""

from configparser import ConfigParser
from ipaddress import ip_address
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
FAIL2BAN = ROOT / "pages/component-fail2ban.md"
PRODUCER = ROOT / "pages/component-security-events.md"
FIXTURE = ROOT / "tests/fixtures/journal-security-events.json"

# From native fail2ban 1.1.x common.conf [lt_short], with _daemon=\S*:
# \s*(?:<__hostname>\s+)?(?:<_daemon><__pid_re>?:?\s+)?
# This is a representative offline check only; fail2ban-regex on journald is
# mandatory before enabling a real jail.
JOURNAL_PREFIX = r"\s*(?:\S+\s+)?(?:\S*(?:\[\d+\])?:?\s+)?"
ADDRESS = r"(?P<ip>[0-9a-fA-F:.]+)"


def native_journal_line(entry):
    """Reconstruct hostname/identifier[pid]: MESSAGE as Fail2ban does."""
    parts = []
    if entry.get("_HOSTNAME"):
        parts.append(entry["_HOSTNAME"])
    identifier = entry.get("SYSLOG_IDENTIFIER") or entry.get("_COMM")
    if identifier:
        pid = entry.get("SYSLOG_PID") or entry.get("_PID")
        parts.append(f"{identifier}[{pid}]:" if pid else f"{identifier}:")
    parts.append(entry["MESSAGE"])
    return " ".join(parts)


class Fail2banJournalContractTests(unittest.TestCase):
    def test_example_uses_native_journal_prefix_instead_of_bare_message(self):
        spec = FAIL2BAN.read_text()
        example = re.search(
            r"\x60\x60\x60ini\n(\[INCLUDES\]\nbefore = common\.conf.*?journalmatch = _SYSTEMD_UNIT=myapp\.service)\n\x60\x60\x60",
            spec, re.DOTALL,
        )
        self.assertIsNotNone(example, "Fail2ban must supply a complete native filter example")
        config = ConfigParser(interpolation=None)
        config.read_string(example.group(1))
        self.assertEqual(config["INCLUDES"]["before"], "common.conf")
        self.assertEqual(config["DEFAULT"]["logtype"], "journal")
        self.assertEqual(config["Definition"]["failregex"],
                         "^%(__prefix_line)sSECURITY event=abuse ip=<HOST>$")
        self.assertEqual(config["Definition"]["journalmatch"], "_SYSTEMD_UNIT=myapp.service")
        self.assertNotIn("logpath", config["Definition"])
        self.assertIn("no automatic legacy migration", spec.lower())

    def test_realistic_metadata_formats_to_distinct_strict_event_matches(self):
        fixture = json.loads(FIXTURE.read_text())
        self.assertEqual(fixture["unit"], "mycount-server.service")
        seen = set()
        for entry in fixture["entries"]:
            with self.subTest(message=entry["MESSAGE"], unit=entry["_SYSTEMD_UNIT"]):
                self.assertIn("__REALTIME_TIMESTAMP", entry)
                self.assertNotIn(entry["__REALTIME_TIMESTAMP"], entry["MESSAGE"])
                line = native_journal_line(entry)
                matches = []
                if entry["_SYSTEMD_UNIT"] == fixture["unit"]:
                    for event in ("bad_request", "auth_failure"):
                        expression = re.compile(
                            r"^" + JOURNAL_PREFIX +
                            r"SECURITY event=" + re.escape(event) +
                            r" ip=" + ADDRESS + r"$"
                        )
                        found = expression.fullmatch(line)
                        if found:
                            try:
                                ip = str(ip_address(found.group("ip")))
                            except ValueError:
                                continue
                            matches.append((event, ip))
                expected = [] if entry["event"] is None else [(entry["event"], entry["address"])]
                self.assertEqual(matches, expected)
                seen.update(event for event, _ in matches)
        self.assertEqual(seen, {"bad_request", "auth_failure"})

    def test_producer_does_not_embed_timestamp_or_own_security_policy(self):
        spec = PRODUCER.read_text()
        code = (ROOT / "components/templates/security-events/interface/SecurityEvents.py").read_text()
        self.assertIn('spec_version: "0.1.1"', spec)
        self.assertIn('spec_version: "0.3.1"', FAIL2BAN.read_text())
        self.assertIn('warning("SECURITY event=%s ip=%s"', code)
        self.assertNotIn("datetime", code)
        self.assertIn("journald", spec)
        self.assertIn("no application timestamp", spec.lower())
        self.assertNotIn("fail2ban", code.lower().split("class securityevents", 1)[1])

    def test_native_acceptance_covers_two_jails_without_app_counters(self):
        spec = FAIL2BAN.read_text()
        for literal in (
            "fail2ban-client -t", "fail2ban-client -d", "import systemd.journal",
            "journalctl -u myapp.service -o cat", "journalctl -u myapp.service -o verbose",
            "fail2ban-regex -m", "bad_request", "auth_failure", "3 events in 60 seconds",
            "5 events in 300 seconds", "overlapping", "Fail2ban aggregates",
        ):
            self.assertIn(literal, spec, literal)


if __name__ == "__main__":
    unittest.main()
