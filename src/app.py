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
VERBOSE = True
TG_TOCKEN = '6113902116:AAFVcJO8_ZgFy58dvOqtyXc5_WnD4Jk3Us4'
TG_GROUP_ID = -1001830526147
COUNTIES = [
    {"tg_topic_id": 3,     "active": False,    "location": Location.DONEGAL},
    {"tg_topic_id": 35,    "active": True,    "location": Location.WICKLOW},
    {"tg_topic_id": 34,    "active": True,    "location": Location.DOWN},
    {"tg_topic_id": 32,    "active": False,    "location": Location.GALWAY},
    {"tg_topic_id": 31,    "active": False,    "location": Location.LONGFORD},
    {"tg_topic_id": 30,    "active": False,    "location": Location.ROSCOMMON},
    {"tg_topic_id": 29,    "active": False,    "location": Location.ANTRIM},
    {"tg_topic_id": 28,    "active": False,    "location": Location.TIPPERARY},
    {"tg_topic_id": 27,    "active": False,    "location": Location.MONAGHAN},
    {"tg_topic_id": 26,    "active": False,    "location": Location.KILDARE},
    {"tg_topic_id": 25,    "active": False,    "location": Location.WEXFORD},
    {"tg_topic_id": 24,    "active": False,    "location": Location.LEITRIM},
    {"tg_topic_id": 23,    "active": False,    "location": Location.OFFALY},
    {"tg_topic_id": 22,    "active": False,    "location": Location.LOUTH},
    {"tg_topic_id": 21,    "active": False,    "location": Location.SLIGO},
    {"tg_topic_id": 20,    "active": False,    "location": Location.WESTMEATH},
    {"tg_topic_id": 19,    "active": False,    "location": Location.LAOIS},
    {"tg_topic_id": 18,    "active": False,    "location": Location.CARLOW},
    {"tg_topic_id": 17,    "active": False,    "location": Location.KILKENNY},
    {"tg_topic_id": 16,    "active": False,    "location": Location.FERMANAGH},
    {"tg_topic_id": 15,    "active": False,    "location": Location.CAVAN},
    {"tg_topic_id": 14,    "active": False,    "location": Location.MAYO},
    {"tg_topic_id": 13,    "active": False,    "location": Location.LIMERICK},
    {"tg_topic_id": 12,    "active": False,    "location": Location.KERRY},
    {"tg_topic_id": 11,    "active": False,    "location": Location.MEATH},
    {"tg_topic_id": 5,     "active": False,    "location": Location.CLARE},
    {"tg_topic_id": 4,     "active": False,    "location": Location.CORK},
    {"tg_topic_id": 2,     "active": False,    "location": Location.DUBLIN},
    {"tg_topic_id": 112,   "active": False,    "location": Location.WATERFORD},
]

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
        "state": listing_raw['state'] if 'state' in listing_raw else None,
        "county": county.value['displayValue'],
        "title": listing.title,
        "publish_date": listing.publish_date,
        "category": listing.category,
        "num_bedrooms": listing_raw['numBedrooms'] if 'numBedrooms' in listing_raw else None,
        "num_bathrooms": listing_raw['numBathrooms'] if 'numBathrooms' in listing_raw else None,
        "size_meters_squared": listing.size_meters_squared,
        "sections": " / ".join(listing.sections) if listing.sections is not None else None,
        "monthly_price": listing_short['monthly_price'],
        "images": ", ".join([im['size720x480'] for im in listing.images]) if listing.images is not None else None,
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
    result = db.query(Offer.id, Offer.monthly_price).filter(Offer.state == 'PUBLISHED', Offer.county == county['location'].value['displayValue']).all()
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

    if VERBOSE:
        print(f"new offers [{len(offers_new)}]: {', '.join([str(offer.id) for offer in offers_new])}")
        print(f"upd offers [{len(offers_upd)}]: {', '.join([str(offer.id) for offer in offers_upd])}")
        print(f"off offers [{len(offers_off)}]: {', '.join([str(offer_id) for offer_id in offers_off])}")

    # ----------------------------------------
    # notify
    notify_new_offers(offers_new, county)
    notify_changed_offers(offers_upd, db_offers_id_price, county)


def dict_to_string(dict_msg):
    msg_rows = []
    for key in dict_msg:
        if dict_msg[key] is not None and dict_msg[key] != "" and dict_msg[key] != "None":
            msg_rows.append(f'{key} {dict_msg[key]}')
    return "\n".join(msg_rows)


def generate_message(msg_type, offer, county, old_monthly_price=None):
    # NOT USED (keep as reference)
    """
    property_info_old = {
        "type": offer.property_type,
        "Address": offer.title,
        'county': county['location'].value['displayName'],
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
    """

    old_monthly_price_str = f' (€{old_monthly_price} - old price)' if old_monthly_price is not None else ""
    main_propery_info_list = [offer.num_bedrooms, offer.num_bathrooms, offer.property_type]
    main_propery_info_str = ", ".join([el for el in main_propery_info_list if el is not None])
    property_info = {
        "💰": f'€{offer.monthly_price} per month{old_monthly_price_str}', # HACK
        "🏠": main_propery_info_str,
        #"🗓": "...", # lease - disable temporarily
    }

    if offer.latitude is not None and offer.longitude is not None:
        map_info = {
            "🛰": f"<a href='https://www.google.com/maps?t=k&q=loc:{offer.latitude}+{offer.longitude}'>Satellite view</a>",
            "🗺": f"<a href='https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={offer.latitude},{offer.longitude}'>Street view</a>",
        }
    else:
        map_info is None

    if offer.seller_name is not None or offer.seller_phone is not None:
        phone_alt_str = f' ({offer.seller_phone_alt})' if offer.seller_phone_alt is not None else ""
        seller_info = {
            "👤": offer.seller_name,
            "📞": f'{offer.seller_phone}{phone_alt_str}',
            "🕗": offer.seller_when_to_call,
        }
    else:
        seller_info = None

    # construct the message
    msg = f"{msg_type}: <a href='{offer.url}'>{offer.title}</a>\n\n{dict_to_string(property_info)}"
    if map_info is not None:
        msg = msg + f"\n\n{dict_to_string(map_info)}"
    if seller_info is not None:
        msg = msg + f"\n\n{dict_to_string(seller_info)}"

    return msg


def notify_new_offers(offers, county):
    for offer in offers:
        msg = generate_message("NEW", offer, county)
        send_notification(msg, county)


def notify_changed_offers(offers, db_offers_id_price, county):
    for offer in offers:
        old_monthly_price = db_offers_id_price[offer.id]
        msg = generate_message("UPD", offer, county, old_monthly_price)
        send_notification(msg, county)


def send_notification(msg, county):
    if BOT_ON:
        bot.send_message(TG_GROUP_ID, msg, parse_mode='html', reply_to_message_id=county['tg_topic_id'])


def store_offers(db: Session, offers: list):
    print('merge offers')
    for offer in offers:
        db.merge(offer)
    db.commit()


def update_offers_service(db: Session):
    """
    Update offers service and send notifications
    """
    for county in COUNTIES:
        # ignore disabled counties
        if county['active'] is False:
            continue

        if VERBOSE:
            print(f"handle {county['location'].value['displayValue']}")

        # scrap listings from daft
        daft = Daft()
        daft.set_location(county['location'])
        daft.set_search_type(SearchType.RESIDENTIAL_RENT)
        daft.set_sort_type(SortType.PUBLISH_DATE_DESC)
        listings = daft.search()

        # disable notification procedure with empty db of processed county
        if db.query(Offer).filter(Offer.county == county['location'].value['displayValue']).first() is None:
            # TODO: refactor notification logic to exclude confusing vars
            # DESCRIPTION: if global notification param is ON - apply notifications
            # only when db offers by county exists, in other case fill db without notifications 
            notification_on = False
        else:
            notification_on = NOTIFICATION_ON

        # serialize listings to offers
        offers = [listing_to_offer(listing, county['location']) for listing in listings]

        # check and send notifications
        if notification_on:
            check_and_notify(db, offers, county)

        # store / update offers
        store_offers(db, offers)

        sleep(10)


def request_single_offer(db):
    # DEBUG: for debug purpose
    offer = db.query(Offer).filter(Offer.id == 4732790).first()
    county = {"tg_topic_id": 35,    "active": False,     "location": Location.WICKLOW}
    return notify_new_offers([offer], county)


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
def scan_offers(db: Session = Depends(get_db)):
    """
    Update db offers and send notifications
    """
    return update_offers_service(db)