class BinaryIndexedTree:
    def __init__(self, n):
        self.tree = [0] * (n + 1)
        self.n = n

    def update(self, idx, val):
        while idx <= self.n:
            self.tree[idx] += val
            idx += idx & -idx

    def query(self, idx):
        res = 0
        while idx > 0:
            res += self.tree[idx]
            idx -= idx & -idx
        return res


class SegmentTree:
    def __init__(self, arr):
        self.segment_tree = [0] * (4 * len(arr))
        self.n = len(arr)

    def update(self, idx, val, node=1, start=0, end=None):
        if end is None:
            end = self.n - 1
        if start == end:
            self.segment_tree[node] = val
        else:
            mid = (start + end) // 2
            if start <= idx <= mid:
                self.update(idx, val, 2 * node, start, mid)
            else:
                self.update(idx, val, 2 * node + 1, mid + 1, end)
            self.segment_tree[node] = self.segment_tree[2 * node] + self.segment_tree[2 * node + 1]

    def query(self, left, right, node=1, start=0, end=None):
        if end is None:
            end = self.n - 1
        if right < start or left > end:
            return 0
        if left <= start and right >= end:
            return self.segment_tree[node]
        mid = (start + end) // 2
        return (
            self.query(left, right, 2 * node, start, mid)
            + self.query(left, right, 2 * node + 1, mid + 1, end)
        )

    def inversion_count(self, arr):
        max_val = max(arr)
        bit_tree = BinaryIndexedTree(max_val)
        inv_count = 0
        for i in range(len(arr) - 1, -1, -1):
            inv_count += bit_tree.query(arr[i] - 1)
            bit_tree.update(arr[i], 1)
        return inv_count
    
    def build_tree(self, node, start, end, arr):
        if start == end:
            self.segment_tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self.build_tree(2 * node + 1, start, mid, arr)
            self.build_tree(2 * node + 2, mid + 1, end, arr)
            self.segment_tree[node] = self.segment_tree[2 * node + 1] + self.segment_tree[2 * node + 2]

    def update_range(self, node, start, end, left, right, value, arr):
        if start > end or start > right or end < left:
            return

        if start == end:
            arr[start] += value
            self.segment_tree[node] += value
            return

        mid = (start + end) // 2
        self.update_range(2 * node + 1, start, mid, left, right, value, arr)
        self.update_range(2 * node + 2, mid + 1, end, left, right, value, arr)
        self.segment_tree[node] = self.segment_tree[2 * node + 1] + self.segment_tree[2 * node + 2]

    def update_range_of_indexes(self, left, right, value, arr):
        self.update_range(0, 0, len(arr) - 1, left, right, value, arr)
        return arr


def count_inversions(arr):
    seg_tree = SegmentTree(arr)
    return seg_tree.inversion_count(arr)

arr = [1, 3, 5, 7, 9, 11]
segment_tree = SegmentTree(arr)
segment_tree.build_tree(0, 0, len(arr) - 1,arr)

print("Original array:", arr)

left_index = 1
right_index = 4
value_to_add = 10

updated_arr = segment_tree.update_range_of_indexes(left_index, right_index, value_to_add, arr)

print("Updated array:", updated_arr)


arr = [8, 4, 2, 1]
inversions = count_inversions(arr)
print("Inversion count:", inversions)


