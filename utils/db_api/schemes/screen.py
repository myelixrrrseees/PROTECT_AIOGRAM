from sqlalchemy import Column, BigInteger, String, sql, Float, Sequence

from utils.db_api.db_gino import TimedBaseModel


class Screen(TimedBaseModel):
    __tablename__ = 'screen'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    screen_name = Column(String(300))
    screen_id = Column(String(300))
    status = Column(String(30))

    query: sql.select

