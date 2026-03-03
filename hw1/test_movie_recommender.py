####
#
# Automatic testing script for movie_recommender.py
#
# Run with:
#     python test_movie_recommender.py
#
# This script:
# 1. Creates controlled test input files
# 2. Loads the data
# 3. Calls all 5 required features
# 4. Compares results with expected values
# 5. Prints PASS / FAIL results
#
####

from movie_recommender import (
    load_movies,
    load_ratings,
    top_n_movies_overall,
    top_n_movies_in_genre,
    top_n_genres,
    user_top_genre,
    recommend_top_3,
)

# =======================================================
#              CREATE CONTROLLED DATASET #1
# =======================================================

def create_test_dataset_one():
    movies_data = [
        "Action|1|Die Hard (1988)",
        "Drama|2|Forrest Gump (1994)",
        "Comedy|3|The Mask (1994)",
        "Comedy|4|Ace Ventura (1994)"
    ]

    ratings_data = [
        "Die Hard (1988)|5|101",
        "Die Hard (1988)|4|102",
        "Forrest Gump (1994)|5|101",
        "Forrest Gump (1994)|4|103",
        "The Mask (1994)|3|101",
        "Ace Ventura (1994)|4|104"
    ]

    with open("test_movies.txt", "w", encoding="utf-8") as f:
        for line in movies_data:
            f.write(line + "\n")

    with open("test_ratings.txt", "w", encoding="utf-8") as f:
        for line in ratings_data:
            f.write(line + "\n")


# =======================================================
#              CREATE CONTROLLED DATASET #2
# =======================================================

def create_test_dataset_two():
    movies_data = [
        "Action|1|The Dark Knight (2008)",
        "Sci-Fi|2|Interstellar (2014)",
        "Thriller|3|Inception (2010)"
    ]

    ratings_data = [
        "The Dark Knight (2008)|5|201",
        "The Dark Knight (2008)|5|202",
        "Interstellar (2014)|4|201",
        "Inception (2010)|5|203"
    ]

    with open("nolan_movies.txt", "w", encoding="utf-8") as f:
        for line in movies_data:
            f.write(line + "\n")

    with open("nolan_ratings.txt", "w", encoding="utf-8") as f:
        for line in ratings_data:
            f.write(line + "\n")


# =======================================================
#                   RUN TESTS FUNCTION
# =======================================================

def run_tests(movies_file, ratings_file, expected, dataset_name):
    print(f"\n===== Running Tests for {dataset_name} =====\n")

    movie_to_genre, genre_to_movies = load_movies(movies_file)
    movie_ratings, user_ratings = load_ratings(ratings_file)

    # -------------------------------------------------------
    # Feature 1
    # -------------------------------------------------------
    result1 = top_n_movies_overall(1, movie_ratings)

    print("Feature 1 (Top Movie Overall): ", end="")
    if result1 and result1[0][0] == expected["feature1"]:
        print("PASS")
    else:
        print("FAIL")

    # -------------------------------------------------------
    # Feature 2
    # -------------------------------------------------------
    result2 = top_n_movies_in_genre(1, expected["genre_test"], genre_to_movies, movie_ratings)

    print("Feature 2 (Top Movie in Genre): ", end="")
    if result2 and result2[0][0] == expected["feature2"]:
        print("PASS")
    else:
        print("FAIL")

    # -------------------------------------------------------
    # Feature 3
    # -------------------------------------------------------
    result3 = top_n_genres(1, movie_to_genre, genre_to_movies, movie_ratings)

    print("Feature 3 (Top Genre): ", end="")
    if result3 and result3[0][0] == expected["feature3"]:
        print("PASS")
    else:
        print("FAIL")

    # -------------------------------------------------------
    # Feature 4
    # -------------------------------------------------------
    result4 = user_top_genre(expected["user_test"], user_ratings, movie_to_genre)

    print("Feature 4 (User Top Genre): ", end="")
    if result4 == expected["feature4"]:
        print("PASS")
    else:
        print("FAIL")

    # -------------------------------------------------------
    # Feature 5
    # -------------------------------------------------------
    result5 = recommend_top_3(
        expected["user_test"],
        user_ratings,
        movie_to_genre,
        genre_to_movies,
        movie_ratings
    )

    print("Feature 5 (Recommend Top 3): ", end="")
    if isinstance(result5, list):
        print("PASS")
    else:
        print("FAIL")

    print("\n===== Testing Complete =====\n")


# =======================================================
#                    MAIN EXECUTION
# =======================================================

if __name__ == "__main__":

    # Create both datasets
    create_test_dataset_one()
    create_test_dataset_two()

    # Expected values for Dataset #1
    expected_dataset_one = {
        "feature1": "Die Hard (1988)",
        "feature2": "Forrest Gump (1994)",
        "feature3": "Action",
        "feature4": "Action",
        "genre_test": "Drama",
        "user_test": 101
    }

    # Expected values for Dataset #2
    expected_dataset_two = {
        "feature1": "The Dark Knight (2008)",
        "feature2": "Interstellar (2014)",
        "feature3": "Action",
        "feature4": "Action",
        "genre_test": "Sci-Fi",
        "user_test": 201
    }

    run_tests("test_movies.txt", "test_ratings.txt", expected_dataset_one, "Dataset #1")
    run_tests("nolan_movies.txt", "nolan_ratings.txt", expected_dataset_two, "Dataset #2")
