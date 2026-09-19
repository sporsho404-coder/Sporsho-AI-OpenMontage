# INTEGRATIONS — How Everything Connects

Wiring between Arena, GitHub, OpenMontage, and `D:\SPORSHO AI`.

---

## The Full Picture

```
┌──────────────┐
│   ARENA      │  you talk to this
└──────┬───────┘
       │ reads instructions
       ↓
┌──────────────────────────────────────────────┐
│ GITHUB (private)                             │
│ Sporsho-AI-OpenMontage                       │
│  ├── SPORSHO/        ← your layer            │
│  └── OpenMontage     ← upstream, unmodified  │
└──────┬───────────────────────────────────────┘
       │ cloned to / read from
       ↓
┌──────────────┐        OPENMONTAGE_PROJECTS_DIR
│  WORKING     │ ─────────────────────────────────┐
│  MACHINE     │                                  │
└──────┬───────┘                                  ↓
       │ executes tools          ┌────────────────────────────┐
       └────────────────────────→│  D:\SPORSHO AI             │
                                 │  projects/ clients/        │
                                 │  references/ library/      │
                                 │  exports/ cache/           │
                                 └────────────────────────────┘
```

## The Four Connections

| Connection | Mechanism | Doc |
|---|---|---|
| Arena → repo | Agent reads markdown instructions | [`../sporsho/ARENA.md`](../../docs/sporsho/ARENA.md) |
| repo → local disk | `OPENMONTAGE_PROJECTS_DIR` env var | [`../sporsho/INTEGRATION.md`](../../docs/sporsho/INTEGRATION.md) §1 |
| repo → upstream | `git fetch upstream && git merge` | [`GITHUB.md`](GITHUB.md) |
| tools → disk | Explicit `output_path` under `projects/<id>/` | [`../sporsho/LOCAL-MEDIA.md`](../../docs/sporsho/LOCAL-MEDIA.md) |

## Files

| File | Covers |
|---|---|
| [`GITHUB.md`](GITHUB.md) | Repository & remote operations |
| [`UPSTREAM.md`](UPSTREAM.md) | Staying in sync with OpenMontage |
| [`PROVIDERS.md`](PROVIDERS.md) | API keys and provider availability |
| [`LOCAL-DRIVE.md`](LOCAL-DRIVE.md) | Wiring the drive, per platform |

## Configuration Files

| Path | Owner | Holds |
|---|---|---|
| `config.yaml` | **upstream** | LLM provider, budget, checkpoint policy, output defaults |
| `.env` | **you** — never commit | API keys for 30+ providers |
| `.env.example` | upstream | The list of supported keys |

## The Golden Rule

Everything above works because Sporsho knowledge lives in `SPORSHO/` and upstream
files are left alone. The moment you edit an upstream file to store your own
knowledge, `git merge upstream/main` starts conflicting and the update path breaks.

**Your knowledge in `SPORSHO/`. Upstream's machinery untouched. One env var pointing
at your drive.** That is the entire architecture.
