from flask import Flask, render_template, request, redirect,flash, session, url_for
import os
import psycopg2

app = Flask(__name__)
##############################################
# Mở file config.py run mà lấy secret_key 
# Lưu ý tránh share secret key 
###############################################
app.secret_key = b'\xc9\xfd"9\xe4v"\xa4\x98:\xa6\x1f\x99\x99qf\x17r}R>\xc73,' 
def connect_db():
    # Kết nối đến cơ sở dữ liệu và trả về kết nối và con trỏ
    conn = psycopg2.connect(
        dbname='QLThuVien',
        user='postgres',
        password='123456',
        host='localhost',
        port='5432'
    )
    cursor = conn.cursor()
    return conn, cursor

def close_db(conn, cursor):
    # Đóng kết nối và con trỏ
    cursor.close()
    conn.close()
#
@app.route('/index')
def index():
    return render_template('index.html')
######
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Xác thực tài khoản ở đây (thường từ cơ sở dữ liệu)
        if request.form['username'] == 'admin' and  request.form['password'] == '123456':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            return 'Sai tên đăng nhập hoặc mật khẩu!'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  # Clear the session data
    return redirect('/login')  # Redirect to login page after logout

@app.route('/all_books')
def all_books():
    conn, cursor = connect_db()

    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()  # Lấy tất cả sách từ cơ sở dữ liệu

    close_db(conn, cursor)
    return render_template("all_book.html", books=books)



@app.route('/books')
def display_books():
    conn, cursor = connect_db()

    cursor.execute('''
        SELECT 
            Books.book_id,
            Books.title AS book_title,
            Books.author,
            Users.username AS borrower,
            Loans.date_borrowed AS borrowed_date,
            Loans.return_date AS return_date  -- Thêm thông tin về ngày trả sách
        FROM 
            Loans
        JOIN 
            Books ON Loans.book_id = Books.book_id
        LEFT JOIN 
            Users ON Loans.user_id = Users.user_id
    ''')
    books_data = cursor.fetchall()

    close_db(conn, cursor)

    return render_template('books.html', books=books_data)
####
@app.route('/readers')
def reader():
    conn, cursor = connect_db()
    cursor.execute('SELECT * FROM reader')

    reader =cursor.fetchall()
    close_db(conn, cursor)
    return render_template('reader.html',reader = reader)

@app.route('/book/<int:book_id>')
def view_book(book_id):
    conn, cursor = connect_db()
    
    cursor.execute('SELECT * FROM books WHERE book_id = %s', (book_id,))
    book = cursor.fetchone()

    close_db(conn, cursor)

    return render_template('book_detail.html', book=book)

@app.route('/book/<int:book_id>/edit')
def edit_book(book_id):
    conn, cursor = connect_db()
    
    cursor.execute('SELECT * FROM Books WHERE book_id = %s', (book_id,))
    book = cursor.fetchone()
    cursor.close()

    if book:
        close_db(conn, cursor)
        return render_template('edit_book.html', book=book, book_id=book_id)
    else:
        close_db(conn, cursor)
        return "Cuốn sách không tồn tại!"

@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    conn, cursor = connect_db()
    
    try:
        cursor.execute('DELETE FROM Loans WHERE book_id = %s', (book_id,))
        cursor.execute('DELETE FROM Books WHERE book_id = %s', (book_id,))
        conn.commit()
    except psycopg2.Error as e:
        conn.rollback()
        print("Error deleting book:", e)
    finally:
        close_db(conn, cursor)

    return redirect('/all_books')
####

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'GET':
        return render_template('add_book.html')

    if request.method == 'POST':
        book_id =request.form['book_id']
        title = request.form['title']
        author = request.form['author']
        year_published = request.form['year_published']
        genre = request.form['genre']
        quantity_available = request.form['quantity_available']

        # Kiểm tra xem mã sách đã tồn tại chưa 
        conn, cursor = connect_db()
        cursor.execute('SELECT * FROM Books WHERE book_id = %s', (book_id))
        book = cursor.fetchone()

        if book:
            cursor.close()
            return render_template('add_book.html', error='mã sách đã tồn tại!')

        # Thêm sách vào cơ sở dữ liệu
        try:
            cursor.execute('''
            INSERT INTO Books (book_id,title, author, year_published, genre, quantity_available)
            VALUES (%s, %s, %s, %s, %s,%s)
            ''', (book_id,title, author, year_published, genre, quantity_available))
            conn.commit()
            cursor.close()
            return render_template('add_book.html', success='Thêm sách thành công!')
        except Exception as e:
            cursor.close()
            return render_template('add_book.html', error='Đã xảy ra lỗi khi thêm sách!')
        
    
if __name__ == '__main__':
    app.run(debug=True)
