from fastapi import FastAPI, Depends
from daftlistings import Daft, Location, SearchType, PropertyType, Listing
from sqlalchemy import create_engine, Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from pprint import pprint

# ===============================================================================
# database
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declarate 
Base = declarative_base()


# ===============================================================================
# app
app = FastAPI()
daft = Daft()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===============================================================================
# models
class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    state = Column(String, nullable=True)
    title = Column(String, nullable=True)
    publish_date = Column(String, nullable=True)
    category = Column(String, nullable=True)
    num_bedrooms = Column(String, nullable=True)
    num_bathrooms = Column(String, nullable=True)
    size_meters_squared = Column(String, nullable=True)
    sections = Column(String, nullable=True)
    monthly_price = Column(String, nullable=True)
    images = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    url = Column(String, nullable=True)
    featured_level = Column(String, nullable=True)
    sale_type = Column(String, nullable=True)
    rating = Column(String, nullable=True)
    property_type = Column(String, nullable=True)
    seller_id = Column(Integer, nullable=True)
    seller_name = Column(String, nullable=True)
    seller_phone = Column(String, nullable=True)
    seller_phone_alt = Column(String, nullable=True)
    seller_when_to_call = Column(String, nullable=True)
    seller_type = Column(String, nullable=True)
    

# create db
#Base.metadata.create_all(bind=engine)


# ===============================================================================
# service
def listing_to_offer(listing):
    """
    Serialize listing from daftlistings to the Offer object
    """
    listing_short = listing.as_dict_for_mapping()
    listing_raw = listing.as_dict()
    offer_dict = {
        "id": listing.id,
        "state": listing_raw['state'],
        "title": listing.title,
        "publish_date": listing.publish_date,
        "category": listing.category,
        "num_bedrooms": listing_raw['numBedrooms'] if 'numBedrooms' in listing_raw else None,
        "num_bathrooms": listing_raw['numBathrooms'] if 'numBathrooms' in listing_raw else None,
        "size_meters_squared": listing.size_meters_squared,
        "sections": " / ".join(listing.sections),
        "monthly_price": listing_short['monthly_price'],
        "images": ",".join([im['size720x480'] for im in listing.images]),
        "latitude": listing.latitude,
        "longitude": listing.longitude,
        "url": listing.daft_link,
        "featured_level": listing.featured_level,
        "sale_type": " / ".join(listing_raw['saleType']) if 'saleType' in listing_raw else None,
        "rating": listing_raw['ber']['rating'] if 'ber' in listing_raw else None,
        "property_type": listing_raw['propertyType'] if 'propertyType' in listing_raw else None,
        "seller_id": listing.agent_id,
        "seller_name": listing.agent_name,
        "seller_phone": listing_raw['seller']['phone'].strip() if 'phone' in listing_raw['seller'] else None,
        "seller_phone_alt": listing_raw['seller']['alternativePhone'].strip() if 'alternativePhone' in listing_raw['seller'] else None,
        "seller_when_to_call": listing_raw['seller']['phoneWhenToCall'] if 'phoneWhenToCall' in listing_raw['seller'] else None,
        "seller_type": listing.agent_seller_type,
    }
    return Offer(**offer_dict)


def check_and_notify(offers, db_offers):
    # TODO
    # ignore empty db situation
    if len(db_offers) == 0:
        return None
    pass


def store_offers(db: Session, offers: list):
    print('merge offers')
    for offer in offers:
        db.merge(offer)
    db.commit()


def update_offers_service(db: Session):
    """
    Update offers service and send notifications
    """

    # scrap listings from daft
    daft.set_location(Location.DONEGAL)
    daft.set_search_type(SearchType.RESIDENTIAL_RENT)
    listings = daft.search()

    # serialize listings to offers
    offers = [listing_to_offer(listing) for listing in listings]

    # get db offers    
    db_offers = db.query(Offer).all()

    # check and send notifications
    #check_and_notify(offers, db_offers)

    # store / update offers
    store_offers(db, offers)

    return len(offers)


# ===============================================================================
# controller
@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/offers")
async def get_offers(db: Session = Depends(get_db)):
    db_offers = db.query(Offer).all()
    return db_offers


@app.get("/offers_test")
async def get_offers_test():
    offer_dict = {
        "id": 124,
        "title": "some"
    }
    offer = Offer(**offer_dict)
    return offer


@app.post("/search")
def update_offers(db: Session = Depends(get_db)):
    """
    Update db offers and send notifications
    """
    return update_offers_service(db)