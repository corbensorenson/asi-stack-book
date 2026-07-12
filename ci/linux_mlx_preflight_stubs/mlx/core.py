"""Fail-closed MLX core stub for Linux no-model-call preflights."""


class _ForbiddenRandom:
    def seed(self, *_args, **_kwargs):
        raise RuntimeError("Linux MLX preflight stub forbids random/model execution")


random = _ForbiddenRandom()
