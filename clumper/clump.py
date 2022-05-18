class Clumper:
    """
       This object adds methods to a list of dictionaries that make
       it nicer to explore.
       Arguments:
           blob: the list of data to turn into a Clumper
           groups: specify any groups you'd like to attach to the Clumper
           listify: if the input is a dictionary, turn it into a list with one dictionary inside beforehand.
       Usage:
       ```python
       from clumper import Clumper
       list_dicts = [{'a': 1}, {'a': 2}, {'a': 3}, {'a': 4}]
       c = Clumper(list_dicts)
       assert len(c) == 4
       ```
       """

    def __init__(self, blob):
        self.blob = blob

    def keep(self, *funcs):
        """
                Allows you to select which items to keep and which items to remove.

                Arguments:
                    funcs: functions that indicate which items to keep
                Usage:
                ```python
                from clumper import Clumper
                list_dicts = [{'a': 1}, {'a': 2}, {'a': 3}, {'a': 4}]
                clump = Clumper(list_dicts).keep(lambda d: d['a'] >= 3)
                expected = [{'a': 3}, {'a': 4}]
                assert clump.equals(expected)
                ```
                """
        data = self.blob
        for func in funcs:
            data = [d for d in data if func(d)]
        return Clumper(data)

    def head(self, n):
        """
                Selects the top `n` items from the collection.
                ![](../img/head.png)
                Arguments:
                    n: the number of items to grab
                Usage:
                ```python
                from clumper import Clumper
                list_dicts = [{'a': 1}, {'a': 2}, {'a': 3}, {'a': 4}]
                result = Clumper(list_dicts).head(2)
                expected = [{'a': 1}, {'a': 2}]
                assert result.equals(expected)
                ```
                """
        return Clumper([self.blob[i] for i in range(n)])

    def tail(self, n):
        """
                Selects the bottom `n` items from the collection.
                ![](../img/tail.png)
                Arguments:
                    n: the number of items to grab
                Usage:
                ```python
                from clumper import Clumper
                list_dicts = [{'a': 1}, {'a': 2}, {'a': 3}, {'a': 4}]
                result = Clumper(list_dicts).tail(2)
                expected = [{'a': 3}, {'a': 4}]
                assert result.equals(expected)
                ```
                """
        return Clumper([self.blob[-i] for i in range(1, n+1)])

    def select(self, *keys):
        """
                Selects a subset of the keys in each item in the collection.
                ![](../img/select.png)
                Arguments:
                    keys: the keys to keep
                Usage:
                ```python
                from clumper import Clumper
                list_dicts = [
                    {'a': 1, 'b': 2},
                    {'a': 2, 'b': 3, 'c':4},
                    {'a': 1, 'b': 6}]
                clump = Clumper(list_dicts).select('a', 'b')
                assert all(["c" not in d.keys() for d in clump])
                ```
                """
        return Clumper([{k: d[k] for k in keys} for d in self.blob])

    def mutate(self, **kwargs):
        """
                Adds or overrides key-value pairs in the collection of dictionaries.

                Arguments:
                    kwargs: keyword arguments of keyname/function-pairs
                Warning:
                    This method is aware of groups. There may be different results if a group is active.
                Usage:
                ```python
                from clumper import Clumper
                list_dicts = [
                    {'a': 1, 'b': 2},
                    {'a': 2, 'b': 3, 'c':4},
                    {'a': 1, 'b': 6}]
                result = (Clumper(list_dicts)
                          .mutate(c=lambda d: d['a'] + d['b'],
                                  s=lambda d: d['a'] + d['b'] + d['c']))
                expected = [
                    {'a': 1, 'b': 2, 'c': 3, 's': 6},
                    {'a': 2, 'b': 3, 'c': 5, 's': 10},
                    {'a': 1, 'b': 6, 'c': 7, 's': 14}
                ]
                assert result.equals(expected)
                ```
                """
        data = self.blob
        for key, func in kwargs.items():
            for i in range(len(data)):
                data[i][key] = func(data[i])
        return Clumper(data)

    def sort(self, key, reverse=False):
        """
               Allows you to sort the collection of dictionaries.

               Arguments:
                   key: the number of items to grab
                   reverse: the number of items to grab
               Warning:
                   This method is aware of groups. Expect different results if a group is active.
               Usage:
               ```python
               from clumper import Clumper
               list_dicts = [
                   {'a': 1, 'b': 2},
                   {'a': 3, 'b': 3},
                   {'a': 2, 'b': 1}]
               (Clumper(list_dicts)
                 .sort(lambda d: d['a'])
                 .collect())
               (Clumper(list_dicts)
                 .sort(lambda d: d['b'], reverse=True)
                 .collect())
               ```
               """
        return Clumper(sorted(self.blob, key=key, reverse=reverse))

    def collect(self):
        """
            Returns a list instead of a `Clumper` object.
        """
        return self.blob
