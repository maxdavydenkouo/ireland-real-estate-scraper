import scraper
from fastapi import FastAPI
from pydantic import BaseModel, Field


# ===============================================================================
# app
app = FastAPI()


# ===============================================================================
# core
class Offer(BaseModel):
    id: None
    active: bool = Field()
    title: str = Field(min_length=1, max_length=100)
    publish_date: str = Field(min_length=1)
    price: str = Field(min_length=1)
    property_type: str = Field(min_length=1)
    num_bedrooms: str = Field(min_length=1)
    num_bathrooms: str = Field(min_length=1)
    seller_id: int = Field(gt=0)
    seller_name: str = Field(min_length=1)
    seller_phone: str = Field(min_length=1)
    seller_phone_extra: str = Field(min_length=1)
    seller_when_to_call: str = Field(min_length=1)
    seller_type: str = Field(min_length=1)
    images: list = Field()
    coordinates: list = Field()
    url: str = Field(min_length=1)
    category: str = Field(min_length=1)
    state: str = Field(min_length=1)



def serialize_offers(offers):
    """
    Map raw offer from scraper to the Offer object
    """
    serialized_offers = []
    for offer in offers:
        # TODO: finish
        serialized_offer = offer
        serialized_offers.append(serialized_offer)
    return serialized_offers



# ===============================================================================
# service
def scan():
    # scrap raw offers
    offers = scraper.scraping_loop(0)

    # serialize offers
    offers = serialize_offers(offers)

    # store / update offers

    # send notifications


# ===============================================================================
# controller
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/scan")
def post_scan():
    return scan()

@app.get("/offers")
def get_offers():
    return scan()