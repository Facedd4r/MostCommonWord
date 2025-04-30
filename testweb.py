import unittest
from main import app

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # позволяет эмулировать HTTP‑запросы
        self.app.testing = True  # переводит приложение в режим тестирования

    def test_index_page_loads(self):
        # Тестируем GET-запрос к маршрутам "/" и "/index" и проверяем, что возвращается статус 200.
        response_root = self.app.get('/')  # эмулирует GET‑запрос по URL /
        self.assertEqual(response_root.status_code, 200)
        response_index = self.app.get('/index')
        self.assertEqual(response_index.status_code, 200)

    def test_post_file_correct_decoding(self):
        # словарь data с кортежем
        with open('test.txt', 'rb') as f:
            data = {
                'file': (f, 'test.txt')
            }
        # data=data передаем словарь
        # content_type='multipart/form-data' указывает, что передается форма с файлом.
            response = self.app.post('/', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn("hello".encode('utf-8'), response.data)
            self.assertIn("2".encode('utf-8'), response.data)

    def test_post_empty_file(self):
        with open('spaces.txt', 'rb') as f:
            data = {
                "file": (f, "spaces.txt")
            }
            response = self.app.post('/', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn("видел".encode('utf-8'), response.data) # response.data хранит тело HTTP‑ответа
            self.assertIn("3".encode('utf-8'), response.data) #проверяет, находится ли элемент в контейнере

    def test_post_file_punctuation(self):
        with open('punctuation.txt', 'rb') as f:
            data = {
                "file": (f, "punctuation.txt")
            }
            response = self.app.post('/', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn("я".encode('utf-8'), response.data)
            self.assertIn("2".encode('utf-8'), response.data)

    def test_post_file_two_words(self):
        with open('words.txt', 'rb') as f:
            data = {
                "file": (f, "words.txt")
            }
            response = self.app.post('/', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn("гулял".encode('utf-8'), response.data)
            self.assertIn("2".encode('utf-8'), response.data)




if __name__ == '__main__':
    unittest.main()
