
def dictfetchall(cursor):
    """
    Returns all rows from a cursor as a dict
    
    @see https://docs.djangoproject.com/en/dev/topics/db/sql/
    """
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]