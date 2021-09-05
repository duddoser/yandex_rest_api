from requests import get, post, delete, put

# # получение всех новостей
# print(get('http://localhost:8080/news').json())
#
# # получение одной новости
# print(get('http://localhost:8080/news/4').json())
# print(get('http://localhost:8080/news/8').json())
# print(get('http://localhost:8080/news/q').json())
#
# # добавление новости
# print(post('http://localhost:8080/news').json())
# print(post('http://localhost:8080/news',
#            json={'title': 'Заголовок'}).json())
# print(post('http://localhost:8080/news',
#            json={'title': 'Заголовок',
#                  'content': 'Текст новости',
#                  'user_id': 1}).json())
#
# # удаление новости
# print(delete('http://localhost:8080/news/4').json())
# print(delete('http://localhost:8080/news/3').json())

# изменение новости
print(put('http://localhost:8080/news',
          json={'title': 'Заголовок'}).json())
print(put('http://localhost:8080/news',
          json={'title': 'Заголовок',
                'content': 'Текст новости',
                'user_id': 1}).json())
