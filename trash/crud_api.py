from flask import Flask, jsonify, request

app = Flask(__name__)

users = [
    { "id": 1, "name": "Alice", "email": "alice@email.com", "age": 25},
    { "id": 2, "name": "Bob", "email": "bob@email.com", "age": 26},
    { "id": 3, "name": "Saria", "email": "saria@email.com", "age": 24},
    { "id": 4, "name": "John", "email": "john@email.com", "age": 23},
]

@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    else:
        return jsonify({"message": "user not found"}), 404

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = {
        "id": users[-1]["id"] + 1 if users else 1,
        "name": data.get("name"),
        "email": data.get("email"),
        "age": data.get("age"),
    }

    users.append(new_user)
    return jsonify(new_user), 201

@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        user["name"] = data.get("name", user["name"])
        user["email"] = data.get("email", user["email"])
        user["age"] = data.get("age", user["age"])
        return jsonify(user)
    else:
        return jsonify({"message": "id user not found"}), 404

@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": "user deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)