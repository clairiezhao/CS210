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

    with open("test_movies2.txt", "w", encoding="utf-8") as f:
        for line in movies_data:
            f.write(line + "\n")

    with open("test_ratings2.txt", "w", encoding="utf-8") as f:
        for line in ratings_data:
            f.write(line + "\n")


# =======================================================
#              CREATE CONTROLLED DATASET #3
# =======================================================

def create_test_dataset_three():
    movies_data = [
        "Action|1|Mad Max (1979)",
        "Drama|2|The Shawshank Redemption (1994)",
        "Comedy|3|Superbad (2007)"
    ]

    ratings_data = [
        "Mad Max (1979)|4|101",
        "Mad Max (1979)|5|102"
    ]

    with open("test_movies3.txt", "w", encoding="utf-8") as f:
        for line in movies_data:
            f.write(line + "\n")
    
    with open("test_ratings3.txt", "w", encoding="utf-8") as f:
        for line in ratings_data:
            f.write(line + "\n")


# =======================================================
#              CREATE CONTROLLED DATASET #4
# =======================================================

def create_test_dataset_four():
    movies_data = [
        "Action|1|Avatar (2009)",
        "Action|2|Batman Begins (2005)"
    ]

    ratings_data = [
        "Avatar (2009)|4|1",
        "Avatar (2009)|4|2",
        "Batman Begins (2005)|4|3",
        "Batman Begins (2005)|4|4"
    ]

    with open("test_movies4.txt", "w", encoding="utf-8") as f:
        for line in movies_data:
            f.write(line + "\n")
    
    with open("test_ratings4.txt", "w", encoding="utf-8") as f:
        for line in ratings_data:
            f.write(line + "\n")



# =======================================================
#              CREATE CONTROLLED DATASET #5
# =======================================================

def create_test_dataset_five():
    movies_data = [
        "Sci-Fi|1|Inception (2010)",
        "Sci-Fi|2|Interstellar (2014)",
        "Sci-Fi|3|Tenet (2020)"
    ]

    ratings_data = [
        "Inception (2010)|5|300",
        "Interstellar (2014)|4|300",
        "Tenet (2020)|5|300"
    ]

    with open("test_movies5.txt", "w", encoding="utf-8") as f:
        for line in movies_data:
            f.write(line + "\n")
    
    with open("test_ratings5.txt", "w", encoding="utf-8") as f:
        for line in ratings_data:
            f.write(line + "\n")


# =======================================================
#              CREATE CONTROLLED DATASET #6
# =======================================================

def create_test_dataset_six():
    movies_data = [
        "Action|1|Die Hard (1988)",
        "Action|2|Mad Max (1979)",
        "Drama|3|Forrest Gump (1994)",
        "Comedy|4|Step Brothers (2008)",
        "Comedy|5|Superbad (2007)",
        "Sci-Fi|6|Interstellar (2014)",
        "Thriller|7|The Prestige (2006)",
        "Horror|8|The Shining (1980)",
        "Horror|9|The Conjuring (2013)"
    ]

    ratings_data = [
        "Die Hard (1988)|5|101",
        "Die Hard (1988)|4|102",
        "Mad Max (1979)|5|103",
        "Forrest Gump (1994)|5|101",
        "Forrest Gump (1994)|5|104",
        "Step Brothers (2008)|3|101",
        "Superbad (2007)|3|102",
        "Interstellar (2014)|4|105",
        "The Prestige (2006)|5|106",
        "The Prestige (2006)|5|107",
        "The Conjuring (2013)|4|108"
    ]

    with open("test_movies6.txt", "w", encoding="utf-8") as f:
        for line in movies_data:
            f.write(line + "\n")
    
    with open("test_ratings6.txt", "w", encoding="utf-8") as f:
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
    n = expected["n_value"]

    result1 = top_n_movies_overall(n, movie_ratings)

    print("Feature 1 (Top Movie Overall): ", end="")
    if result1 and result1[0][0] == expected["feature1"]:
        print("PASS")
    else:
        print("FAIL")

    # -------------------------------------------------------
    # Feature 2
    # -------------------------------------------------------
    result2 = top_n_movies_in_genre(n, expected["genre_test"], genre_to_movies, movie_ratings)

    print("Feature 2 (Top Movie in Genre): ", end="")
    if result2 and result2[0][0] == expected["feature2"]:
        print("PASS")
    else:
        print("FAIL")

    # -------------------------------------------------------
    # Feature 3
    # -------------------------------------------------------
    result3 = top_n_genres(n, movie_to_genre, genre_to_movies, movie_ratings)

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
    create_test_dataset_three()
    create_test_dataset_four()
    create_test_dataset_five()
    create_test_dataset_six()

    # Expected values for Dataset #1
    expected_dataset_one = {
        "feature1": "die hard (1988)",
        "feature2": "forrest gump (1994)",
        "feature3": "action",
        "feature4": "action",
        "genre_test": "drama",
        "user_test": 101,
        "n_value": 1
    }

    # Expected values for Dataset #2
    expected_dataset_two = {
        "feature1": "the dark knight (2008)",
        "feature2": "interstellar (2014)",
        "feature3": "action",
        "feature4": "action",
        "genre_test": "sci-fi",
        "user_test": 201,
        "n_value": 2
    }

    # Expected values for Dataset #3
    expected_dataset_three = {
        "feature1": "mad max (1979)",
        "feature2": "mad max (1979)",
        "feature3": "action",
        "feature4": "action",
        "genre_test": "action",
        "user_test": 101,
        "n_value": 2
    }

    # Expected values for Dataset #4
    expected_dataset_four = {
        "feature1": "avatar (2009)",
        "feature2": "avatar (2009)",
        "feature3": "action",
        "feature4": "action",
        "genre_test": "action",
        "user_test": 1,
        "n_value": 2
    }

    # Expected values for Dataset #5
    expected_dataset_five= {
        "feature1": "inception (2010)",
        "feature2": "inception (2010)",
        "feature3": "sci-fi",
        "feature4": "sci-fi",
        "genre_test": "sci-fi",
        "user_test": 300,
        "n_value": 3
    }

    # Expected values for Dataset #6
    expected_dataset_six= {
        "feature1": "forrest gump (1994)",
        "feature2": "mad max (1979)",
        "feature3": "drama",
        "feature4": "action",
        "genre_test": "action",
        "user_test": 101,
        "n_value": 5
    }


    run_tests("test_movies.txt", "test_ratings.txt", expected_dataset_one, "Dataset #1")
    run_tests("test_movies2.txt", "test_ratings2.txt", expected_dataset_two, "Dataset #2")
    run_tests("test_movies3.txt", "test_ratings3.txt", expected_dataset_three, "Dataset #3")
    run_tests("test_movies4.txt", "test_ratings4.txt", expected_dataset_four, "Dataset #4")
    run_tests("test_movies5.txt", "test_ratings5.txt", expected_dataset_five, "Dataset #5")
    run_tests("test_movies6.txt", "test_ratings6.txt", expected_dataset_six, "Dataset #6")
