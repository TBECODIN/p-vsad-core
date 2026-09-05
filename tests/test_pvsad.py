from src.pvsad.backend import canonicalize_and_hash

def test_canonical_hash_consistency():
    # Payload A and Payload B have identical data but reversed key order
    payload_a = {"status": "ok", "alpha": 100}
    payload_b = {"alpha": 100, "status": "ok"}
    
    hash_a = canonicalize_and_hash(payload_a)
    hash_b = canonicalize_and_hash(payload_b)
    
    # Assert that canonicalization forces the hashes to match exactly
    assert hash_a == hash_b, "Canonicalization failed: Hash mismatch on identical key sets!"
