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

## Метод _divide_graphs()_
В случае несвязности графа разделяет его на несколько объектов класса. Это необходимо, так как все методы работают с связными графами.

## Метод _remove_pairs()_

Из оставшихся пар (вершин, касающиеся одной достопримечательности) выбирает оптимальную вершину. Для каждой вычисляется набор весов со своим приоритетом. И на их основе выбирается оптимальная.

Результат:

![remove_pairs_result](https://github.com/alenahalm/Graph/assets/75882124/fc522608-f191-49ee-bdaa-69443d39c4e3)

## Метод _remove_extra_edges()_

Упрощает граф далее, убирая лишние ребра и вершины. Результат:

![remove_extra_edges_result](https://github.com/alenahalm/Graph/assets/75882124/b8ae1f5b-31f9-41a4-86fb-b2debd5d0562)

## Метод _shortest_distance()_

Вычисляет оптимальный путь и его длину Результат:

![result](https://github.com/alenahalm/Graph/assets/75882124/f96efbe3-8a93-49d9-8c92-bdc5236e1a70)
