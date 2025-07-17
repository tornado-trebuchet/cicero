from src.infrastructure.orm.orm_session import engine
from sqlalchemy import text

def reset_database():
    print("Dropping all tables with CASCADE...")
    with engine.connect() as conn:
        # Drop all tables in the public schema with CASCADE
        conn.execute(text('''
            DO $$ DECLARE
                r RECORD;
            BEGIN
                -- Drop all tables
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        '''))
        conn.commit()
    print("Database reset complete.")

if __name__ == "__main__":
    reset_database()
