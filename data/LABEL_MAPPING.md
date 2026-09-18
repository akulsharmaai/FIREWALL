# LABEL MAPPING & PSYCHOLOGICAL TARGET RULES

## 1. Primary Binary Label (`manipulation_detected`)
- `1`: Digital/Behavioral manipulation, deceptive UI copy, clickbait attention traps, or persuasive web rhetoric.
- `0`: Non-manipulative, standard, informative, benign UI copy, news headlines, or abstract/academic non-persuasive text.

---

## 2. Secondary Class Mapping (`manipulation_type`)

| Original Source Category / Pattern | Standardized `manipulation_type` | Description & Scope |
| :--- | :--- | :--- |
| `Not Dark Pattern`, `0` (Clickbait/News), Academic Logic Examples | `none` | Standard informative text, news headlines, UI labels, or non-persuasive text. |
| `Scarcity` | `artificial_scarcity` | Fabricated inventory limits ("Only 2 left!"). |
| `Urgency` | `urgency` | Artificial time constraints ("Sale ends in 05:00"). |
| `Social Proof`, `ad populum` (digital) | `social_pressure` | Peer pressure, popularity cues ("89 people viewing this"). |
| `Misdirection`, `Forced Action`, `GuiltyFeeds (0)` | `deceptive_choice` | Confirmshaming, pre-selected options, deceptive choices. |
| `Obstruction`, `Sneaking` | `dark_pattern` | Hidden costs, forced continuity, subscription traps. |
| `clickbait (1)` | `clickbait` | Sensationalized headline designed to trigger curiosity gaps. |
| Digital rhetoric targeting emotions | `emotional_manipulation` | Manipulative copy targeting fear, guilt, or personal attack. |
| Digital/Commercial persuasion slogans | `general_persuasion` | Fallacious logic or persuasive web copy designed to influence behavior. |

---

## 3. Psychological Target Rules (`psychological_target`)

> [!NOTE]
> `psychological_target` is treated strictly as a secondary heuristic label and must NEVER be used as the primary ML training target.

| `manipulation_type` | Mapped `psychological_target` | Rationale |
| :--- | :--- | :--- |
| `artificial_scarcity` | `fomo` | Triggers Fear Of Missing Out. |
| `urgency` | `loss_aversion` | Triggers anxiety of losing a deal or opportunity. |
| `social_pressure` | `social_conformity` | Leverages crowd behavior and social proof. |
| `clickbait` | `curiosity_gap` | Exploits informational gaps to force clicks. |
| `emotional_manipulation` | `fear_guilt_empathy` | Targets emotional vulnerabilities. |
| `deceptive_choice` (Confirmshaming) | `guilt_shame` | Shames user for declining ("No thanks, I like paying full price"). |
| `general_persuasion` | `authority_trust` | Leverages authority, slogans, or persuasive claims. |
| `none` / Unmapped | `unknown` | Preserves annotation integrity without guessing. |
