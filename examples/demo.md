# ChainPulse Demo Script

## Quick Start (60 seconds)

```bash
# Install
pip install chainpulse

# Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-...

# Single query — the money shot
chainpulse "What's happening with Bitcoin fees right now?"

# Interactive mode
chainpulse -i
> Should I send my transaction now or wait?
> Give me a complete network health check
> How congested is the mempool?
> quit
```

## Example Queries

**Fees & Timing:**
- "What are current fee rates?"
- "Should I send my transaction now or wait?"
- "How much would a typical transaction cost right now?"

**Network Health:**
- "Give me a full network health check"
- "What's the current hashrate and difficulty?"
- "How many halvings have occurred?"

**Mempool:**
- "How congested is the mempool?"
- "What's the minimum fee to get into the next block?"

**Market:**
- "What's the current Bitcoin price?"
- "Show me price and network stats together"

**Combined Analysis:**
- "Is this a good time to consolidate UTXOs?"
- "Compare current fees to what they might be tomorrow"
