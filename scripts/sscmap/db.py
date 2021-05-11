from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DataRecord(Base):
    __tablename__ = "data_records"

    data_id = Column(String, primary_key=True)
    technology = Column(String, index=True)
    species = Column(String, index=True)
    tissue = Column(String, index=True)
    disease = Column(String, index=True)
    disease_subtype = Column(String, index=True)
    molecule = Column(String, index=True)
    source_name = Column(String)
    source_url = Column(String)
    journal = Column(String)
    year = Column(Integer, index=True)
    resolution = Column(Integer, index=True)
    cell_count = Column(Integer, index=True)
    marker_count = Column(Integer, index=True)
    has_cell_type = Column(Boolean, index=True)


class DataStats(Base):
    __tablename__ = "data_stats"

    data_id = Column(String, primary_key=True)
    cell_components = Column(String)
    cell_density = Column(String)
    co_expression = Column(String)
    cell_interaction = Column(String)


class CellInfo(Base):
    __tablename__ = "cell_info"

    roi_id = Column(String, primary_key=True)
    data_id = Column(String, index=True)
    cell_x = Column(ARRAY(Float))
    cell_y = Column(ARRAY(Float))
    cell_type = Column(ARRAY(String))
    cell_name = Column(ARRAY(Integer))
    neighbor_one = Column(ARRAY(Integer))
    neighbor_two = Column(ARRAY(Integer))
    markers = Column(ARRAY(String))


class CellExp(Base):
    __tablename__ = "cell_exp"

    id = Column(Integer, primary_key=True)
    roi_id = Column(String, index=True)
    data_id = Column(String, index=True)
    marker = Column(String)
    expression = Column(ARRAY(Float))


class ROIInfo(Base):
    __tablename__ = "roi_info"

    roi_id = Column(String, primary_key=True)
    data_id = Column(String, index=True)
    header = Column(ARRAY(String))
    meta = Column(ARRAY(String))
    shannon_entropy = Column(Float)
    altieri_entropy = Column(Float)


def init_db(engine):
    Base.metadata.create_all(engine)
