Стартовать сервис можно командой docker-compose up из каталога проекта
Запустить тесты можно командой docker exec -it appfollow pytest -v tests

Сервис слушает localhosts:8000 c единственным методом GET posts
В качестве параметров принимает следующие поля:
1) order - выбирается из значений (asc, desc)
2) sort - возможна сортировка по полям(id, url, title, created)
3) limit - целочисленное значение <= 1000
4) offset - целочисленное значение

Пример:
1) curl -X GET http://localhost:8000/posts?offset=10&limit=10
2) curl -X GET http://localhost:8000/posts?offset=10&limit=10&sort=id
3) curl -X GET http://localhost:8000/posts?offset=10&limit=10&sort=created&order=desc