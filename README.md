# Graph
Класс граф для игры "Город отражений".

Работа класса на примере лодочников. Каждая вершина графа - отдельная ячейка. Вершины, помеченные одним цветом, касаются одной достопримечательности.

Входные данные:

![input_data](https://github.com/alenahalm/Graph/assets/75882124/ade39e43-b5c2-4850-9a06-478c25f1caa6)

Для поиска оптимального пути необходимо вызвать метод _calculate()_.

```python
def calculate(self):
        self.simplify()
        self.divide_graphs()
        self.remove_pairs()
        self.remove_extra_edges()
        d, p = self.shortest_distance()
        return d, p
```
