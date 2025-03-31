import pandas as pd
from flask import Flask, render_template, request, url_for, send_from_directory, redirect

app = Flask(__name__, template_folder='templates', static_folder='static')

todos = []

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    todo = request.form['todo']
    todos.append(todo)
    return redirect(url_for('index'))

@app.route('/remove/<int:index>')
def remove(index):
    del todos[index-1]
    return redirect(url_for('index'))

@app.route('/download_todos')
def download():
    df = pd.DataFrame({
        'todo_id': list(range(len(todos))),
        'todo': todos
    })

    df.to_excel('todos.xlsx')

    return send_from_directory(directory='.', path='todos.xlsx', as_attachment=False)


if __name__ == '__main__':
    app.run(debug=True)
# The following code is for the HTML template (index.html)