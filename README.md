# description
Service for scraping https://www.daft.ie/property-for-rent/donegal and sending tg notifications about new propositions.

# functionality
- parse daft site by city
- collect offers
- store offers
- notify users in tg via bot about fresh ones

# plan
- [x] basic scraping functionality
- [x] full autonomous scraping by city page by page
- [x] fastapi infrastructure (> service should have runtime)
- [x] raplace scraper on daftlisting python package
- [x] sqlalchemy implementation
- [x] daftlisting to offer serialization
- [x] store elements
- [x] check parsed elements and mark for nofications
- [x] notifications
    - [x] tg bot integration
    - [x] notification view
    - [x] set up bot on group with topics
    - [x] add new counties
- [x] edit view
- [x] crontab
- [ ] deploy
- [ ] wishes
    - [x] fastapi infrastructure
    - [x] sqlalchemy
    - [ ] pydantic
    - [ ] logging
    - [ ] testing
    - [ ] refactor

# notes
1. Config param to show only published items. (published / paused)
If remove 'values' key - service will show all elements
```json
"filters": [
    {
      "name": "adState",
      "values": [
        "published"
      ]
    }
  ],
```
