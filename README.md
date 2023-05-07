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
[x] fastapi infrastructure (> service should have runtime)
[ ] sqlalchemy
[ ] store elements
[ ] check parsed elements and mark for nofications
[ ] notifications
    [ ] tg bot integration
    [ ] notification view
[ ] crontab
[ ] tests
[ ] refactor
[ ] wishes
    [x] fastapi infrastructure
    [ ] sqlalchemy
    [ ] pydantic
    [ ] logging
    [ ] testing