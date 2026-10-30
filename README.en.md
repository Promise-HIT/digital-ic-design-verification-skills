# Digital IC Design & Verification Skills

A Chinese-first collection of three Agent Skills for digital IC frontend work: synthesizable RTL, verification planning and implementation, and evidence-based review and debugging.

[中文说明](README.md) · [Examples](docs/EXAMPLES.md) · [MIT License](LICENSE)

| Skill | Scope |
| --- | --- |
| [digital-ic-rtl-design](skills/digital-ic-rtl-design/SKILL.md) | Interface contracts, microarchitecture, SystemVerilog, FIFO/FSM/handshakes, reset, CDC/RDC and EDA workflows |
| [digital-ic-verification](skills/digital-ic-verification/SKILL.md) | Requirement-traceable plans, independent checkers, UVM, SVA, coverage and regression closure |
| [digital-ic-review-debug](skills/digital-ic-review-debug/SKILL.md) | Evidence-backed findings, causal triage, reproducible failures and signoff gaps |

Install all three as sibling directories: some references are shared through relative links. Instructions and references are primarily Chinese; this page is an English overview.

## Install

Clone this repository or download and extract its ZIP. From the repository root, with Python 3.10+:

```powershell
# Windows PowerShell
python scripts/install.py --dest "$env:USERPROFILE/.agents/skills"
```

```bash
# macOS / Linux
python3 scripts/install.py --dest "$HOME/.agents/skills"
```

For a single project, pass that project's `.agents/skills` directory instead. The installer copies all three skills and refuses existing destinations. It does not change agent configuration or install EDA tools.

See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills) for Codex discovery and invocation. Other agents may use different installation locations; compatibility has not been tested individually.

## Use

```text
Use $digital-ic-rtl-design to implement a parameterized FIFO from this specification.
Inspect the project build first, state reset and simultaneous-transfer semantics,
and report the checks that actually ran.
```

Use `$digital-ic-verification` for test plans and testbenches, and `$digital-ic-review-debug` for reviews or failure diagnosis. [Examples](docs/EXAMPLES.md) include the four bundled Python utilities.

The utilities use the Python standard library. Real lint, simulation, formal, synthesis and STA need the project's tools, licenses, libraries and constraints. A process returning zero or a metadata check passing is not proof of design correctness.

## Validate

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_repo.py
python -m unittest discover -s tests -v
```

Windows and Linux CI validate metadata, relative links, Python syntax and observable utility behavior. CI does not run an EDA signoff flow.

## Sources and license

Organized from the supplied enhanced skill bundle. Personal absolute paths, duplicate backups and prior run reports are excluded. Original books, company manuals, EDA software, process libraries and UVM distributions are not included. Inherited source hashes were not independently reverified during publication preparation. See [source notes](docs/SOURCES.md).

Repository content is released under the [MIT License](LICENSE). External materials remain subject to their owners' rights and terms.
