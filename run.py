import db
# 创建数据库实例
db = db.Database()

# 创建一个名为students的表，有三列：id、name、age
columns = ["id", "name", "age"]
db.create_table("students", columns)

# 插入数据
data = [(1, "Nagasaki", 16), (2, "Chihaya", 15), (3, "Takamatsu", 14)]
for record in data:
    db.tables["students"].insert(record)

# 创建基于name列的平衡二叉树索引
db.tables["students"].create_index("name_index", "balanced_binary_tree", "name")

# 查询名字为Nagasaki的学生信息
condition = {"name": "Nagasaki"}
result = db.tables["students"].select(columns, condition)
print(result)

# 更新年龄为16岁的学生的名字为Shiina
update_values = {"name": "Shiina"}
db.tables["students"].update({"age": 20}, update_values)

# 删除年龄为14岁的学生记录
db.tables["students"].delete({"age": 22})