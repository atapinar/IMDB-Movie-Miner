import requests
import json
import time
import textwrap
from PIL import Image
from io import BytesIO
import os


class Film:
    def __init__(self, title, year, genre, rating, director, actors, poster, imdb, plot):
        self.title = title
        self.year = year
        self.genre = genre
        self.rating = rating
        self.director = director
        self.actors = actors
        self.poster = poster
        self.imdb = imdb
        self.plot = plot

    def __str__(self):
        return (
            f"Title: {self.title}\n"
            f"Year: {self.year}\n"
            f"Genre: {self.genre}\n"
            f"IMDB Rating: {self.rating}\n"
            f"Director: {self.director}\n"
            f"Actors: {self.actors}\n"
            f"Plot: {textwrap.fill(self.plot, 80)}\n"
            f"IMDB Link: {self.imdb}\n"
        )

    def display_poster(self):
        if self.poster and self.poster != 'N/A':
            try:
                response = requests.get(self.poster)
                img = Image.open(BytesIO(response.content))
                img.show()
            except Exception as error:
                print(f"Unable to display the poster: {error}")
        else:
            print("Poster not available.")

    def save_movie_data(self):
        movie_data = {
            "Title": self.title,
            "Year": self.year,
            "Genre": self.genre,
            "IMDB Rating": self.rating,
            "Director": self.director,
            "Actors": self.actors,
            "Plot": self.plot,
            "IMDB Link": self.imdb
        }

        filename = self.title.replace(" ", "_") + ".json"
        with open(filename, "w") as json_file:
            json.dump(movie_data, json_file, indent=4)
        print(f"Saved movie data to {filename}")

    @staticmethod
    def fetch_movie_data(title):
        api_key = os.getenv('OMDB_API_KEY', '97ce0888')  # Ideally set your API key as an environment variable
        url = f'http://www.omdbapi.com/?t={title.replace(" ", "+")}&apikey={api_key}'

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data["Response"] == "True":
            # Create a Film object from the API data
            film = Film(
                title=data.get("Title", "N/A"),
                year=data.get("Year", "N/A"),
                genre=data.get("Genre", "N/A"),
                rating=data.get("imdbRating", "N/A"),
                director=data.get("Director", "N/A"),
                actors=data.get("Actors", "N/A"),
                poster=data.get("Poster", "N/A"),
                imdb=f"https://www.imdb.com/title/{data.get('imdbID', '')}",
                plot=data.get("Plot", "N/A")
            )
            return film
        else:
            print(f"Error fetching data for {title}, please check the spelling or try another title.")
            return None


def main():
    while True:
        user_input = input("Enter a movie title or type 'exit' to quit: ")
        if user_input.lower() == "exit":
            print("Thanks for using Movie Searcher 2.0")
            break

        movie = Film.fetch_movie_data(user_input)
        if movie:
            print("\n" + "=" * 40)
            print(movie)
            print("=" * 40 + "\n")

            poster_option = input("Would you like to view the poster? (yes/no): ")
            if poster_option.lower() in ["yes", "y"]:
                movie.display_poster()

            save_option = input("Would you like to save the movie data? (yes/no): ")
            if save_option.lower() in ["yes", "y"]:
                movie.save_movie_data()

        # Adding a shorter sleep time to prevent API abuse, but still provide a buffer
        time.sleep(2)


if __name__ == "__main__":
    main()
