import sqlite3

def migrate():
    conn = sqlite3.connect('instance/trackmycourse.db')
    cur = conn.cursor()
    try:
        cur.execute('ALTER TABLE course ADD COLUMN drive_url VARCHAR(500)')
        conn.commit()
        print('Added drive_url column to course table.')
    except sqlite3.OperationalError as e:
        print('Column already exists or error:', e)

    # Set drive_url for 20MCA201 (Course ID 8)
    cur.execute("""
        UPDATE course
        SET drive_url = 'https://drive.google.com/drive/folders/1d-bjA0vt65UWnMpIMC4u26_gyewsxMOz'
        WHERE code = '20MCA201' OR id = 8
    """)
    conn.commit()

    cur.execute("SELECT id, code, name, drive_url FROM course WHERE code = '20MCA201'")
    print('Updated 20MCA201:', cur.fetchone())
    conn.close()

if __name__ == '__main__':
    migrate()
