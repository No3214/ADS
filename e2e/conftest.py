"""Playwright e2e — varsayilan pytest suite'inin DISINDA (e2e/). CI'da --with-deps ile
calisir; lokalde tarayici varsa calisir, yoksa skipif ile atlanir. Container icin --no-sandbox."""
import pytest


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {**browser_type_launch_args,
            "args": ["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"]}
