from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.sql import func
from ai_exam_system.database import Base

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    roll_number = Column(String(50), index=True)
    student_answers = Column(Text)
    evaluation = Column(Text)
    confidence = Column(String(20))
    final_score = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
