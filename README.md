P-VSAD Core: Automated Cryptographic Evidence Ledger

P-VSAD (Personalized Vigilance System for Actionable Data) is a lightweight, local-first cryptographic provenance and continuous evidence collection engine. It intercepts system telemetry, applies deterministic structural canonicalization, and securely seals events into unalterable, cryptographically signed receipts.

Key Architecture Highlights

Deterministic Invariance (RFC 8785-inspired):** Implements strict key sorting and serialization rules prior to hashing to completely eliminate hash drift across different environments.
Cryptographic Sealing (SHA3-512):** Computes high-security cryptographic hashes for every ingested telemetry payload.
Asymmetric Verification (Ed25519):** Automatically signs hash receipts using military-grade Ed25519 private keys, allowing third parties to mathematically verify data authenticity using your public key without trusting the underlying storage medium.
Decoupled Edge Daemon:** Features an autonomous local monitoring scout that captures system state and streams it safely over a FastAPI ingestion pipeline.

---

Project Structure

```text
p-vsad-core/
├── src/
│   └── pvsad/
│       ├── __init__.py
│       ├── backend.py      # FastAPI ingestion, canonicalization, and Ed25519 signing engine
│       ├── config.py       # Pydantic-based configuration management
│       ├── daemon.py       # Autonomous telemetry gathering scout
│       └── keygen.py       # Ed25519 keypair generation utility
├── tests/
│   └── test_pvsad.py       # Pytest suite verifying canonical invariance
├── requirements.txt        # Pinned dependency stack
└── .gitignore              # Security boundaries for local keys and environments
