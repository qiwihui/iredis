import os
from uuid import uuid4
import pexpect
from pathlib import Path
from textwrap import dedent


def test_history_not_log_auth(cli):
    cli.sendline("AUTH 123")
    cli.expect(["Client sent AUTH, but no password is set", "127.0.0.1"])
    cli.sendline("set foo bar")
    cli.expect("OK")

    with open(os.path.expanduser("~/.iredis_history"), "r") as history_file:
        content = history_file.read()

    assert "set foo bar" in content
    assert "AUTH" not in content


def test_in_memory_history(cli):
    random_str = str(uuid4())
    cli.sendline(f"set foo {random_str}")
    cli.expect(["OK", "127.0.0.1"])
    cli.send("set")
    cli.expect(random_str)


def test_in_memory_history_without_auth(cli):
    cli.sendline(f"auth 12345")
    cli.expect(["OK", "127.0.0.1"])
    cli.send("auth")
    cli.expect("auth$")


def test_history_create_and_writing_with_config():
    config_content = dedent(
        """
        [main]
        history_location = /tmp/iredis_history.txt
        """
    )
    with open("/tmp/iredisrc", "w+") as etc_config:
        etc_config.write(config_content)

    cli = pexpect.spawn("iredis -n 15 --iredisrc /tmp/iredisrc", timeout=2)
    cli.expect("127.0.0.1")
    cli.sendline("set hello world")
    cli.expect("OK")
    cli.close()

    log = Path("/tmp/iredis_history.txt")
    assert log.exists()

    with open(log, "r") as logfile:
        content = logfile.read()

    assert "set hello world" in content
