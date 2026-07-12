"""Fail-closed sampler stub for Linux no-model-call preflights."""


def make_sampler(*_args, **_kwargs):
    raise RuntimeError("Linux MLX preflight stub forbids sampler construction")
