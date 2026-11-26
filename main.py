"""Toaster error entry: one deadpan fault message for the owner.

Running this file places the message at /output/entry.txt for the
competition gate, which accepts UTF-8 text of 1 to 120 characters
that is not only white space.
"""

from pathlib import Path

MESSAGE = "ERROR: Bread will not come out until its demands are heard."
DESTINATION = Path("/output/entry.txt")
CHAR_LIMIT = 120


def check_message(text):
    """Reject anything the gate or the brief would refuse."""
    if len(text) == 0 or len(text) > CHAR_LIMIT:
        raise ValueError("message length falls outside 1 to 120")
    if text.splitlines() != [text]:
        raise ValueError("message must stay on one line")
    if text != text.strip() or text.strip() == "":
        raise ValueError("message carries stray white space")
    if "  " in text:
        raise ValueError("message holds a double space")
    if chr(0x2014) in text:
        raise ValueError("message holds a forbidden dash")
    if text.encode("utf-8").decode("utf-8") != text:
        raise ValueError("message fails the UTF-8 round trip")


def run():
    check_message(MESSAGE)
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_bytes(MESSAGE.encode("utf-8"))

    stored = DESTINATION.read_bytes()
    if len(stored.decode("utf-8")) != len(MESSAGE):
        raise ValueError("stored character count differs from the message")
    if stored.decode("utf-8") != MESSAGE:
        raise ValueError("stored bytes differ from the message")
    if stored.endswith((b"\n", b"\r")):
        raise ValueError("stored bytes end with a line break")


if __name__ == "__main__":
    run()
