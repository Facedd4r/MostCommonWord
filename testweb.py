import unittest
import io
from main import app
class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client() #позволяет эмулировать HTTP‑запросы
        self.app.testing = True #переводит приложение в режим тестирования

    def test_index_page_loads(self):
        # Тестируем GET-запрос к маршрутам "/" и "/index" и проверяем, что возвращается статус 200.
        response_root = self.app.get('/') #эмулирует GET‑запрос по URL /
        self.assertEqual(response_root.status_code, 200)
        response_index = self.app.get('/index')
        self.assertEqual(response_index.status_code, 200)

    def test_post_file_correct_decoding(self):
        #словарь data с кортежем
        data = {
            'file': (io.BytesIO(b"Hello hello world"), 'test.txt')
        }
        #data=data передаем словарь
        #content_type='multipart/form-data' указывает, что передается форма с файлом.
        response = self.app.post('/', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn("hello".encode('utf-8'), response.data)
        self.assertIn("2".encode('utf-8'), response.data)

    def test_post_empty_file(self):
        data = {
            "file": (io.BytesIO(b""), "empty.txt")
        }
        response = self.app.post('/', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn("".encode('utf-8'), response.data) #response.data хранит тело HTTP‑ответа,

    def test_post_missing_file(self):
        # Отправляем POST-запрос без файла. Ожидаем, что сервер не вернёт статус 200.
        response = self.app.post('/', data={}, content_type='multipart/form-data')
        self.assertNotEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
