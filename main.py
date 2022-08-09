import random
from datetime import date
from faker import Faker
fake = Faker(locale="pl_PL")

class Movie:
    def __init__(self, title, release_date, genre, played):
        self.title = title
        self.release_date = release_date
        self.genre = genre
        self.played = played

    def __str__(self):
        return f'{self.title} ({self.release_date})'

    def play(self):
        return self.played+1 

class Serie(Movie):
    def __init__(self, episode_num, serie_num, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.episode_num = episode_num
        self.serie_num = serie_num

    def __str__(self):
        return ("%s S%02dE%02d" % (self.title, self.serie_num, self.episode_num))
        #return f'{self.title} S{self.serie_num}E{self.episode_num}'

    def get_episodes_number(self, list_of_movies):
        count = 0
        for i in list_of_movies:
            if self.title == i.title:
                count += 1
        return count

def get_movies(list_of_movies):
    only_movies = []
    for i in list_of_movies:
        if type(i) == Movie:
            only_movies.append(i)
    return sorted(only_movies, key=lambda movie: movie.title)

def get_series(list_of_movies):
    only_series = []
    for i in list_of_movies:
        if type(i) == Serie:
            only_series.append(i)
    return sorted(only_series, key=lambda movie: movie.title)

def search(list_of_movies, title):
    for i in list_of_movies:
        if i.title == title:
            print(i)

def generate_ten_times(func):
    def wrapper(*args, **kwargs):
        for _ in range(10):
            func(*args, **kwargs)
        #return func(*args, **kwargs)
    return wrapper

@generate_ten_times
def generate_views(list_of_movies):
    index=list_of_movies.index(random.choice(list_of_movies))
    list_of_movies[index].played += random.choice(range(1, 101))
    #print(list_of_movies[index].played)
    return list_of_movies

#dodać parametr content_type
def top_titles(title_num, content_type, list_of_movies):
    #zakładam, że człowieko-komputer wybierze zawsze opcję 1 lub 2 :]
    if content_type == 1:
        list_of_movies = get_movies(list_of_movies)
    elif content_type == 2:
        list_of_movies = get_series(list_of_movies)
    top_titles = sorted(list_of_movies, key=lambda movie: movie.played, reverse=True)
    return top_titles[:title_num]

def add_full_seasons(_title, _release_date, _genre, season_num, episode_amount, list_of_movies):
    for i in range(episode_amount):
        serial = Serie(title=_title, release_date=_release_date, genre=_genre, serie_num=season_num, episode_num=i+1, played=0)
        list_of_movies.append(serial)
        print(serial)
    return list_of_movies

def create_movie_library(series, movies):
    temp_movie_list = []
    for _ in range(series):
        serie = Serie(title=fake.company(), release_date=fake.year(), genre=fake.first_name(), serie_num=random.choice(range(1,25)), episode_num=random.choice(range(1,25)), played=0)
        temp_movie_list.append(serie)
    for _ in range(movies):
        movie = Movie(title=fake.company(), release_date=fake.year(), genre=fake.first_name(), played=0)
        temp_movie_list.append(movie)
    return temp_movie_list

if __name__ == "__main__":
    print("Biblioteka filmów.")
    #wypełnij bibliotekę treścią x filmów, y seriali
    movie_list = create_movie_library(20,20)
    #wygeneruj views
    generate_views(movie_list)
    #pokaż bibliotekę filmów i seriali
    for i in movie_list:
        print(f'{i}, wyświetleń {i.played}')
    #dodaj cały sezon
    print("")
    movie_list = add_full_seasons("Pełny Sezon", "2022", "Criminal", 5, 15, movie_list)
    #ile episodów danego serialu
    print("")
    print(f'Ile episodów danego serialu: {movie_list[40].get_episodes_number(movie_list)}')
    #pokaż najpopularniejsze seriale i filmy dzisiaj
    today = date.today()
    d = today.strftime("%d.%m.%Y")
    print("")
    print(f'Najpopularniejsze filmy i seriale dnia {d}:')
    top = top_titles(5,2,movie_list)
    for i in top:
        print(f'{i}, wyświetleń {i.played}')