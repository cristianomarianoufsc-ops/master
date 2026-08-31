# Runtime C280 code-to-glyph map

This report uses a runtime capture, not the heuristic D12x expansion.
A code is accepted when `C280[code]` is non-zero; the text loop then
uses that same code as the glyph selector.

- capture result: `step_limit` at PC `0x406F`
- C280 non-zero entries: **20**
- streams scanned: **260**
- source: bank `13`, CPU `0xAD0C`, stride `0x10`
- transformed stride after 05B3E model: `0x80`

| Code | C280 value | Glyph index | Source offset | Transformed offset | Stream occurrences |
|---:|---:|---:|---:|---:|---:|
| `0x40` | `0x01` | `64` | `0x0400` | `0x2000` | 51 |
| `0x41` | `0x01` | `65` | `0x0410` | `0x2080` | 0 |
| `0x42` | `0x01` | `66` | `0x0420` | `0x2100` | 93 |
| `0x43` | `0x01` | `67` | `0x0430` | `0x2180` | 21 |
| `0x44` | `0x01` | `68` | `0x0440` | `0x2200` | 61 |
| `0x45` | `0x01` | `69` | `0x0450` | `0x2280` | 100 |
| `0x46` | `0x01` | `70` | `0x0460` | `0x2300` | 109 |
| `0x47` | `0x01` | `71` | `0x0470` | `0x2380` | 18 |
| `0x48` | `0x01` | `72` | `0x0480` | `0x2400` | 443 |
| `0x49` | `0x01` | `73` | `0x0490` | `0x2480` | 0 |
| `0x4A` | `0x01` | `74` | `0x04A0` | `0x2500` | 162 |
| `0x4B` | `0x01` | `75` | `0x04B0` | `0x2580` | 58 |
| `0x4C` | `0x01` | `76` | `0x04C0` | `0x2600` | 97 |
| `0x4D` | `0x01` | `77` | `0x04D0` | `0x2680` | 0 |
| `0x4E` | `0x01` | `78` | `0x04E0` | `0x2700` | 175 |
| `0x4F` | `0x01` | `79` | `0x04F0` | `0x2780` | 27 |
| `0x89` | `0x01` | `137` | `0x0890` | `0x4480` | 243 |
| `0xA9` | `0x01` | `169` | `0x0A90` | `0x5480` | 388 |
| `0xC9` | `0x01` | `201` | `0x0C90` | `0x6480` | 0 |
| `0xE9` | `0x01` | `233` | `0x0E90` | `0x7480` | 143 |

## Interpretation limits

The capture stopped before the dialogue breakpoint, so this map is a
runtime snapshot of the current execution path, not yet the final game-wide
C280 table. Stream occurrence counts are structural cross-references and
do not prove that a stream is narrative text.
