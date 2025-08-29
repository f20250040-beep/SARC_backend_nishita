
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
books = {}
borrow_history = {}
book_id_counter = 1

@app.route('/')
def home():
    return "Hello, Flask is working!"

# Create a book
@app.route('/books', methods=['POST'])
def add_book():
    global book_id_counter
    data = request.json
    book_id = book_id_counter
    book_id_counter += 1

    books[book_id] = {
        "id": book_id,
        "title": data.get("title"),
        "author": data.get("author"),
        "genre": data.get("genre"),
        "status": data.get("status")
    }
    borrow_history[book_id] = []
    return jsonify({"message": "Book added", "book": books[book_id]}), 201


# Read all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(list(books.values()))


# Read a single book
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    if book_id not in books:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(books[book_id])


# Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    if book_id not in books:
        return jsonify({"error": "Book not found"}), 404
    data = request.json
    books[book_id].update({
        "title": data.get("title", books[book_id]["title"]),
        "author": data.get("author", books[book_id]["author"]),
        "genre": data.get("genre", books[book_id]["genre"]),
        "status": data.get("status", books[book_id]["status"])
    })
    return jsonify({"message": "Book updated", "book": books[book_id]})


# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    if book_id not in books:
        return jsonify({"error": "Book not found"}), 404
    del books[book_id]
    del borrow_history[book_id]
    return jsonify({"message": "Book deleted"})


# Borrow a book
@app.route('/books/<int:book_id>/borrow', methods=['POST'])
def borrow_book(book_id):
    if book_id not in books:
        return jsonify({"error": "Book not found"}), 404
    data = request.json
    entry = {"action": "borrowed", "date": data.get("date")}
    borrow_history[book_id].append(entry)
    return jsonify({"message": "Book borrowed", "history": borrow_history[book_id]})


# Return a book
@app.route('/books/<int:book_id>/return', methods=['POST'])
def return_book(book_id):
    if book_id not in books:
        return jsonify({"error": "Book not found"}), 404
    data = request.json
    entry = {"action": "returned", "date": data.get("date")}
    borrow_history[book_id].append(entry)
    return jsonify({"message": "Book returned", "history": borrow_history[book_id]})


# Get borrowing history
@app.route('/books/<int:book_id>/history', methods=['GET'])
def get_history(book_id):
    if book_id not in books:
        return jsonify({"error": "Book not found"}), 404
    return jsonify(borrow_history[book_id])


if __name__ == "__main__":
    app.run(debug=True, port=5001)

