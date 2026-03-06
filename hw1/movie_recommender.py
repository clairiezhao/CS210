from collections import defaultdict


# ===============================================================
#                 CLI: Movie Recommender System
# ===============================================================
def main():
    movie_to_genre = {}
    genre_to_movies = defaultdict(set)

    movie_ratings = defaultdict(list)
    user_ratings = defaultdict(list)

    movies_loaded = False
    ratings_loaded = False

    while True:
        print("\n===== Movie Recommender Menu =====")
        print("1) Load movies text file")
        print("2) Load ratings text file")
        print("3) Feature 1: Top N movies (overall)")
        print("4) Feature 2: Top N movies (in genre)")
        print("5) Test each function (Features 1–5)")
        print("6) Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            path = input("Enter movies file path: ").strip()
            movie_to_genre, genre_to_movies = load_movies(path)
            movies_loaded = True
            print(f"Loaded {len(movie_to_genre)} movies and {len(genre_to_movies)} genres.")

        elif choice == "2":
            path = input("Enter ratings file path: ").strip()
            movie_ratings, user_ratings = load_ratings(path)
            ratings_loaded = True
            print(f"Loaded ratings for {len(movie_ratings)} movies and {len(user_ratings)} users.")

        elif choice == "3":
            if not ratings_loaded:
                print("Load ratings first (option 2).")
                continue
            try:
                n = int(input("Enter N: ").strip())
                if n <= 0:
                    print("N must be a positive integer.")
                    continue
            except ValueError:
                print("Invalid input. Please enter an integer.")
                continue

            top_n_movies_overall(n, movie_ratings)


        elif choice == "4":
            if not movies_loaded:
                print("Load movies first (option 1).")
                continue
            if not ratings_loaded:
                print("Load ratings first (option 2).")
                continue
            genre = input("Enter genre (case-sensitive): ").strip()

            try:
                n = int(input("Enter N: ").strip())
                if n <= 0:
                    print("N must be a positive integer.")
                    continue
            except ValueError:
                print("Invalid input. Please enter an integer.")
                continue
            top_n_movies_in_genre(n, genre, genre_to_movies, movie_ratings)

        elif choice == "5":
            # Basic "test each function" menu action
            if not movies_loaded or not ratings_loaded:
                print("Load BOTH movies and ratings first (options 1 and 2).")
                continue

            print("\n--- Running Feature 1 sample ---")
            top_n_movies_overall(5, movie_ratings)

            print("\n--- Running Feature 2 sample ---")
            # pick first available genre to demo
            if genre_to_movies:
                sample_genre = next(iter(genre_to_movies.keys()))
                top_n_movies_in_genre(5, sample_genre, genre_to_movies, movie_ratings)
            else:
                print("No genres loaded.")

            print("\n--- Running Feature 3 sample ---")
            top_n_genres(3, movie_to_genre, genre_to_movies, movie_ratings)

            print("\n--- Running Feature 4 sample ---")
            if user_ratings:
                sample_user = next(iter(user_ratings.keys()))
                user_top_genre(sample_user, user_ratings, movie_to_genre)
            else:
                print("No users loaded.")

            print("\n--- Running Feature 5 sample ---")
            if user_ratings:
                sample_user = next(iter(user_ratings.keys()))
                recommend_top_3(sample_user, user_ratings, movie_to_genre, genre_to_movies, movie_ratings)
            else:
                print("No users loaded.")

        elif choice == "6":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


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
            
            genre = genre.lower()
            movie_name = movie_name.lower()

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

            movie_name = movie_name.lower()

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




# ===============================================================
#                           FEATURES
# ===============================================================


# ================================================================
# 1) Movie popularity based on average rating.
# ================================================================

def top_n_movies_overall(n, movie_ratings):
    """
    Feature 1: Top n movies ranked on average rating.
    Prints and returns list of tuples: [(movie_name, avg_rating, num_ratings), ...]
    """
    averages = []
    for movie, ratings in movie_ratings.items():
        if ratings:  # avoid divide by zero
            avg = sum(ratings) / len(ratings)
            averages.append((movie, avg, len(ratings)))

    # sort by avg desc, then by number of ratings desc, then name asc
    averages.sort(key=lambda x: (-x[1], -x[2], x[0]))

    print(f"\nTop {n} Movies by Average Rating")
    print("-" * 50)
    for i, (movie, avg, count) in enumerate(averages[:n], start=1):
        print(f"{i}. {movie:<30}  Avg: {avg:.2f}  Count: {count}")
    print()

    return averages[:n]


# ================================================================
# 2) Top n movies in a genre ranked on average rating.
# ================================================================

def top_n_movies_in_genre(n, genre, genre_to_movies, movie_ratings):
    """
    Feature 2: Top n movies in a genre ranked on average rating.
    Prints and returns list of tuples: [(movie_name, avg_rating, num_ratings), ...]
    """
    genre = genre.strip()

    if genre not in genre_to_movies:
        print(f"\nGenre '{genre}' not found.\n")
        return []

    candidates = []
    for movie in genre_to_movies[genre]:
        if movie in movie_ratings and movie_ratings[movie]:
            ratings = movie_ratings[movie]
            avg = sum(ratings) / len(ratings)
            candidates.append((movie, avg, len(ratings)))

    candidates.sort(key=lambda x: (-x[1], -x[2], x[0]))

    print(f"\nTop {n} Movies in Genre: {genre}")
    print("-" * 50)
    if not candidates:
        print("No rated movies found in this genre.\n")
        return []

    for i, (movie, avg, count) in enumerate(candidates[:n], start=1):
        print(f"{i}. {movie:<30}  Avg: {avg:.2f}  Count: {count}")
    print()

    return candidates[:n]

# ================================================================
# 3) Top n genres with highest average of average movie ratings
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
# 4) User's highest-rated genre (based on user's ratings only)
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
# 5) Top 3 unrated movies from user's top genre
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