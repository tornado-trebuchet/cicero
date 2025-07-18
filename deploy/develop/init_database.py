from src.infrastructure.orm.orm_session import create_tables

def create():
    print("Creating all tables...")
    create_tables()
    print("Database initialized.")

if __name__ == "__main__":
    create()
