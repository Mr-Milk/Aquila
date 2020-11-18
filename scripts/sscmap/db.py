from sqlalchemy import Column, Float, String
from sqlalchemy.dialects.postgresql import ARRAY, JSON, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.indexable import index_property

Base = declarative_base()


class DataRecord(Base):
    __tablename__ = "data_records"

    data_id = Column(String, primary_key=True)
    data_meta = Column(JSON)

    tissue = index_property("data_meta", "tissue")
    disease = index_property("data_meta", "disease")
    disease_subtype = index_property("data_meta", "disease_subtype")
    molecular = index_property("data_meta", "molecular")
    year = index_property("data_meta", "year")
    resolution = index_property("data_meta", "resolution")
    cell_count = index_property("data_meta", "cell_count")
    marker_count = index_property("data_meta", "marker_count")


class DataStats(Base):
    __tablename__ = "data_stats"

    data_id = Column(String, primary_key=True)
    cell_components = Column(JSON)
    cell_density = Column(JSON)
    spatial_distribution = Column(JSON)
    entropy_shannon = Column(JSON)
    entropy_altieri = Column(JSON)


class CellInfo(Base):
    __tablename__ = "cell_info"

    cell_id = Column(UUID, primary_key=True)
    cell_x = Column(String)
    cell_y = Column(String)
    cell_type = Column(String)
    roi_id = Column(UUID)
    data_id = Column(String)


class CellExpression(Base):
    __tablename__ = "cell_expression"

    cell_id = Column(UUID, primary_key=True)
    expression = Column(ARRAY(Float))
    roi_id = Column(UUID, index=True)
    data_id = Column(String, index=True)


class GroupLevel(Base):
    __tablename__ = "group_level"

    data_id = Column(String, primary_key=True)
    levels_table = Column(JSON)


def init_db(engine):
    Base.metadata.create_all(engine)
