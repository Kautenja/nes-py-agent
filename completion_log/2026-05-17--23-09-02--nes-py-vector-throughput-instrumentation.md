# Completion Log: nes-py Vector Throughput Instrumentation

## Summary

Completed spec 052 by extending `nes_py.speedtest` with repeated vector
profiles for scalar loops, Gymnasium vector baselines, and the native vector
prototype. The JSON output includes host/build metadata, env counts, action and
observation modes, setup/teardown timing, native step timing, synchronization,
observation access, RAM/info readback, Python overhead, worker stats, and
explicit CPU-affinity experiment labels.

## Verification

- `nes-py`: `.venv/bin/python -m unittest nes_py.tests.test_speedtest` (`11 tests`, `OK`)
- `nes-py`: `.venv/bin/python -m unittest discover .` (`246 tests`, `OK`)
- `nes-py`: `build/nes-emu-release/nes_emu_benchmarks --benchmark-samples 1 --benchmark-resamples 1`
- `nes-py`: `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --vector-profile --steps 10 --warmup-steps 2 --runs 2 --env-counts 1,2,4 --action-policy noop --vector-backend scalar_loop --vector-backend gym_sync_vector_env --vector-backend native_vector --vector-observation step_only --vector-observation native_grayscale --vector-observation ram_info --instrumentation --json --no-progress`
- `nes-py`: `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --steps 1000 --warmup-steps 100 --json --no-progress`
- `nes-py`: `.venv/bin/python -m nes_py.speedtest --rom nes_py/tests/games/super-mario-bros-1.nes --observation-profile --steps 1000 --warmup-steps 100 --action-policy noop --json --no-progress`
- `nes-py`: `git diff --check`

## Notes

The instrumentation overhead check in
`docs/vector-throughput-instrumentation.md` measured a -0.31% median difference
for native vector step-only throughput with instrumentation enabled, inside the
1% budget. No CPU affinity or synchronization optimization was kept.

## Commits

- `nes-py`: `61862c9` (`p90`, pushed to `origin/p90`)
- Umbrella: included in the umbrella commit that records this completion log
