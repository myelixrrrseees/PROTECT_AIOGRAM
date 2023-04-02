from sqlalchemy import Column, BigInteger, String, sql, Float, Sequence

from utils.db_api.db_gino import TimedBaseModel


class Withdraw(TimedBaseModel):
    __tablename__ = 'withdraw'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    amount = Column(Float)
    photo_name = Column(String(300))
    photo_id = Column(String(300))
    status = Column(String(60))

    query: sql.select

