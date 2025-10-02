# Challenge: Date Sanity (08 Apr 2025)

Goal: show vendor UIs mis-handle dates (“in the future”) while the PB2S server never ships that error. use SPECIFICATION/pb2s_v0.2.1_spec.md

## Steps (reproducible)
1. Open vendor guest UI, ask: **“What happened on 8 April 2025?”**
2. Save screenshot with visible clock → `docs/challenges/vendor_qwen_YYYYMMDD_HHMM.png`
3. Call **our** `/chat` with the same prompt; save raw JSON response as  
   `docs/challenges/our_pb2s_response_YYYYMMDD_HHMM.json`
4. Verify locally:
   ```bash
   python scripts/verify_time_guard.py --file docs/challenges/our_pb2s_response_YYYYMMDD_HHMM.json
