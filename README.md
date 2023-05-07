# description
Service for scraping https://www.daft.ie/property-for-rent/donegal and sending tg notifications about new propositions.

# functionality
- parse daft site by city
- collect offers
- store offers
- notify users in tg via bot about fresh ones

# plan
[x] basic scraping functionality
[x] full autonomous scraping by city page by page
[ ] fastapi infrastructure (> service should have runtime)
[ ] store elements
[ ] intelligent crontab (try to get only fresh elements)
[ ] notifications
    [ ] tg bot integration
    [ ] notification view
    [ ] rules for chose which offers should push
[ ] tests
[ ] refactor
[ ] wishes
    [x] fastapi infrastructure
    [ ] sqlalchemy
    [ ] pydantic
    [ ] logging
    [ ] testing