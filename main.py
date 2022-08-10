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
        return f'{self.title} S{self.serie_num:02d}E{self.episode_num:02d}'

    def get_episodes_number(self, video_library):
        count = 0
        for i in video_library:
            if self.title == i.title:
                count += 1
        return count

def get_video(video_library, video_type):
    videos = []
    for i in video_library:
        if type(i) == video_type:
            videos.append(i)
    return videos

def get_movies(video_library):
    return sorted(get_video(video_library, Movie), key=lambda movie: movie.title)

def get_series(video_library):
    return sorted(get_video(video_library, Serie), key=lambda serie: serie.title)

def search(video_library, title):
    for i in video_library:
        if i.title == title:
            return i

def generate_ten_times(func):
    def wrapper(*args, **kwargs):
        for _ in range(10):
            func(*args, **kwargs)
    return wrapper

@generate_ten_times
def generate_views(video_library):
    index = random.randint(0,len(video_library)-1)
    video_library[index].played += random.randint(1,100)

def top_titles(title_num, content_type, video_library):
    #zakładam, że człowieko-komputer wybierze zawsze opcję 1 lub 2 :]
    if content_type == 1:
        video_library = get_movies(video_library)
    elif content_type == 2:
        video_library = get_series(video_library)
    top_titles = sorted(video_library, key=lambda movie: movie.played, reverse=True)
    return top_titles[:title_num]

def add_full_seasons(_title, _release_date, _genre, season_num, episode_amount, video_library):
    for i in range(episode_amount):
        serial = Serie(title=_title, release_date=_release_date, genre=_genre, serie_num=season_num, episode_num=i+1, played=0)
        video_library.append(serial)
        print(serial)
    return video_library

def create_movie_library(series, movies):
    temp_library = []
    for _ in range(series):
        serie = Serie(title=fake.company(), release_date=fake.year(), genre=fake.first_name(), serie_num=random.choice(range(1,25)), episode_num=random.choice(range(1,25)), played=0)
        temp_library.append(serie)
    for _ in range(movies):
        movie = Movie(title=fake.company(), release_date=fake.year(), genre=fake.first_name(), played=0)
        temp_library.append(movie)
    return temp_library

if __name__ == "__main__":
    print("Biblioteka filmów.")
    library = create_movie_library(20,20)
    generate_views(library)
    for i in library:
        print(f'{i}, wyświetleń {i.played}')
    print("")
    library = add_full_seasons("Pełny Sezon", "2022", "Criminal", 5, 15, library)
    print("")
    print(f'Ile episodów danego serialu: {library[40].get_episodes_number(library)}')
    today = date.today()
    d = today.strftime("%d.%m.%Y")
    print("")
    print(f'Najpopularniejsze filmy i seriale dnia {d}:')
    top = top_titles(5,1,library)
    for i in top:
        print(f'{i}, wyświetleń {i.played}')