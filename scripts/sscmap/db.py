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
    markers = Column(ARRAY(String))
    molecular = Column(String, index=True)
    source_name = Column(String)
    source_url = Column(ARRAY(String))
    journal = Column(String)
    level_name = Column(ARRAY(String))
    level_count = Column(ARRAY(Integer))
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
    spatial_distribution = Column(String)
    entropy_shannon = Column(String)
    entropy_altieri = Column(String)


class CellInfo(Base):
    __tablename__ = "cell_info"

    cell_id = Column(String, primary_key=True)
    cell_x = Column(Float)
    cell_y = Column(Float)
    cell_type = Column(String)
    expression = Column(ARRAY(Float))
    roi_id = Column(String, index=True)
    data_id = Column(String, index=True)


class GroupLevel(Base):
    __tablename__ = "group_level"

    roi_id = Column(String, primary_key=True)
    data_id = Column(String, index=True)
    levels_table = Column(String)


def init_db(engine):
    Base.metadata.create_all(engine)
