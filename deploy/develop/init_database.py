from src.infrastructure.orm.orm_session import create_tables

def main():
    print("Creating all tables...")
    create_tables()
    print("Database initialized.")

if __name__ == "__main__":
    main()
