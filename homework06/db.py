# mypy: ignore-errors
from sqlalchemy import Column, Integer, String, create_engine  # mypy: ignore
from sqlalchemy.ext.declarative import declarative_base  # mypy: ignore
from sqlalchemy.orm import sessionmaker  # mypy: ignore

from scraputils import get_news


def create_database(lst):
    s = session()
    slovar_nov = {"title": "None", "url": "None", "author": "None", "points": 0, "comments": 0}
    for slovar in lst:
        if slovar != slovar_nov:
            new = News(
                title=slovar["title"],
                author=slovar["author"],
                url=slovar["url"],
                comments=slovar["comments"],
                points=slovar["points"],
            )
            s.add(new)
            s.commit()


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    url = "https://news.ycombinator.com/"
    news_list = get_news(url, n_pages=34)
    create_database(news_list)
