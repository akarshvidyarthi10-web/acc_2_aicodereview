"""
Simple Intrusion Detection System (IDS) Example
------------------------------------------------
This script simulates packet inspection, rule-based detection,
and logging for suspicious activity. It is purely educational
and not intended for production use.
"""

import random
import time
import logging
from typing import List, Dict, Any

# ------------------------------
# Logger Setup
# ------------------------------
logging.basicConfig(
    filename="ids.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------------------
# Packet Simulation
# ------------------------------
class Packet:
    def __init__(self, src_ip: str, dst_ip: str, payload: str, protocol: str):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.payload = payload
        self.protocol = protocol

    def __repr__(self):
        return f"Packet(src={self.src_ip}, dst={self.dst_ip}, proto={self.protocol}, payload={self.payload})"


def generate_random_packet() -> Packet:
    ips = ["192.168.1.10", "10.0.0.5", "172.16.0.3", "203.0.113.55"]
    payloads = ["GET /index.html", "DROP TABLE users;", "PING", "ssh login attempt", "normal traffic"]
    protocols = ["TCP", "UDP", "ICMP"]

    return Packet(
        src_ip=random.choice(ips),
        dst_ip=random.choice(ips),
        payload=random.choice(payloads),
        protocol=random.choice(protocols)
    )

# ------------------------------
# Detection Rules
# ------------------------------
class Rule:
    def __init__(self, name: str, keyword: str, severity: str):
        self.name = name
        self.keyword = keyword
        self.severity = severity

    def match(self, packet: Packet) -> bool:
        return self.keyword.lower() in packet.payload.lower()


class RuleSet:
    def __init__(self):
        self.rules: List[Rule] = []

    def add_rule(self, rule: Rule):
        self.rules.append(rule)
        logging.info(f"Rule added: {rule.name}")

    def check_packet(self, packet: Packet) -> List[Dict[str, Any]]:
        alerts = []
        for rule in self.rules:
            if rule.match(packet):
                alerts.append({
                    "rule": rule.name,
                    "severity": rule.severity,
                    "packet": packet
                })
        return alerts

# ------------------------------
# IDS Core
# ------------------------------
class IDS:
    def __init__(self, ruleset: RuleSet):
        self.ruleset = ruleset
        self.alerts: List[Dict[str, Any]] = []

    def inspect(self, packet: Packet):
        logging.debug(f"Inspecting packet: {packet}")
        matches = self.ruleset.check_packet(packet)
        if matches:
            for alert in matches:
                self.alerts.append(alert)
                logging.warning(f"ALERT: {alert['rule']} triggered by {alert['packet']}")

    def run(self, iterations: int = 50):
        for _ in range(iterations):
            pkt = generate_random_packet()
            self.inspect(pkt)
            time.sleep(0.1)

    def summary(self):
        print("\n--- IDS Summary ---")
        for alert in self.alerts:
            print(f"Rule: {alert['rule']} | Severity: {alert['severity']} | Packet: {alert['packet']}")
        print(f"Total Alerts: {len(self.alerts)}")

# ------------------------------
# Example Rules
# ------------------------------
def build_default_ruleset() -> RuleSet:
    rs = RuleSet()
    rs.add_rule(Rule("SQL Injection Attempt", "DROP TABLE", "HIGH"))
    rs.add_rule(Rule("Ping Flood", "PING", "MEDIUM"))
    rs.add_rule(Rule("Unauthorized SSH", "ssh login", "HIGH"))
    rs.add_rule(Rule("Suspicious GET", "GET /index.html", "LOW"))
    return rs

# ------------------------------
# Main Execution
# ------------------------------
if __name__ == "__main__":
    ruleset = build_default_ruleset()
    ids = IDS(ruleset)
    ids.run(iterations=100)
    ids.summary()
