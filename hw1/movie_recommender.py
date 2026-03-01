from collections import defaultdict

def main():
    pass

from collections import defaultdict

def load_movies(movie_file):
    """
    Returns:
        movie_to_genre: {movie_name: genre}
        genre_to_movies: {genre: set(movie_names)}
    """
    movie_to_genre = {}
    genre_to_movies = defaultdict(set)

    with open(movie_file, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            parts = line.split("|")

            # Validate correct number of fields
            if len(parts) != 3:
                print(f"Warning (movies.txt line {line_number}): "
                      f"Invalid format → {line}")
                continue

            genre, movie_id, movie_name = [p.strip() for p in parts]

            # Validate required fields are not empty
            if not genre or not movie_name:
                print(f"Warning (movies.txt line {line_number}): "
                      f"Missing genre or movie name → {line}")
                continue

            # Check for duplicate movie definitions
            if movie_name in movie_to_genre:
                print(f"Warning (movies.txt line {line_number}): "
                      f"Duplicate movie entry → {movie_name}")
                continue

            movie_to_genre[movie_name] = genre
            genre_to_movies[genre].add(movie_name)

    return movie_to_genre, genre_to_movies


def load_ratings(rating_file):
    """
    Returns:
        movie_ratings: {movie_name: [ratings]}
        user_ratings: {user_id: [(movie_name, rating)]}
    """
    movie_ratings = defaultdict(list)
    user_ratings = defaultdict(list)

    with open(rating_file, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            # Skip empty lines
            if not line:
                continue

            parts = line.split("|")

            # Validate correct number of fields
            if len(parts) != 3:
                print(f"Warning (ratings.txt line {line_number}): "
                      f"Invalid format → {line}")
                continue

            movie_name, rating_str, user_id_str = [p.strip() for p in parts]

            # Validate rating
            try:
                rating = float(rating_str)
            except ValueError:
                print(f"Warning (ratings.txt line {line_number}): "
                      f"Invalid rating → {rating_str}")
                continue

            # Validate user_id
            try:
                user_id = int(user_id_str)
            except ValueError:
                print(f"Warning (ratings.txt line {line_number}): "
                      f"Invalid user ID → {user_id_str}")
                continue

            # Optional: validate rating range (example: 0–5)
            if rating < 0 or rating > 5:
                print(f"Warning (ratings.txt line {line_number}): "
                      f"Rating out of range → {rating}")
                continue

            movie_ratings[movie_name].append(rating)
            user_ratings[user_id].append((movie_name, rating))

    return movie_ratings, user_ratings


# ---------- Helper Functions ----------

def compute_movie_average_ratings(movie_ratings):
    """
    Returns:
        {movie_name: average_rating}
    """
    return {
        movie: sum(ratings) / len(ratings)
        for movie, ratings in movie_ratings.items()
    }


def compute_genre_average_of_averages(movie_avg, movie_to_genre):
    """
    Returns:
        {genre: average_of_movie_averages}
    """
    genre_ratings = defaultdict(list)

    for movie, avg in movie_avg.items():
        genre = movie_to_genre.get(movie)
        if genre:
            genre_ratings[genre].append(avg)

    return {
        genre: sum(avgs) / len(avgs)
        for genre, avgs in genre_ratings.items()
    }


# ================================================================
# 1) Top n genres with highest average of average movie ratings
# ================================================================

def top_n_genres(n, movie_to_genre, genre_to_movies, movie_ratings):
    movie_avg = compute_movie_average_ratings(movie_ratings)
    genre_avg = compute_genre_average_of_averages(movie_avg, movie_to_genre)

    sorted_genres = sorted(
        genre_avg.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # ---- PRINT OUTPUT ----
    print(f"\nTop {n} Genres by Average Rating")
    print("-" * 40)
    for i, (genre, avg) in enumerate(sorted_genres[:n], start=1):
        print(f"{i}. {genre:<15}  Average Rating: {avg:.2f}")
    print()

    # ---- RETURN ORIGINAL RESULT ----
    return sorted_genres[:n]


# ================================================================
# 2) User's highest-rated genre (based on user's ratings only)
# ================================================================

def user_top_genre(user_id, user_ratings, movie_to_genre):
    if user_id not in user_ratings:
        print(f"\nUser {user_id} has not rated any movies.\n")
        return None

    genre_ratings = defaultdict(list)

    for movie, rating in user_ratings[user_id]:
        genre = movie_to_genre.get(movie)
        if genre:
            genre_ratings[genre].append(rating)

    if not genre_ratings:
        print(f"\nUser {user_id} has no valid genre ratings.\n")
        return None

    genre_avg = {
        genre: sum(ratings) / len(ratings)
        for genre, ratings in genre_ratings.items()
    }

    top_genre, top_avg = max(genre_avg.items(), key=lambda x: x[1])

    # ---- PRINT OUTPUT ----
    print(f"\nUser {user_id}'s Top Genre")
    print("-" * 40)
    print(f"Genre: {top_genre}")
    print(f"Average Rating Given: {top_avg:.2f}\n")

    # ---- RETURN ORIGINAL RESULT ----
    return top_genre


# ================================================================
# 3) Top 3 unrated movies from user's top genre
# ================================================================

def recommend_top_3(user_id, user_ratings, movie_to_genre,
                    genre_to_movies, movie_ratings):

    top_genre = user_top_genre(user_id, user_ratings, movie_to_genre)
    if not top_genre:
        return []

    movie_avg = compute_movie_average_ratings(movie_ratings)

    rated_movies = {movie for movie, _ in user_ratings[user_id]}

    candidates = [
        movie for movie in genre_to_movies[top_genre]
        if movie not in rated_movies and movie in movie_avg
    ]

    sorted_candidates = sorted(
        candidates,
        key=lambda m: movie_avg[m],
        reverse=True
    )

    top_3 = sorted_candidates[:3]

    # ---- PRINT OUTPUT ----
    print(f"\nTop 3 Recommendations for User {user_id}")
    print(f"(From favorite genre: {top_genre})")
    print("-" * 40)

    if not top_3:
        print("No available recommendations.\n")
    else:
        for i, movie in enumerate(top_3, start=1):
            print(f"{i}. {movie:<25}  Average Rating: {movie_avg[movie]:.2f}")
        print()

    # ---- RETURN ORIGINAL RESULT ----
    return top_3

if __name__ == '__main__':
    main()