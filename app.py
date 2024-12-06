from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from database import get_db_connection, init_db
from flask_caching import Cache

app = Flask(__name__)
app.secret_key = 'your_secret_key'
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Cache configuration
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})

# Initialize the database
init_db()

# User class to handle login details
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

# In-memory user store (replace with a DB later)
users = []

# Load user
@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        return User(id=user['id'], username=user['username'], password=user['password'])
    return None


# Route: Register a new user

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        conn = get_db_connection()
        try:
            # Insert user into the database
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                         (username, hashed_password))
            conn.commit()
            flash('Registration successful, you can now log in', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Registration failed: {e}', 'danger')
        finally:
            conn.close()

    return render_template('register.html')


# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            user_obj = User(id=user['id'], username=user['username'], password=user['password'])
            login_user(user_obj)
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))

        flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')


# Route: Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required  # Protect this route with authentication
@cache.cached(timeout=300)  # Cache for 300 seconds
def index():
    conn = get_db_connection()
    recipes = conn.execute('SELECT * FROM recipes').fetchall()
    conn.close()
    return render_template('index.html', recipes=recipes)

@app.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        conn = get_db_connection()
        conn.execute('INSERT INTO recipes (title, ingredients, instructions) VALUES (?, ?, ?)',
                     (title, ingredients, instructions))
        conn.commit()
        conn.close()

        cache.clear()  # Clear all cached data
        return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/recipe/<int:id>')
@login_required  # Protect this route with authentication
@cache.cached(timeout=300, query_string=True)  # Cache results based on query string and timeout
def view(id):
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (id,)).fetchone()
    conn.close()

    if recipe is None:
        return render_template('view.html', recipe=None), 404  # Return 404 if not found
    
    return render_template('view.html', recipe=recipe)

@app.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    conn = get_db_connection()
    recipe = conn.execute('SELECT * FROM recipes WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        title = request.form['title']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        conn.execute('UPDATE recipes SET title = ?, ingredients = ?, instructions = ? WHERE id = ?',
                     (title, ingredients, instructions, id))
        conn.commit()
        conn.close()
        cache.clear()  # Clear all cached data
        return redirect(url_for('index'))

    conn.close()
    return render_template('update.html', recipe=recipe)

# Route: Delete a recipe
@app.route('/delete/<int:id>', methods=('POST',))
@login_required  # Protect this route with authentication
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM recipes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=False, port=8080, use_reloader=True)


