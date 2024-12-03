import hashlib
import time

class User:
    def __init__(self, nickname: str, password: str, age: int):
        self.nickname = nickname
        self.password = hashlib.sha256(password.encode()).hexdigest()  # ИСПРАВЛЕНО: заменено на sha256
        self.age = age

    def __str__(self):
        return self.nickname

class Video:
    def __init__(self, title: str, duration: int, adult_mode: bool = False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode

    def __eq__(self, other):
        return isinstance(other, Video) and self.title == other.title  # ИСПРАВЛЕНО: добавлена проверка типа


class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def register(self, nickname: str, password: str, age: int):
        for user in self.users:
            if user.nickname == nickname:
                print(f'Пользователь {nickname} уже существует')
                return
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user

    def log_out(self):
        self.current_user = None

    def log_in(self, nickname: str, password: str):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        for user in self.users:
            if user.nickname == nickname and user.password == hashed_password:
                self.current_user = user
                return# ИСПРАВЛЕНО
        print('Пользователь не найден или пароль не верный.')

    def add(self, *videos):
        for video in videos:
            if video not in self.videos:# уникальность видео проверяем с помощью метода __eq__
                self.videos.append(video)

    def get_videos(self, keyword: str):
        list_keyword = []
        for video in self.videos:
            if keyword.upper() in video.title.upper():
                list_keyword.append(video.title)
        return list_keyword

    def watch_video(self, title: str):
        if not self.current_user:
            print('Войдите в аккаунт, чтобы смотреть видео.')
            return
        for video in self.videos:
            if video.title == title:
                if video.adult_mode and self.current_user.age < 18:
                    print('Вам нет 18 лет, пожалуйста, покиньте страницу')
                    return
                while video.time_now < video.duration:
                    time.sleep(1)
                    video.time_now += 1
                    print(video.time_now, end='')
                print(' Конец видео')
                video.time_now = 0

if __name__ == '__main__':

    ur = UrTube()
    v1 = Video('Лучший язык программирования 2024 года', 200)
    v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

    ur.add(v1, v2)

    print(ur.get_videos('лучший'))
    print(ur.get_videos('ПРОГ'))

    ur.watch_video('Для чего девушкам парень программист?')
    ur.register('vasya_pupkin', 'lolkekcheburek', 13)
    ur.watch_video('Для чего девушкам парень программист?')
    ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
    ur.watch_video('Для чего девушкам парень программист?')

    ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
    print(ur.current_user)

    ur.watch_video('Лучший язык программирования 2024 года!')
