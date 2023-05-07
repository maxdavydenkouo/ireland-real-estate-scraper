# description
Service for parsing https://www.daft.ie/property-for-rent/donegal and sending tg notifications about new propositions.

# functionality
- parse daft site by city
- collect offers
- store offers
- notify users in tg via bot about fresh ones

# plan
[x] basic parsing functionality
[ ] full autonomous parsing by city
[ ] store elements
[ ] fastapi infrastructure (> service should have runtime)
[ ] intelligent crontab (try to get only fresh elements)
[ ] notifications
    [ ] tg bot integration
    [ ] notification view
    [ ] rules for chose which offers should push
[ ] wishes
    [x] fastapi infrastructure
    [ ] sqlalchemy
    [ ] pydantic
    [ ] logging
    [ ] testing