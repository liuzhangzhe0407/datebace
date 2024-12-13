class Database:
    def __init__(self):
        self.tables = {}

    def create_table(self, table_name, columns):#创建
        if table_name not in self.tables:
            self.tables[table_name] = Table(table_name, columns)
            return True
        return False


class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        self.data = []
        self.indexes = {}

    #增
    def insert(self, record):
        if len(record) == len(self.columns):
            self.data.append(record)
            return True
        return False
        
    #删
    def delete(self, condition):
        new_data = []
        for row in self.data:
            if not self._evaluate_condition(row, condition):
                new_data.append(row)
        self.data = new_data
        return True

    #改
    def update(self, condition, update_values):
        updated_rows = 0
        for i in range(len(self.data)):
            row = self.data[i]
            if self._evaluate_condition(row, condition):
                updated_row = list(row)
                for col_name, new_value in update_values.items():
                    col_index = self.columns.index(col_name)
                    updated_row[col_index] = new_value
                self.data[i] = tuple(updated_row)
                updated_rows += 1
        return updated_rows > 0

    #查
    def select(self, columns, condition):
        result = []
        selected_column_indices = [self.columns.index(col) for col in columns]
        for row in self.data:
            if self._evaluate_condition(row, condition):
                selected_row = [row[i] for i in selected_column_indices]
                result.append(selected_row)
        return result

    def create_index(self, index_name, index_type, column_name):
        col_index = self.columns.index(column_name)
        if index_type == "balanced_binary_tree":
            self.indexes[index_name] = BalancedBinaryTreeIndex([row[col_index] for row in self.data])
        # 可以类似地添加对KD树、红黑树等索引的创建逻辑，这里暂省略部分代码

    def _evaluate_condition(self, row, condition):
        # 简单实现条件判断逻辑，例如支持等于条件，可扩展支持更多复杂条件
        for col_name, value in condition.items():
            col_index = self.columns.index(col_name)
            if row[col_index]!= value:
                return False
        return True


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

#平衡二叉树
class BalancedBinaryTreeIndex:
    def __init__(self, values):
        self.root = self._build_balanced_tree(values)

    def _build_balanced_tree(self, values):
        if not values:
            return None
        sorted_values = sorted(values)
        mid = len(sorted_values) // 2
        root = Node(sorted_values[mid])
        root.left = self._build_balanced_tree(sorted_values[:mid])
        root.right = self._build_balanced_tree(sorted_values[mid + 1:])
        return root

    def search(self, value):
        return self._search_helper(self.root, value)

    def _search_helper(self, node, value):
        if node is None:
            return False
        if node.value == value:
            return True
        elif value < node.value:
            return self._search_helper(node.left, value)
        else:
            return self._search_helper(node.right, value)
