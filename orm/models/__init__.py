from orm.database import Base, engine
from orm.models.payload import Payload
from orm.models.region import Region
from orm.models.sub_variant import SubVariant
from orm.models.variant import Variant

Base.metadata.create_all(engine)
