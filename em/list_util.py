class SliceListView:
    def __init__(self, lst, start=None, end=None):
        self._lst = lst
        self._start = start or 0
        self._end = len(lst) if end is None else end

    def __getitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(self._end - self._start)
            return [self._lst[self._start + i] for i in range(start, stop, step)]
        return self._lst[self._start + index]

    def __setitem__(self, index, value):
        if isinstance(index, slice):
            start, stop, step = index.indices(self._end - self._start)
            indices = range(start, stop, step)
            if hasattr(value, '__iter__'):
                for i, v in zip(indices, value):
                    self._lst[self._start + i] = v
            else:
                for i in indices:
                    self._lst[self._start + i] = value
        else:
            self._lst[self._start + index] = value

    def __delitem__(self, index):
        if isinstance(index, slice):
            start, stop, step = index.indices(self._end - self._start)
            # Collect absolute indices to delete
            indices = list(range(start, stop, step))
            # Deletion must be done from the end to avoid shifting
            for i in reversed(indices):
                del self._lst[self._start + i]
            self._end -= len(indices)
        else:
            del self._lst[self._start + index]
            self._end -= 1

    def __len__(self):
        return self._end - self._start

    def __repr__(self):
        return repr(self[:])

    def index(self, value, start=0, stop=None):
        """Return first index of value in the view (raises ValueError if not found)."""
        length = len(self)
        if stop is None:
            stop = length

        # Normalize indices
        if start < 0:
            start += length
        if stop < 0:
            stop += length

        # Clamp to bounds
        start = max(start, 0)
        stop = min(stop, length)

        for i in range(start, stop):
            if self[i] == value:
                return i
        raise ValueError(f"{value!r} is not in ListView")

    def remove(self, value):
        """Remove the first occurrence of value within the view."""
        for i in range(self._start, self._end):
            if self._lst[i] == value:
                del self._lst[i]
                self._end -= 1  # Adjust view size after deletion
                return
        raise ValueError(f"{value!r} not found in view")


class ConcatenatedListView:
    def __init__(self, *lists):
        self._lists = lists

    def __len__(self):
        return sum(len(lst) for lst in self._lists)

    def _find(self, idx):
        if idx < 0:
            idx += len(self)
        if not 0 <= idx < len(self):
            raise IndexError("Index out of range")
        for lst in self._lists:
            if idx < len(lst):
                return lst, idx
            idx -= len(lst)
        raise IndexError

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return [self[i] for i in range(*idx.indices(len(self)))]
        lst, pos = self._find(idx)
        return lst[pos]

    def __setitem__(self, idx, value):
        if isinstance(idx, slice):
            indices = list(range(*idx.indices(len(self))))
            if hasattr(value, '__iter__') and not isinstance(value, (str, bytes)):
                if len(value) != len(indices):
                    raise ValueError(f"Attempt to assign sequence of size {len(value)} "
                                     f"to extended slice of size {len(indices)}")
                for i, v in zip(indices, value):
                    self[i] = v
            else:
                for i in indices:
                    self[i] = value
        else:
            lst, pos = self._find(idx)
            lst[pos] = value

    def __delitem__(self, idx):
        if isinstance(idx, slice):
            indices = list(range(*idx.indices(len(self))))
            # Deletion should be done from end to avoid shifting
            for i in reversed(indices):
                lst, pos = self._find(i)
                del lst[pos]
        else:
            lst, pos = self._find(idx)
            del lst[pos]

    def index(self, value, start=0, stop=None):
        if stop is None:
            stop = len(self)

        if start < 0:
            start += len(self)
        if stop < 0:
            stop += len(self)

        # Clamp to bounds
        start = max(start, 0)
        stop = min(stop, len(self))

        for i in range(start, stop):
            if self[i] == value:
                return i
        raise ValueError(f"{value!r} is not in ConcatenatedListView")

    def remove(self, value):
        for lst in self._lists:
            try:
                index = lst.index(value)
                del lst[index]
                return
            except ValueError:
                continue
        raise ValueError(f"{value!r} not in ConcatenatedListView")

    def __repr__(self):
        return repr([self[i] for i in range(len(self))])


def first_line(t: str):
    if t:
        return t.splitlines()[0]
    else:
        return ''
