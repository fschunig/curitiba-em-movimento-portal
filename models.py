from extensions import db


class Region(db.Model):
    __tablename__ = "regions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)


class Facility(db.Model):
    __tablename__ = "facilities"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    neighborhood = db.Column(db.String)
    zip_code = db.Column(db.String)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    latitude = db.Column(db.Numeric)
    longitude = db.Column(db.Numeric)
    region_id = db.Column(db.Integer, db.ForeignKey("regions.id"))
    open_air_gym = db.Column(db.Boolean)
    updated_at = db.Column(db.DateTime)


class ClassGroup(db.Model):
    """Representa a tabela `classes` (a "turma": atividade + local + horário)."""

    __tablename__ = "classes"

    class_hash = db.Column(db.String, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"))
    facility_id = db.Column(db.Integer, db.ForeignKey("facilities.id"))
    region_id = db.Column(db.Integer, db.ForeignKey("regions.id"))
    class_name = db.Column(db.String)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    weekdays = db.Column(db.String) 
    min_age = db.Column(db.Integer)
    max_age = db.Column(db.Integer)
    first_seen_at = db.Column(db.DateTime)
    last_seen_at = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)


class AvailabilitySnapshot(db.Model):
    __tablename__ = "availability_snapshots"

    class_hash = db.Column(db.String, db.ForeignKey("classes.class_hash"), primary_key=True)
    collected_at = db.Column(db.DateTime, primary_key=True)
    availability_status = db.Column(db.String)
    enrollment_status = db.Column(db.String)
    available_slots = db.Column(db.Integer)
    pcd_available_slots = db.Column(db.Integer)
    possibly_incomplete = db.Column(db.Boolean)


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)


class ActivityCategory(db.Model):
    __tablename__ = "activity_categories"

    activity_id = db.Column(db.Integer, db.ForeignKey("activities.id"), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())