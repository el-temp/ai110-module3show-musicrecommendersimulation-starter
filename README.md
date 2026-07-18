# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

## Response:
To recomend songs the system will use genre, mood, energy, and accousticness.

The user profile stores information for favorite genre, favorite mood, target energy, and a boolean for if they like accoustics which can be used as a benchmark for recomendation.

For the text comparison like mood and energy points will be added if they match. Since accousticness is only stored as a boolean if that is set to true then the accoustincess will simply be added and if it is false it won't be added at all or maybe even subtracted. For energy point will be calculated as adding 1 -|energy-target energy|.

Songs that score higher points will be recomended first.

This system may result in too much bias being focused on genre and mood(could potentially be remedied by having user rank which metric they value more )
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

### Profile 1: High-Energy Pop

`{'favorite_genre': 'pop', 'favorite_mood': 'happy', 'target_energy': 0.9, 'likes_acoustic': False}`

```
1. Sunrise City by Neon Echo — Score: 5.74
   - genre match (+2.0)
   - mood match (+2.0)
   - energy closeness (+0.9)
   - non-acoustic match (+0.8)

2. Gym Hero by Max Pulse — Score: 3.92
   - genre match (+2.0)
   - energy closeness (+1.0)
   - non-acoustic match (+0.9)

3. Rooftop Lights by Indigo Parade — Score: 3.51
   - mood match (+2.0)
   - energy closeness (+0.9)
   - non-acoustic match (+0.7)

4. Iron Fists by Grey Anvil — Score: 1.90
   - energy closeness (+0.9)
   - non-acoustic match (+1.0)

5. City Pulse by DJ Solstice — Score: 1.90
   - energy closeness (+1.0)
   - non-acoustic match (+0.9)
```

### Profile 2: Chill Lofi

`{'favorite_genre': 'lofi', 'favorite_mood': 'chill', 'target_energy': 0.3, 'likes_acoustic': True}`

```
1. Library Rain by Paper Lanterns — Score: 5.81
   - genre match (+2.0)
   - mood match (+2.0)
   - energy closeness (+0.9)
   - acoustic match (+0.9)

2. Midnight Coding by LoRoom — Score: 5.59
   - genre match (+2.0)
   - mood match (+2.0)
   - energy closeness (+0.9)
   - acoustic match (+0.7)

3. Spacewalk Thoughts by Orbit Bloom — Score: 3.90
   - mood match (+2.0)
   - energy closeness (+1.0)
   - acoustic match (+0.9)

4. Focus Flow by LoRoom — Score: 3.68
   - genre match (+2.0)
   - energy closeness (+0.9)
   - acoustic match (+0.8)

5. Golden Hour Drive by Vinyl Static — Score: 1.95
   - energy closeness (+1.0)
   - acoustic match (+0.9)
```

### Profile 3: Deep Intense Rock

`{'favorite_genre': 'rock', 'favorite_mood': 'intense', 'target_energy': 0.85, 'likes_acoustic': False}`

```
1. Storm Runner by Voltline — Score: 5.84
   - genre match (+2.0)
   - mood match (+2.0)
   - energy closeness (+0.9)
   - non-acoustic match (+0.9)

2. Gym Hero by Max Pulse — Score: 3.87
   - mood match (+2.0)
   - energy closeness (+0.9)
   - non-acoustic match (+0.9)

3. City Pulse by DJ Solstice — Score: 1.89
   - energy closeness (+1.0)
   - non-acoustic match (+0.9)

4. Iron Fists by Grey Anvil — Score: 1.85
   - energy closeness (+0.9)
   - non-acoustic match (+1.0)

5. Sunrise City by Neon Echo — Score: 1.79
   - energy closeness (+1.0)
   - non-acoustic match (+0.8)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

### Weight Experiment: Double Energy, Halve Genre

As a temporary experiment, `score_song` in `recommender.py` was changed so that:

- genre match: `+2.0` → `+1.0` (halved)
- energy closeness: `1 - abs(diff)` → `(1 - abs(diff)) * 2` (doubled, max `+2.0`)

`main.py` was re-run against all six profiles with these new weights. Selected before/after comparisons:

**High-Energy Pop** — rank order changed: "Gym Hero" (genre-only match) dropped from #2 to #3, displaced by "Rooftop Lights" (mood-only match), because losing a point of genre weight let a mood match edge it out. "Storm Runner" and "City Pulse" (energy-only matches) climbed into the top 5 (2.88 each) on the strength of near-perfect energy closeness alone.

**Deep Intense Rock** — "Iron Fists" fell out of the top 5 entirely, replaced by "Sunrise City," since Iron Fists had been relying on close energy + non-acoustic match without any genre/mood match, and doubling energy wasn't enough to keep it ahead once other pure-energy matches also got the same boost.

**Adversarial: Extreme Energy + Acoustic Conflict** — "Iron Fists" still wins by a wide margin (4.97 vs. 1.92 for #2), but the gap shrank from roughly 4x to roughly 2.6x. Doubling energy weight raised everyone's energy-closeness contribution roughly equally, so it didn't meaningfully rebalance the genre+mood-vs-acousticness conflict — Iron Fists's categorical bonuses (genre 1.0 + mood 2.0 = 3.0) still dwarf the acoustic penalty it incurs (0.0 instead of up to 1.0).

**Conclusion: different, not more accurate.** This reweighting didn't fix any of the underlying issues found in the adversarial testing — it just shifted which songs win in close calls. Pure energy-matches now rank higher relative to pure genre-matches (arguably reasonable, since energy is a continuous/precise signal and genre is a coarse binary one), but the core problem — that additive categorical bonuses can still swamp a fully-failed continuous preference — persists. Whether this reweighting counts as "more accurate" depends entirely on which axis a real user weights more heavily in their own head, which the system has no way to learn; it's a different tradeoff, not a strictly better one. The weight change was reverted back to the original values (genre `+2.0`, energy `1 - abs(diff)`) after this experiment.

### Adversarial / Edge Case Profiles

To stress-test the scoring logic, I ran profiles with internally conflicting preferences to see whether the system would produce misleading or nonsensical "confident" recommendations.

#### Adversarial Profile 1: High Energy + Sad Mood

`{'favorite_genre': 'pop', 'favorite_mood': 'sad', 'target_energy': 0.9, 'likes_acoustic': False}` — conflicting because high-energy songs in this catalog are almost never tagged "sad."

```
1. Gym Hero by Max Pulse — Score: 3.92
   - genre match (+2.0)
   - energy closeness (+1.0)
   - non-acoustic match (+0.9)

2. Sunrise City by Neon Echo — Score: 3.74
   - genre match (+2.0)
   - energy closeness (+0.9)
   - non-acoustic match (+0.8)

3. Iron Fists by Grey Anvil — Score: 1.90
   - energy closeness (+0.9)
   - non-acoustic match (+1.0)

4. City Pulse by DJ Solstice — Score: 1.90
   - energy closeness (+1.0)
   - non-acoustic match (+0.9)

5. Storm Runner by Voltline — Score: 1.89
   - energy closeness (+1.0)
   - non-acoustic match (+0.9)
```

**Observation:** No song in the catalog has mood "sad," so the mood match bonus never fires for anyone. The system silently falls back to genre + energy + acousticness and never signals that "sad" was an impossible target — it just quietly ignores that preference. This isn't really "tricked," but it reveals that unmatched categorical preferences fail silently instead of surfacing a warning to the user.

#### Adversarial Profile 2: Nonexistent Genre

`{'favorite_genre': 'polka', 'favorite_mood': 'happy', 'target_energy': 0.5, 'likes_acoustic': False}` — genre doesn't exist in the catalog at all.

```
1. Sunrise City by Neon Echo — Score: 3.50
   - mood match (+2.0)
   - energy closeness (+0.7)
   - non-acoustic match (+0.8)

2. Rooftop Lights by Indigo Parade — Score: 3.39
   - mood match (+2.0)
   - energy closeness (+0.7)
   - non-acoustic match (+0.7)

3. Backyard Games by Kidcore Kingdom — Score: 1.67
   - energy closeness (+0.8)
   - non-acoustic match (+0.8)

4. Slow Burn by Velvet Aria — Score: 1.55
   - energy closeness (+0.9)
   - non-acoustic match (+0.6)

5. City Pulse by DJ Solstice — Score: 1.54
   - energy closeness (+0.6)
   - non-acoustic match (+0.9)
```

**Observation:** Same failure mode as above — an impossible genre just means the +2.0 genre bonus never applies to anyone, so the system quietly recommends based on mood/energy/acousticness alone. The recommender never detects or reports that "polka" isn't a real option; it degrades gracefully but silently, which could mislead a user into thinking the recommendations reflect their genre preference when they don't at all.

#### Adversarial Profile 3: Extreme Energy + Acoustic Conflict

`{'favorite_genre': 'metal', 'favorite_mood': 'angry', 'target_energy': 1.0, 'likes_acoustic': True}` — asks for maximum energy (metal/angry) *and* strong acoustic preference, which are contradictory in this catalog (the metal/angry song is the least acoustic track available).

```
1. Iron Fists by Grey Anvil — Score: 5.00
   - genre match (+2.0)
   - mood match (+2.0)
   - energy closeness (+1.0)
   - acoustic match (+0.0)

2. Coffee Shop Stories by Slow Stereo — Score: 1.26
   - energy closeness (+0.4)
   - acoustic match (+0.9)

3. Golden Hour Drive by Vinyl Static — Score: 1.25
   - energy closeness (+0.3)
   - acoustic match (+0.9)

4. Library Rain by Paper Lanterns — Score: 1.21
   - energy closeness (+0.3)
   - acoustic match (+0.9)

5. Spacewalk Thoughts by Orbit Bloom — Score: 1.20
   - energy closeness (+0.3)
   - acoustic match (+0.9)
```

**Observation:** This is the most interesting case. Even though the user asked for `likes_acoustic: True`, "Iron Fists" wins by a wide margin (5.00 vs 1.26) purely because it perfectly matches genre and mood while completely failing the acoustic preference (acoustic score of 0.0, the worst possible). Meanwhile, songs #2–5 satisfy the acoustic preference well (+0.9) but score far lower overall because they miss genre/mood. This exposes a real weight-balance issue: the additive scoring lets two +2.0 categorical bonuses (genre + mood, worth 4.0 combined) completely dominate and mask a total failure on another axis (acousticness, worth at most 1.0). A user with truly conflicting preferences gets a recommendation that satisfies only part of what they asked for, with no indication that a tradeoff was made.

### Summary of what the adversarial testing revealed

- Unmatched categorical preferences (a mood or genre that doesn't exist in the catalog) fail silently — the corresponding bonus just never applies, with no feedback to the user.
- The additive scoring model lets high-weight categorical matches (genre +2.0, mood +2.0) drown out a complete failure on a lower-weight continuous preference (acousticness, max +1.0), so conflicting preferences resolve in favor of whichever axis has more available point-weight rather than a balanced compromise.
- The system never flags contradictions in the input itself (e.g., high energy + "sad" mood, or high energy + acoustic) — it just scores whatever combination it's given.

---

## Limitations and Risks

- It only works on a tiny catalog (17 songs).
- It does not understand lyrics or language.
- **Energy "dead zones" underserve moderate-energy users.** The catalog's energy values cluster into a low band (0.28–0.45) and a high band (0.75–0.97), with gaps of 0.10–0.13 in the middle (only 2 songs sit between 0.45 and 0.75). A user targeting `energy=0.6` can never score as well on the energy axis as a user targeting `0.3` or `0.9`, purely because of catalog density — the system never flags this, so it presents a structurally worse recommendation with the same confidence as a well-matched one.
- **Genre/mood matching is exact-string and binary, which reinforces filter bubbles.** 12 of 14 genres and 9 of 13 moods appear only once in the catalog, and there's no notion of genre/mood *similarity* (`"pop"`, `"indie pop"`, and `"dream pop"` are totally unrelated to the scorer). A niche-taste user gets at most one song that can ever earn the genre/mood bonus, and the system never surfaces adjacent styles as a bridge — it only ever reinforces the exact label a user typed, never nudges them toward related music.
- **Categorical bonuses (genre +2, mood +2) outweigh continuous features (energy, acousticness, each capped at +1).** This means two label matches will beat a perfect audio-feature match almost every time (confirmed in testing: a song with 0% acoustic match against an acoustic-loving user's stated preference still won by a wide margin because it matched genre + mood). Users whose taste is really about *feel* rather than a genre/mood tag are structurally shortchanged.
- **Small-catalog artist concentration compounds the genre bias.** Two artists ("Neon Echo," "LoRoom") each have 2 of the catalog's 17 songs; for the 3-song "lofi" genre, that means one artist supplies two-thirds of the recommendations for anyone who likes lofi.
- **No diversity or exploration mechanism.** Scoring is fully deterministic, so a given profile always returns the exact same top 5, with no randomness or "you might also like" cross-genre logic — this is a textbook filter bubble: stated preferences are reinforced, never challenged or broadened.
- **Unmatched/impossible preferences fail silently** (see Experiments section) — a genre or mood that doesn't exist in the catalog just contributes nothing to the score, with no warning to the user that part of their profile was ignored.

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



