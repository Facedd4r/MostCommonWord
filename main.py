from flask import Flask, render_template, request
from collections import Counter #для подсчёта частоты встречаемости слов в тексте.
app = Flask(__name__)
#если пользователь обращается по этим адресам
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html") # Если GET-запрос, просто возвращаем форму

@app.route('/', methods=['post', 'get']) #для post запроса
def form():
    if request.method == 'POST': #Проверяется, что метод запроса равен POST
        file = request.files["file"]
        if file: #если файл присутствует
            content = file.read().decode("utf-8")
            words = content.split()
            words = [word.lower() for word in words] #списочное выражение
            counter = Counter(words) #объект, хранящий сколько раз каждое слово встречается в тексте
            if counter: #если есть слова
                #Метод most_common(n) возвращает список из n самых часто встречающихся элементов
                most_common_word, freq = counter.most_common(1)[0]
                # [0] берем первый элемент списка, то есть кортеж(слово, количество).
            else:
                most_common_word, freq = None, 0
            return render_template('result.html', word=most_common_word, frequency=freq)



if __name__ == '__main__':
    app.run(debug=True) #запускает встроенный сервер Flask