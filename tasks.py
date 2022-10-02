# mypy: ignore_errors

from invoke_release.tasks import *  # noqa: F403

configure_release_parameters(  # noqa: F405
    module_name="pynction",
    display_name="pynction",
    use_pull_request=True,
)
