from unicodedata import category
import typer
from rich.console import Console
from rich.table import Table
from model import Todo
from database import get_all_todo, delete_todo, insert_todo, complete_todo, update_todo


console = Console()

app = typer.Typer()

@app.command(short_help='Add an item')
def add(task: str, category: str):
    todo = Todo(task, category)
    insert_todo(todo)

    typer.echo(f'Adding {task} and {category}')

@app.command()
def delete(position: int):
    delete_todo(position - 1)
    typer.echo(f"Delete the {position}")

@app.command()
def update(position: int, task: str =None, category: str= None):
    typer.echo(f"Updating {position}")

@app.command()
def complete(postion: int):
    typer.echo(f"Completed {postion}")

@app.command()
def show():
    tasks = get_all_todo()
    console.print("[bold magenta]Todos[/bold magenta]!")

    table = Table(show_header=True, header_style="bold blue")
    table.add_column("#", style='dim', width=6)
    table.add_column("Tasks", min_width=20)
    table.add_column("Category", min_width=12, justify="right")
    table.add_column("Done", min_width=12, justify="right")
    table.add_column("Date Started", min_width=12, justify="right")

    def get_category_color(category):
        COLORS = {'Learn': 'cyan', 'Projects': 'red', 'Sports': 'cyan', 'Monitoring': 'green'}
        if category in COLORS:
            return COLORS[category]
        return 'white'


    for idx, task in enumerate(tasks, start=1):
        c = get_category_color(task.category)
        is_done_str = '✅' if task.status == 2 else '❌'
        table.add_row(str(idx), task.task, f"[{c}]{task.category}[/{c}]", is_done_str, task.date_added)
    
    console.print(table)

if __name__=='__main__':
    app()