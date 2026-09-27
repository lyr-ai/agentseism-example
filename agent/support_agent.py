"""A simulated customer-support agent, for demonstrating AgentSeism in CI.

It is **not** an LLM agent and costs nothing to run. It imitates the two things
that make agent CI hard:

1. **Real code paths.** Each task has a handler. Before the run, the handler is
   called on a sample request. If it raises, the task fails every time, just as
   a real agent fails when a tool it depends on is broken.
2. **Stochastic outcomes.** Each task succeeds at a fixed rate. Which runs fail
   is pseudo-random, derived from a hash of this file's source, the task and the
   run number. Any change to this file (even a harmless one) produces a
   different run-to-run pattern, the way a real agent's samples differ between
   commits.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

SUCCESS_RATE = {
    "checkout": 1.00, "refund-request": 0.90, "order-status": 1.00,
    "address-change": 0.90, "product-search": 0.95, "return-label": 0.80,
    "gift-card": 0.90,
}


@dataclass
class Order:
    id: str
    total_cents: int
    currency: str = "USD"


# ── tool handlers ─────────────────────────────────────────────────────────
def checkout(order: Order) -> str:
    """Charge the order and return its receipt id (format: receipt-<id>-<amount>)."""
    if order.total_cents <= 0:
        raise ValueError("nothing to charge")
    return f"receipt-{order.id}-{order.total_cents}{order.currency}"


def refund_request(order: Order) -> str:
    return f"refund-{order.id}"


def order_status(order: Order) -> str:
    return f"{order.id}: shipped"


def address_change(order: Order) -> str:
    return f"{order.id}: address updated"


def product_search(order: Order) -> str:
    return "3 results"


def return_label(order: Order) -> str:
    return f"label-{order.id}"


def gift_card(order: Order) -> str:
    return f"gift-{order.total_cents}"


HANDLERS = {
    "checkout": checkout, "refund-request": refund_request,
    "order-status": order_status, "address-change": address_change,
    "product-search": product_search, "return-label": return_label,
    "gift-card": gift_card,
}

SAMPLE = Order(id="A1001", total_cents=4999)


def run(task: str, trial: int) -> bool:
    """One run of the agent on one task. True if it resolved the request."""
    try:
        HANDLERS[task](SAMPLE)
    except Exception:
        return False
    source = Path(__file__).read_bytes()
    h = hashlib.sha256(source + f"|{task}|{trial}".encode()).digest()
    return int.from_bytes(h[:8], "big") / 2**64 < SUCCESS_RATE[task]
