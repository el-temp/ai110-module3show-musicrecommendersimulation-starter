"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

# Three distinct user preference profiles, plus adversarial / edge case
# profiles designed to see if the scoring logic can be "tricked" or
# produces unexpected results.
PROFILES = {
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.3,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.85,
        "likes_acoustic": False,
    },
    # Adversarial / edge case profiles
    "Adversarial: High Energy + Sad Mood": {
        "favorite_genre": "pop",
        "favorite_mood": "sad",
        "target_energy": 0.9,
        "likes_acoustic": False,
    },
    "Adversarial: Nonexistent Genre": {
        "favorite_genre": "polka",
        "favorite_mood": "happy",
        "target_energy": 0.5,
        "likes_acoustic": False,
    },
    "Adversarial: Extreme Energy + Acoustic Conflict": {
        "favorite_genre": "metal",
        "favorite_mood": "angry",
        "target_energy": 1.0,
        "likes_acoustic": True,
    },
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, user_prefs in PROFILES.items():
        print("=" * 60)
        print(f"PROFILE: {name}")
        print(f"Preferences: {user_prefs}")
        print("=" * 60)

        recommendations = recommend_songs(user_prefs, songs, k=5)

        print("\nTop recommendations:\n")
        for rank, (song, score, reasons) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} by {song['artist']} — Score: {score:.2f}")
            for reason in reasons:
                print(f"   - {reason}")
            print()


if __name__ == "__main__":
    main()
