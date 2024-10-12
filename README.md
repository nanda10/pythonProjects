Server Setup (local)

    1. Clone the FastAPI project.
    2. pyproject.toml have all the required package. Should have poetry to install package from toml file. Run 'poetry install' which will install all packages
    3. Create .env file outside clockin folder. Add DB_URL={local_mongodb_url or atlas_mongodb_url} and DB_NAME={database name created in mongodb} attributes.
    4. Add "items" and "user_clockin_record" collection to mongodb database.
    5. Now you can run server using "uvicorn main:app" (--host and --port is optional)

Items APIs explanation

    1.  url: /items
        method: POST
        payload: {
            name: str
            email: str
            item_name: str
            quantity: int
            expiry_date: str
        }
        Endpoint is used to add item details to "items" collection.

    2.  url: /items/{item_id}
        method: GET
        Endpoint is used to fetch item details using item_id

    3.  url: /items/{item_id}
        method: PATCH
        payload: {
            name: str
            email: str
            item_name: str
            quantity: int
            expiry_date: str
        }
        Endpoint is used to update item details using item_id

    4.  url: /items/filter
        method: GET
        query_params: [email: str, quantity: int, expiry_date: str, insert_date: str]
        Endpoint is used to fetch specific item details using filters

    5.  url: /items/email-count
        method: GET
        Endpoint is used get aggregate data of no of items for each email and it will be grouped by email.

    6.  url: /items/{item_id}
        method: DELETE
        Endpoint is used delete item data using item_id

Clockin APIs explanation

    1.  url: /clock-in
        method: POST
        payload:{
            email: str
            location: ["ASIA", "AFRICA", "AUSTRALIA", "ANTARTICA", "EUROPE", "NORTH AMERICA", "SOUTH AMERICA"]
        }
        Endpoint is used to add clockin details to "user_clockin_record" collection.

    2.  url: /clock-in/{clockin_id}
        method: GET
        Endpoint is used to fetch clockin details using clockin_id

    3.  url: /clock-in/{clockin_id}
        method: PATCH
        payload: {
            email: str
            location: ["ASIA", "AFRICA", "AUSTRALIA", "ANTARTICA", "EUROPE", "NORTH AMERICA", "SOUTH AMERICA"]
        }
        Endpoint is used to update clockin details using clockin_id
    
    4.  url: /clock-in/filter
        method: GET
        query_params: [
            email: str,
            insert_datetime: str,
            location: ["ASIA", "AFRICA", "AUSTRALIA", "ANTARTICA", "EUROPE", "NORTH AMERICA", "SOUTH AMERICA"]
        ]
        Endpoint is used to fetch specific clockin details using filters
    
    5.  url: /clock-in/{clockin_id}
        method: DELETE
        Endpoint is used to delete clockin data using clockin_id


