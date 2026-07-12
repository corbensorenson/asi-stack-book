# Linux MLX preflight stubs

GitHub Actions runs on Linux, while the frozen P1/P2 outcome runners import
Apple MLX at module load. Their registered `--preflight` paths do not load a
model, generate tokens, or call MLX operations; they only exercise the separate
observer/evaluator and learned routing setup.

The build and scheduled-deep workflows place this directory on `PYTHONPATH`
only for deep validation. These stubs satisfy those imports and raise
immediately if generation, model loading, sampling, or random seeding is ever
attempted. They are not an MLX implementation, execution fallback, result
reproducer, or evidence source. The frozen runners and their setup-commit
digests remain unchanged.
