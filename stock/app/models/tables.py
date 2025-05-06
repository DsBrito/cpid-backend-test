from sqlalchemy import BigInteger, String, Integer, Float, Date, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.settings.database import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "product"

    id: Mapped[BigInteger] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[String] = mapped_column(String(50), nullable=False)
    description: Mapped[String] = mapped_column(String(100))
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    current_date: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    manufacture_date: Mapped[Date] = mapped_column(Date, nullable=False)
    expiration_date: Mapped[Date] = mapped_column(Date, nullable=True)
    brand: Mapped[str] = mapped_column(String(50), nullable=True)
    supplier: Mapped[str] = mapped_column(String(100), nullable=True)
    code: Mapped[int] = mapped_column(BigInteger, default=lambda: int(datetime.utcnow().timestamp() * 1000), nullable=False)



class Moviment(Base):
    __tablename__ = "moviment"

    id: Mapped[BigInteger] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )
    product_name: Mapped[String] = mapped_column(String(50), nullable=False)
    moviment_type: Mapped[String] = mapped_column(String(50), nullable=False)
    moviment_reason: Mapped[String] = mapped_column(String(50), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    movement_responsible: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

