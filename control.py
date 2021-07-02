#!/usr/bin/env python
"""Convenience script wrapper to start and stop AiiDAlab via docker-compose.

Authors:
    * Carl Simon Adorf <simon.adorf@epfl.ch>
"""
import os
import sys
from pathlib import Path
from secrets import token_hex
from subprocess import run
from time import sleep

import click


def _service_is_up(docker_compose, service):
    aiidalab_container_id = (
        docker_compose(["ps", "-q", "aiidalab"], check=True, capture_output=True)
        .stdout.decode()
        .strip()
    )
    if aiidalab_container_id:
        running_containers = (
            run(["docker", "ps", "-q", "--no-trunc"], check=True, capture_output=True)
            .stdout.decode()
            .strip()
            .splitlines()
        )
        return aiidalab_container_id in running_containers
    else:
        return False


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--home-dir",
    type=click.Path(),
    default=Path.home(),
    help="Specify a path to a directory on a host system that is to be mounted "
    "as the home directory on the AiiDAlab service.",
    show_default=True,
)
@click.option(
    "--port",
    default=8888,
    help="Port on which AiiDAlab can be accessed.",
    show_default=True,
)
@click.option(
    "--jupyter-token",
    help="A secret token that is needed to access AiiDAlab for the first time.",
)
@click.option(
    "--restart", is_flag=True, help="Restart AiiDAlab in case that it is already up."
)
def up(home_dir, port, jupyter_token, restart):
    """Start AiiDAlab on this host."""
    jupyter_token = token_hex(32) if jupyter_token is None else jupyter_token
    env = {
        "AIIDALAB_HOME": str(home_dir),
        "AIIDALAB_PORT": str(port),
        "JUPYTER_TOKEN": str(jupyter_token),
        "PATH": os.environ["PATH"],
    }

    def _docker_compose(args, **kwargs):
        return run(["docker-compose", *args], env=env, **kwargs)

    # Check if server is already started.
    if not restart and _service_is_up(_docker_compose, "aiidalab"):
        click.echo("Service is already running. Use the `--restart` option to restart.")
        return

    click.echo("Starting AiiDAlab...")
    _docker_compose(["up", "--detach", "--build"], check=True, capture_output=True)

    # A short sleep is necessary as the following command might fail if
    # executed immediately after the previous command
    sleep(0.5)

    _docker_compose(["exec", "aiidalab", "wait-for-services"], check=True)

    click.secho("Container started successfully.", fg="green")
    click.secho(f"Open this link in the browser to enter AiiDAlab:", fg="green")
    click.secho(f"http://localhost:{port}/?token={jupyter_token}", fg="green")


@cli.command()
def down():
    """Stop AiiDAlab on this host."""
    run(["docker-compose", "down"], check=True)
    click.echo("AiiDAlab stopped.")


if __name__ == "__main__":
    cli()
