from fastapi import FastAPI, Depends
from daftlistings import Daft, Location, SearchType, SortType
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from time import sleep
import telebot
import os.path


# ===============================================================================
# config
DB_FILE = "app.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///./{DB_FILE}"
NOTIFICATION_ON = True
BOT_ON = True
TG_TOCKEN = '6113902116:AAFVcJO8_ZgFy58dvOqtyXc5_WnD4Jk3Us4'
TG_GROUP_ID = -1001631337721


# ===============================================================================
# database

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# declarate 
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===============================================================================
# app
app = FastAPI()
daft = Daft()
bot = telebot.TeleBot(TG_TOCKEN) 


# ===============================================================================
# models
class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=False)
    state = Column(String, nullable=True)
    county = Column(String, nullable=True)
    title = Column(String, nullable=True)
    publish_date = Column(String, nullable=True)
    category = Column(String, nullable=True)
    num_bedrooms = Column(String, nullable=True)
    num_bathrooms = Column(String, nullable=True)
    size_meters_squared = Column(String, nullable=True)
    sections = Column(String, nullable=True)
    monthly_price = Column(Integer, nullable=True)
    images = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
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
    
# create db file if db file not exists
if os.path.isfile(DB_FILE) is False:
    Base.metadata.create_all(bind=engine)
    

# ===============================================================================
# service
def listing_to_offer(listing, county):
    """
    Serialize listing from daftlistings to the Offer object
    """
    listing_short = listing.as_dict_for_mapping()
    listing_raw = listing.as_dict()
    offer_dict = {
        "id": listing.id,
        "state": listing_raw['state'],
        "county": county.value['displayValue'],
        "title": listing.title,
        "publish_date": listing.publish_date,
        "category": listing.category,
        "num_bedrooms": listing_raw['numBedrooms'] if 'numBedrooms' in listing_raw else None,
        "num_bathrooms": listing_raw['numBathrooms'] if 'numBathrooms' in listing_raw else None,
        "size_meters_squared": listing.size_meters_squared,
        "sections": " / ".join(listing.sections),
        "monthly_price": listing_short['monthly_price'],
        "images": ", ".join([im['size720x480'] for im in listing.images]),
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


def check_and_notify(db, offers, county):
    # ignore empty db situation
    if db.query(Offer.id).count() == 0:
        return None

    # ----------------------------------------
    # check
    # get published offers id and price
    result = db.query(Offer.id, Offer.monthly_price).filter(Offer.state == 'PUBLISHED', Offer.county == county.value['displayValue']).all()
    db_offers_id_price = {}
    for db_offer in result:
        db_offer = db_offer._mapping
        db_offers_id_price[db_offer['id']] = db_offer['monthly_price']

    # offers new
    # offers, which exists in server response, but not exists in published db offers list
    offers_new = []
    for offer in offers:
        if offer.id not in db_offers_id_price:
            offers_new.append(offer)

    # offers changed
    # offers, which exists in server response, and exists in published db offers list, but have another price
    offers_upd = []
    for offer in offers:
        if offer.id in db_offers_id_price and offer.monthly_price != db_offers_id_price[offer.id]:
            offers_upd.append(offer)

    # disable disabled offers
    offers_off = []
    offers_ids = [offer.id for offer in offers]
    for db_offer_id in db_offers_id_price:
        if int(db_offer_id) not in offers_ids:
            offers_off.append(db_offer_id)
    
    for disable_id in offers_off:
        offer = db.query(Offer).filter(Offer.id == disable_id).first()
        offer.state = 'PAUSED'
    db.commit()

    # ----------------------------------------
    # notify
    notify_new_offers(offers_new, county)
    notify_changed_offers(offers_upd, db_offers_id_price, county)


def dict_to_string(dict_msg):
    msg_rows = []
    for key in dict_msg:
        if dict_msg[key] is None:
            dict_msg[key] = ""
        msg_rows.append(f'- {key}: {dict_msg[key]}')
    return "\n".join(msg_rows)


def generate_message(msg_type, offer, county, old_monthly_price=None):
    property_info = {
        "type": offer.property_type,
        "title": offer.title,
        'county': county.value['displayName'],
        "price (month)": str(offer.monthly_price) + " €",
        "price (month) (old)": str(old_monthly_price) + " €",
        "bedrooms": offer.num_bedrooms,
        "bathrooms": offer.num_bathrooms,
        "latitude": offer.latitude,
        "longitude": offer.longitude,
        "rating": offer.rating,
        "published": offer.publish_date,
        "url": offer.url,
    }

    # remove old price for NEW offers
    if old_monthly_price is None:
        del property_info['price (month) (old)']

    seller = {
        "name": offer.seller_name,
        "phone": offer.seller_phone,
        "phone_alt": offer.seller_phone_alt,
        "when_to_call": offer.seller_when_to_call,
    }

    # construct the message
    msg = f"{msg_type} [{offer.id}]\n\n<b>property:</b>\n{dict_to_string(property_info)}\n\n<b>contacts:</b>\n{dict_to_string(seller)}"
    return msg


def notify_new_offers(offers, county):
    for offer in offers:
        msg = generate_message("NEW", offer, county)
        send_notification(msg)


def notify_changed_offers(offers, db_offers_id_price, county):
    for offer in offers:
        old_monthly_price = db_offers_id_price[offer.id]
        msg = generate_message("UPD", offer, county, old_monthly_price)
        send_notification(msg)


def send_notification(msg):
    if BOT_ON:
        bot.send_message(TG_GROUP_ID, msg, parse_mode='html')


def store_offers(db: Session, offers: list):
    print('merge offers')
    for offer in offers:
        db.merge(offer)
    db.commit()


def update_offers_service(db: Session):
    """
    Update offers service and send notifications
    """
    global NOTIFICATION_ON

    counties = [
        Location.DONEGAL
    ]

    for county in counties:
        # scrap listings from daft
        daft.set_location(county)
        daft.set_search_type(SearchType.RESIDENTIAL_RENT)
        daft.set_sort_type(SortType.PUBLISH_DATE_DESC)
        listings = daft.search()

        # disable notification procedure with empty db of processed county
        if db.query(Offer).filter(Offer.county == county.value['displayValue']).first() is None:
           NOTIFICATION_ON = False 

        # serialize listings to offers
        offers = [listing_to_offer(listing, county) for listing in listings]

        # check and send notifications
        if NOTIFICATION_ON:
            check_and_notify(db, offers, county)

        # store / update offers
        store_offers(db, offers)

        sleep(10)


# ===============================================================================
# controller
@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/offers")
async def get_offers(db: Session = Depends(get_db)):
    db_offers = db.query(Offer).all()
    return db_offers


@app.post("/search")
def update_offers(db: Session = Depends(get_db)):
    """
    Update db offers and send notifications
    """
    return update_offers_service(db)