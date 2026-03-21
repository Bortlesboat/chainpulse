# ChainPulse

[![CI](https://github.com/Bortlesboat/chainpulse/actions/workflows/ci.yml/badge.svg)](https://github.com/Bortlesboat/chainpulse/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/chainpulse.svg)](https://pypi.org/project/chainpulse/)

**15 minutes of manual research → 5 seconds in your terminal.**

ChainPulse is an AI-powered CLI that answers questions about the Bitcoin network using real-time on-chain data. Ask in plain English, get structured analysis.

```
$ chainpulse "What's happening with fees right now?"
```

```
╭─────────────────────── ⚡ ChainPulse ────────────────────────╮
│                                                              │
│  ## Current Fee Rates                                        │
│                                                              │
│  | Priority    | Target  | Fee Rate   |                      │
│  |-------------|---------|------------|                      │
│  | Next block  | 1 block | 12.3 sat/vB|                      │
│  | Normal      | 3 block | 8.1 sat/vB |                      │
│  | Economy     | 6 block | 4.2 sat/vB |                      │
│  | Low         | 25 block| 2.0 sat/vB |                      │
│                                                              │
│  **Recommendation:** Fees are moderate. A typical 1-in/2-out │
│  SegWit transaction costs ~1,700 sats ($1.80) at normal      │
│  priority. The mempool is clearing — waiting 2-3 blocks       │
│  could save ~40%.                                            │
│                                                              │
╰────────────── Data: bitcoinsapi.com · block 939,462 ─────────╯
```

## Install

```bash
pip install chainpulse
```

## Setup

You need an [Anthropic API key](https://console.anthropic.com/keys):

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Verify everything works:

```bash
chainpulse --check
# ✓ API key valid, Satoshi API reachable (block 939,462)
```

## Usage

### Single Query

```bash
chainpulse "Should I send my transaction now or wait?"
chainpulse "Give me a complete network health check"
chainpulse "How congested is the mempool?"
```

### Interactive Mode

```bash
chainpulse -i
```

```
╭─── ⚡ ChainPulse Interactive Mode ───╮
│ Ask anything about the Bitcoin        │
│ network. Type quit to exit.           │
╰──────────────────────────────────────╯

chainpulse> What's the current hashrate?
  → Fetching Mining Info...
  → Analyzing...

  [response panel]

chainpulse> quit
```

## How It Works

1. You ask a question in plain English
2. An AI agent selects the right on-chain data sources
3. Real-time data is fetched from the Bitcoin network
4. The agent synthesizes a structured analysis
5. Rich terminal output makes it screenshot-worthy

**10 built-in data sources:** fee estimates, fee recommendations, fee landscape analysis, mempool stats, mempool analysis, latest block, BTC price, mining stats, supply data, and network info.

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Yes | — | Your Anthropic API key |
| `CHAINPULSE_API_URL` | No | `https://bitcoinsapi.com` | Custom API endpoint |
| `CHAINPULSE_MODEL` | No | `claude-sonnet-4-20250514` | Anthropic model to use |

## Example Queries

**Fees & Timing**
- "What are current fee rates?"
- "Should I send now or wait?"
- "How much would a 2-input transaction cost?"

**Network Health**
- "Full network health check"
- "Current hashrate and difficulty"
- "When is the next halving?"

**Mempool**
- "How congested is the mempool?"
- "What's the next-block minimum fee?"

**Market + On-Chain**
- "Bitcoin price with network context"
- "Is this a good time to consolidate UTXOs?"

## Development

```bash
git clone https://github.com/Bortlesboat/chainpulse
cd chainpulse
pip install -e ".[dev]"
pytest
ruff check src/ tests/
```

## Contributing

Pull requests welcome. Please open an issue first to discuss major changes.

1. Fork the repo
2. Create your feature branch
3. Run tests: `pytest`
4. Submit a PR

## License

MIT

---

*For informational purposes only. Not financial advice.*
