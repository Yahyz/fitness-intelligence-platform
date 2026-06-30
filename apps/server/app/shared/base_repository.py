from sqlalchemy.orm import Session


class BaseRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def add(self, entity):
        self.db.add(entity)
        self.db.flush()
        return entity

    def flush(self):
        self.db.flush()

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()