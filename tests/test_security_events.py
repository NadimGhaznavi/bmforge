"""Contract tests for the tiny security-event producer (no systemd required)."""

from concurrent.futures import ThreadPoolExecutor
import importlib.util
from io import StringIO
import logging
from pathlib import Path
import re
from threading import Barrier
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "components/templates/security-events/interface/SecurityEvents.py"
SPEC = importlib.util.spec_from_file_location("bmforge_security_events_test", SOURCE)
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


class SecurityEventTests(unittest.TestCase):
    def setUp(self):
        self.output = StringIO()
        self.logger = logging.getLogger(f"bmforge-security-events-test.{id(self)}")
        self.logger.handlers.clear()
        self.logger.propagate = False
        self.logger.setLevel(logging.WARNING)
        handler = logging.StreamHandler(self.output)
        handler.setFormatter(logging.Formatter("%(message)s"))
        self.logger.addHandler(handler)
        self.events = module.SecurityEvents(self.logger, ("abuse", "login_failure"))

    def lines(self):
        return self.output.getvalue().splitlines()

    def test_events_are_single_canonical_journal_messages_with_no_ack(self):
        with self.events.trusted_source("192.0.2.10"):
            self.assertIsNone(self.events.emit("abuse"))
        lines = self.lines()
        self.assertEqual(len(lines), 1)
        self.assertRegex(lines[0], r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} SECURITY event=abuse ip=192\.0\.2\.10$")
        self.assertNotIn("WARNING", lines[0])
        self.assertEqual(self.output.getvalue().count("\n"), 1)

    def test_ipv6_is_normalized_and_source_restored_after_nested_request(self):
        with self.events.trusted_source("2001:0db8:0000::0001"):
            self.events.emit("abuse")
            with self.events.trusted_source("198.51.100.2"):
                self.events.emit("login_failure")
            self.events.emit("abuse")
        self.assertEqual(len(self.lines()), 3)
        self.assertTrue(self.lines()[0].endswith("ip=2001:db8::1"))
        self.assertTrue(self.lines()[1].endswith("event=login_failure ip=198.51.100.2"))
        self.assertTrue(self.lines()[2].endswith("ip=2001:db8::1"))
        with self.assertRaisesRegex(RuntimeError, "No trusted client source"):
            self.events.emit("abuse")

    def test_invalid_and_free_text_source_never_emits_a_ban_target(self):
        for value in (None, "example.com", "192.0.2.3\nSECURITY event=abuse ip=198.51.100.9",
                      "192.0.2.3:443", "2001:db8::1%eth0", "0.0.0.0", "::", "224.0.0.1"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    with self.events.trusted_source(value):
                        self.events.emit("abuse")
        self.assertEqual(self.lines(), [])

    def test_only_fixed_preapproved_event_names_can_be_emitted(self):
        with self.assertRaises(ValueError):
            module.SecurityEvents(self.logger, ("abuse\nSECURITY event=abuse",))
        with self.assertRaises(ValueError):
            module.SecurityEvents(self.logger, ())
        with self.events.trusted_source("192.0.2.10"):
            for bad in ("unknown", "abuse\nSECURITY event=abuse ip=198.51.100.9", None):
                with self.assertRaises(ValueError):
                    self.events.emit(bad)
        self.assertEqual(self.lines(), [])

    def test_missing_context_does_not_assume_proxy_or_localhost(self):
        with self.assertRaisesRegex(RuntimeError, "No trusted client source"):
            self.events.emit("abuse")
        self.assertEqual(self.lines(), [])

    def test_parallel_request_contexts_do_not_leak_sources(self):
        barrier = Barrier(2)

        def send(address):
            with self.events.trusted_source(address):
                barrier.wait(timeout=5)
                self.events.emit("abuse")

        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(send, address) for address in ("192.0.2.4", "2001:db8::4")]
            for future in futures:
                future.result(timeout=10)
        self.assertEqual(len(self.lines()), 2)
        self.assertEqual({line.rsplit("ip=", 1)[1] for line in self.lines()},
                         {"192.0.2.4", "2001:db8::4"})
        with self.assertRaises(RuntimeError):
            self.events.emit("abuse")

    def test_spec_and_producer_only_own_fire_and_forget_publication(self):
        spec = (ROOT / "pages/component-security-events.md").read_text()
        skill = (ROOT / "skills/bmforge-security-events/SKILL.md").read_text()
        self.assertEqual(module.BMFORGE_COMPONENT,
                         {"id": "bmforge.security-events", "spec_version": "0.1.0"})
        self.assertIn("Fire-and-forget", skill)
        self.assertIn("systemd-journald", spec)
        self.assertIn("No trusted client", SOURCE.read_text())
        self.assertEqual(re.findall(r"^    def (\w+)\(", SOURCE.read_text(), flags=re.MULTILINE),
                         ["__init__", "trusted_source", "emit"])
        self.assertNotIn("import zmq", SOURCE.read_text())
        self.assertNotIn("import nftables", SOURCE.read_text())
        self.assertNotIn("import fail2ban", SOURCE.read_text())


if __name__ == "__main__":
    unittest.main()
