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

Он по очереди выполняет 4 основных метода, направленные на упрощение графа.

## Метод _simplify()_
Убирает незначимые (не имеющие на границе достопримечательность) вершины. Черные вершины выбраны как оптимальные для своей достопримечательности. Результат на примере:

![simplify_result](https://github.com/alenahalm/Graph/assets/75882124/d0c2d02d-8db0-4d02-bf6d-e889425eb21e)

