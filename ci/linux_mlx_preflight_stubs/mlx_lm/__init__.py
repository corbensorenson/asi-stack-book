"""Fail-closed mlx-lm stub for Linux no-model-call preflights."""


def _forbidden(*_args, **_kwargs):
    raise RuntimeError("Linux MLX preflight stub forbids model loading or generation")


generate = _forbidden
load = _forbidden
