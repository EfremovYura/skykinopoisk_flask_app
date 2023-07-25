from sqlalchemy import text, desc
from setup_db import db
from constants import ITEMS_PER_PAGE


class DAO:
    def __init__(self, session: db.session, model: db.Model):
        self.session = session
        self.model = model

    def get_one(self, oid: int) -> db.Model:
        m_object = self.session.query(self.model).get(oid)
        return m_object

    def get_all(self) -> list[db.Model]:
        m_objects = self.session.query(self.model).all()

        return m_objects

    def get_all_page(self, page: int) -> list[db.Model]:
        m_objects = self.session.query(self.model).paginate(page, per_page=ITEMS_PER_PAGE).items

        return m_objects

    def get_all_new(self) -> list[db.Model]:
        m_objects = self.session.query(self.model).order_by(self.model.id.desc()).all()

        return m_objects

    def get_all_new_page(self, page: int) -> list[db.Model]:
        m_objects = self.session.query(self.model).order_by(desc(self.model.id)). \
            paginate(page, per_page=ITEMS_PER_PAGE).items

        return m_objects

    def get_filtered(self, text_filter: str) -> list[db.Model]:
        m_objects = self.session.query(self.model).filter(text(text_filter)).all()
        return m_objects

    def get_filtered_new(self, text_filter: str) -> list[db.Model]:
        m_objects = self.session.query(self.model).filter(text(text_filter)).order_by(self.model.id.desc()).all()
        return m_objects

    def get_filtered_page(self, text_filter: str, page: int) -> list[db.Model]:
        m_objects = self.session.query(self.model).filter(text(text_filter)). \
            paginate(page, per_page=ITEMS_PER_PAGE).items
        return m_objects

    def get_filtered_new_page(self, text_filter: str, page: int) -> list[db.Model]:
        m_objects = self.session.query(self.model).filter(text(text_filter)).order_by(self.model.id.desc()). \
            paginate(page, per_page=ITEMS_PER_PAGE).items
        return m_objects

    def update(self, m_object: db.Model) -> db.Model:
        self.session.add(m_object)
        self.session.commit()

        return m_object

    def delete(self, m_object: db.Model) -> db.Model:
        self.session.delete(m_object)
        self.session.commit()

        return m_object

    def create(self, data: dict) -> db.Model:
        m_object = self.model(**data)

        self.session.add(m_object)
        self.session.commit()

        return m_object
