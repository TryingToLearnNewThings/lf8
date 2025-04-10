import sqlite3


class DatabaseHelper:
    def __init__(self, db="./Database/database.db", connection=None):
        # Connection is being established if none has been transferred
        if connection:
            self.con = connection
        else:
            self.db_path = db
            self.con = sqlite3.connect(self.db_path)

        # Cursor is used for queries
        self.cursor = self.con.cursor()

    def Get_value_from_table(self, table, column, condition_column, condition_value):

        self.cursor.execute(
            f""" 
        SELECT {column} FROM {table} WHERE {condition_column} = ? 
        """,
            (condition_value,),
        )
        result = self.cursor.fetchall()

        if result:
            # If only one line with a value was returned
            if len(result) == 1 and len(result[0]) == 1:
                return result[0][0]  # Returns the single value

            # If several lines were returned but only one tuple is required
            return tuple(result[0]) if len(result) == 1 else tuple(result)

        return None  # If no value was found

    def Update_field_value(self, table, update_field, new_value, id, idField):
        self.cursor.execute(
            f"""UPDATE {table} SET {update_field} = ? WHERE {idField} = ?""",
            (
                new_value,
                id,
            ),
        )
        self.con.commit()
        return print(f"For Player {id}, {table, id} has been updated")
