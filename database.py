import sqlite3
from turtle import pos
from typing import List
import datetime
from model import Todo

conn = sqlite3.connect('todos.db')
c = conn.cursor()

def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS todos (
        task text,
        category text,
        date_added text,
        date_completed text,
        status integer,
        position integer
    )
    """
    )

create_table()

def insert_todo(todo: Todo):
    c.execute('select count(*) from todos')
    count = c.fetchone()[0]
    todo.position = count if count else 0
    with conn:
        # Colon is used in the insert statement to prevent sql injection. This is called parameter substitution
        c.execute('INSERT INTO todos VALUES (:task, :category, :date_added, :date_completed, :status, :position)',
                    {'task': todo.task, 'category': todo.category, 'date_added': todo.date_added, 'date_completed': todo.date_completed, 
                     'status': todo.status, 'position': todo.position})

def get_all_todo()->List[Todo]:
    c.execute('select * from todos')
    results = c.fetchall()
    todos = []
    for result in results:
        todos.append(Todo(*result))
    return todos

def delete_todo(position):
    c.execute('SELECT count(*) FROM todos')
    count = c.fetchone()

    with conn:
        c.execute('DELETE FROM todos WHERE position=:position', {'position': position})
        for pos in (position+1 , count):
            change_position(pos, pos-1, False)

def change_position(old_position: int, new_position: int, commint: bool = True):
    c.execute('UPDATE todos SET position=:new_position WHERE position=:old_position', 
                {'new_position': new_position, 'old_position': old_position})
    if commint:
        conn.commit()

def update_todo(position: int, task: str, category: str):
    with conn:
        if task is not None and category is not None:
            c.execute('UPDATE todos SET task=:task, category=:category WHERE position=:position',
                        {'task': task, 'category': category, 'position': position})
        elif task is not None:
            c.execute('UPDATE todos SET task=:task WHERE position=:position',
                        {'task': task, 'position': position})
        elif category is not None:
            c.execute('UPDATE todos SET category=:category WHERE position=:position',
                        {'category': category, 'position': position})
    pass

def complete_todo(position: int):
    with conn:
        c.execute('UPDATE todo SET status = 2, date_completed=:date_completed WHERE position=:position',
                    {'position': position, 'date_completed':datetime.datetime.now().isoformat()})