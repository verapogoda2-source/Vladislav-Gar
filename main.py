import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

FILENAME = 'movies.json'

# Загрузка данных из файла
def load_movies():
    if os.path.exists(FILENAME):
        with open(FILENAME, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Сохранение данных
def save_movies(data):
    with open(FILENAME, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = load_movies()
        self.filtered_list = self.movies.copy()

        self.create_widgets()
        self.update_treeview()

    def create_widgets(self):
        # Поля для ввода
        frame_input = tk.Frame(self.root)
        frame_input.pack(pady=10)

        tk.Label(frame_input, text="Название:").grid(row=0, column=0, padx=5, sticky='w')
        self.entry_title = tk.Entry(frame_input, width=20)
        self.entry_title.grid(row=0, column=1, padx=5)

        tk.Label(frame_input, text="Жанр:").grid(row=0, column=2, padx=5, sticky='w')
        self.entry_genre = tk.Entry(frame_input, width=15)
        self.entry_genre.grid(row=0, column=3, padx=5)

        tk.Label(frame_input, text="Год:").grid(row=1, column=0, padx=5, sticky='w')
        self.entry_year = tk.Entry(frame_input, width=10)
        self.entry_year.grid(row=1, column=1, padx=5)

        tk.Label(frame_input, text="Рейтинг:").grid(row=1, column=2, padx=5, sticky='w')
        self.entry_rating = tk.Entry(frame_input, width=10)
        self.entry_rating.grid(row=1, column=3, padx=5)

        # Кнопка для добавления
        btn_add = tk.Button(self.root, text="Добавить фильм", command=self.add_movie)
        btn_add.pack(pady=5)

        # Фильтры
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=10)

        tk.Label(filter_frame, text="Фильтр по жанру:").grid(row=0, column=0, padx=5)
        self.filter_genre_entry = tk.Entry(filter_frame, width=15)
        self.filter_genre_entry.grid(row=0, column=1, padx=5)

        tk.Label(filter_frame, text="Фильтр по году:").grid(row=0, column=2, padx=5)
        self.filter_year_entry = tk.Entry(filter_frame, width=10)
        self.filter_year_entry.grid(row=0, column=3, padx=5)

        btn_filter = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        btn_filter.grid(row=0, column=4, padx=5)

        btn_show_all = tk.Button(filter_frame, text="Показать всё", command=self.show_all)
        btn_show_all.grid(row=0, column=5, padx=5)

        # Таблица для отображения фильмов
        columns = ('Название', 'Жанр', 'Год', 'Рейтинг')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings', height=10)
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.pack(pady=10)

    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for movie in self.filtered_list:
            self.tree.insert('', 'end', values=(
                movie['title'], movie['genre'], movie['year'], movie['rating']
            ))

    def add_movie(self):
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        year_str = self.entry_year.get().strip()
        rating_str = self.entry_rating.get().strip()

        # Проверка корректности
        if not title or not genre or not year_str or not rating_str:
            messagebox.showerror("Ошибка", "Все поля обязательны.")
            return

        try:
            year = int(year_str)
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом.")
            return

        try:
            rating = float(rating_str)
            if not (0 <= rating <= 10):
                raise ValueError()
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10.")
            return

        new_movie = {"title": title, "genre": genre, "year": year, "rating": rating}
        self.movies.append(new_movie)
        save_movies(self.movies)
        self.clear_input()
        self.show_all()

    def clear_input(self):
        self.entry_title.delete(0, tk.END)
        self.entry_genre.delete(0, tk.END)
        self.entry_year.delete(0, tk.END)
        self.entry_rating.delete(0, tk.END)

    def apply_filter(self):
        genre_filter = self.filter_genre_entry.get().strip().lower()
        year_filter = self.filter_year_entry.get().strip()

        self.filtered_list = self.movies.copy()

        if genre_filter:
            self.filtered_list = [m for m in self.filtered_list if genre_filter in m['genre'].lower()]

        if year_filter:
            try:
                year_val = int(year_filter)
                self.filtered_list = [m for m in self.filtered_list if m['year'] == year_val]
            except ValueError:
                messagebox.showerror("Ошибка", "Год фильтра должен быть числом.")
                return

        self.update_treeview()

    def show_all(self):
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_year_entry.delete(0, tk.END)
        self.filtered_list = self.movies.copy()
        self.update_treeview()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()
