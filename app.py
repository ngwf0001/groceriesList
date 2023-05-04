import sqlite3
import random
from flask import Flask, session, render_template, request, g

app = Flask(__name__)
app.secret_key = "select_a_COMPLEX_secret_key_please"

@app.route("/")
def index(): 
    all_items, shopping_items = get_db()
    session['shopping_list'] = shopping_items
    session['all_items'] = all_items
    return render_template('index.html', 
                        all_items=all_items, 
                        shopping_items=shopping_items)

@app.route("/add_items", methods=['POST'])
def add_items():
    item_selected = request.values.get('select_items')
    session['shopping_list'].append(item_selected)
    session.modified=True
    return render_template('index.html', 
                    all_items=session['all_items'], 
                    shopping_items=session['shopping_list'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('grocery_list.db')
        cursor = db.cursor()
        cursor.execute("select * from groceries")
        all_data = cursor.fetchall()
        all_data =[data[1] for data in all_data]
        
        shopping_list = all_data.copy()
        random.shuffle(shopping_list)
        shopping_list = shopping_list[:5]
        return all_data, shopping_list

    

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
        

with app.app_context():
    pass

if __name__ == '__main__':
    app.run(debug=True, threaded=True, port=5001)