# description
MVP Service for scraping real estate rent offers from https://www.daft.ie and sending tg notifications about new and changed propositions, with using daftlisting (https://github.com/AnthonyBloomer/daftlistings)

# functionality
- scrap info from https://www.daft.ie via daftlisting
- aggregate offers
- notify users in tg via bot about new/upd ones

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
- [x] deploy
- [ ] logging (+ reattach raw stdoutput logging info)
- [ ] testing
- [ ] refactor
  - [ ] global refactor
  - [ ] put sleep timings to config 
- [ ] wishes
    - [x] fastapi
    - [x] sqlalchemy
    - [ ] pydantic


# notes
1. Config param to daft endpoint to show offers by status type. Values = [published / paused / all]
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

# links
- daftlisting (https://github.com/AnthonyBloomer/daftlistings)