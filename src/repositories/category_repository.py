from repositories.database_helper import DatabaseHelper


class CategoryRepository(DatabaseHelper):
    
    def Get_category_id_by_name(self, categoryName):
        return self.Get_value_from_table(
            "Category", "categoryID", "categoryName", categoryName
        )
        
    def Get_category_name(self):
        self.cursor.execute(
            """ 
        SELECT categoryName FROM Category
            """,)
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]
        
