import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='conversions.db'):
        self.db_name = db_name
        self.init_database()

    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create conversions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_text TEXT NOT NULL,
                output_text TEXT NOT NULL,
                direction TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create users table (for future expansion)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create settings table (for future expansion)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                default_separator TEXT DEFAULT '/',
                theme TEXT DEFAULT 'light',
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        conn.commit()
        conn.close()

    def save_conversion(self, input_text, output_text, direction):
        """Save a conversion to database"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO conversions (input_text, output_text, direction)
            VALUES (?, ?, ?)
        ''', (input_text, output_text, direction))

        conn.commit()
        conversion_id = cursor.lastrowid
        conn.close()

        return conversion_id

    def get_conversions(self, limit=50, offset=0):
        """Get conversion history"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, input_text, output_text, direction,
                   strftime('%Y-%m-%d %H:%M:%S', timestamp) as timestamp
            FROM conversions
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        ''', (limit, offset))

        conversions = cursor.fetchall()
        conn.close()

        return conversions

    def get_conversion_by_id(self, conversion_id):
        """Get specific conversion by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT id, input_text, output_text, direction,
                   strftime('%Y-%m-%d %H:%M:%S', timestamp) as timestamp
            FROM conversions
            WHERE id = ?
        ''', (conversion_id,))

        conversion = cursor.fetchone()
        conn.close()

        return conversion

    def delete_conversion(self, conversion_id):
        """Delete a conversion by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM conversions WHERE id = ?', (conversion_id,))
        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()

        return deleted

    def clear_all_conversions(self):
        """Clear all conversion history"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM conversions')
        conn.commit()
        conn.close()

        return True

    def get_statistics(self):
        """Get conversion statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Total conversions
        cursor.execute('SELECT COUNT(*) FROM conversions')
        total = cursor.fetchone()[0]

        # Conversions by direction
        cursor.execute('''
            SELECT direction, COUNT(*) as count
            FROM conversions
            GROUP BY direction
        ''')
        by_direction = {row[0]: row[1] for row in cursor.fetchall()}

        # Recent conversions (last 24 hours)
        cursor.execute('''
            SELECT COUNT(*)
            FROM conversions
            WHERE timestamp > datetime('now', '-1 day')
        ''')
        recent = cursor.fetchone()[0]

        conn.close()

        return {
            'total_conversions': total,
            'by_direction': by_direction,
            'recent_24h': recent
        }

    # User management functions (for future expansion)
    def create_user(self, username, password_hash):
        """Create a new user"""
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO users (username, password_hash)
                VALUES (?, ?)
            ''', (username, password_hash))
            conn.commit()
            user_id = cursor.lastrowid

            # Create default settings for user
            cursor.execute('''
                INSERT INTO settings (user_id)
                VALUES (?)
            ''', (user_id,))
            conn.commit()

            return user_id
        except sqlite3.IntegrityError:
            return None  # Username already exists
        finally:
            conn.close()

    def get_user(self, username):
        """Get user by username"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        return user

# Singleton instance
db = Database()
