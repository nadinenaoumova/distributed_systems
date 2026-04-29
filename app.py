from flask import Flask, jsonify, request

app = Flask(__name__)

menu = [
    {"id": 1, "dish_name": "Пицца", "price": 500, "category": "Основное"},
    {"id": 2, "dish_name": "Салат", "price": 300, "category": "Закуски"}
]

next_id = 3

# Получить всё меню
@app.route('/api/menu', methods=['GET'])
def get_menu():
    return jsonify(menu)

# Получить блюдо по ID
@app.route('/api/menu/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((i for i in menu if i['id'] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Not found"}), 404

# Добавить блюдо
@app.route('/api/menu', methods=['POST'])
def add_item():
    global next_id
    data = request.get_json()

    if not data or 'dish_name' not in data:
        return jsonify({"error": "dish_name required"}), 400

    new_item = {
        "id": next_id,
        "dish_name": data["dish_name"],
        "price": data.get("price", 0),
        "category": data.get("category", "Другое")
    }

    menu.append(new_item)
    next_id += 1

    return jsonify(new_item), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)