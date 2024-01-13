import logging
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Literal

from ebaysdk.finding import Connection as Finding
from ebaysdk.exception import ConnectionError
from pydantic import ValidationError
from API.validators import RecommendedProduct
from dataclasses import dataclass
from typing import Optional, Dict, Union

# Set up logging
logging.basicConfig(level=logging.INFO)


# dataclasses with slots=True, frozen=True, init=True are used because they are much more optimized than the usual classes
# In our case, they are not yet variable, because they only accept data when created and do not need to be changed anymore, something like a tuple
@dataclass(frozen=True, init=True)
class Category:
    name: str
    min_age: int
    max_age: int
    min_budget: int
    max_budget: int
    hobbies: List[str]
    gender: Literal[0, 1, 2]
    event: str


categories = [
    Category("Bicycle", 3, 100, 95, 8750, ["Sport"], 0, "any"),
    Category("Bicycle accessories", 3, 100, 2, 1100, ["Sport"], 0, "any"),
    Category("Electric scooter", 3, 100, 200, 3775, ["Sport"], 0, "any"),
    Category("Diving mask", 3, 100, 20, 125, ["Sport"], 0, "any"),
    Category("Orbitrek", 3, 100, 50, 400, ["Sport"], 0, "any"),
    Category("Exercise bike", 3, 100, 75, 1000, ["Sport", "homebody"], 0, "any"),
    Category("Big tennis rackets", 6, 100, 19, 475, ["Sport"], 0, "any"),
    Category("Balls", 3, 100, 3, 263, ["Sport"], 0, "any"),
    Category("Dumbbells", 12, 100, 10, 200, ["Sport"], 0, "any"),
    Category("Fitness bracelet", 3, 100, 5, 40, ["Sport"], 0, "any"),
    Category("Game console", 3, 100, 200, 700, ["Technology", "homebody"], 0, "any"),
    Category("Gaming laptop", 3, 100, 475, 8000, ["Technology"], 0, "any"),
    Category("Gaming desktop", 3, 100, 800, 4000, ["Technology", "homebody"], 0, "any"),
    Category("Gaming headset", 3, 100, 12, 500, ["Technology"], 0, "any"),
    Category("Gaming Mouse", 3, 100, 2, 300, ["Technology"], 0, "any"),
    Category("Gaming keyboard", 3, 100, 20, 425, ["Technology"], 0, "any"),
    Category("Videogame", 3, 100, 2, 70, ["Technology", "homebody"], 0, "any"),
    Category("Gaming mouse pad", 3, 100, 10, 150, ["Technology"], 0, "any"),
    Category("Gamepad", 3, 100, 10, 205, ["Technology"], 0, "any"),
    Category("Gaming chair", 3, 100, 75, 1100, ["Technology", "homebody"], 0, "any"),
    Category("Computer table", 3, 100, 40, 3000, ["Technology", "homebody"], 0, "any"),
    Category("Laptop", 3, 100, 300, 8000, ["Technology"], 0, "any"),
    Category("Desktop PC", 3, 100, 200, 10000, ["Technology"], 0, "any"),
    Category("Tablet", 3, 100, 100, 2000, ["Technology"], 0, "any"),
    Category("Monitor", 3, 100, 75, 6000, ["Technology"], 0, "any"),
    Category("TV", 3, 100, 175, 5000, ["Technology", "homebody"], 0, "any"),
    Category("Powerbank", 3, 100, 38, 200, ["Technology"], 0, "any"),
    Category("Headphones", 3, 100, 10, 5000, ["Technology"], 0, "any"),
    Category("Camera", 3, 100, 22, 1000, ["Technology"], 0, "any"),
    Category("Video camera", 3, 100, 22, 4000, ["Technology"], 0, "any"),
    Category("Portable speaker", 3, 100, 20, 150, ["Technology"], 0, "any"),
    Category("Drawing tablet", 3, 100, 60, 150, ["Technology"], 0, "any"),
    Category("Glue Gun", 3, 100, 15, 50, ["Handicraft"], 0, "any"),
    Category("Oscillating multi-tool", 3, 100, 20, 100, ["Handicraft"], 1, "any"),
    Category("Gas soldering iron", 3, 100, 10, 40, ["Handicraft"], 1, "any"),
    Category("Tool box", 3, 100, 10, 1200, ["Handicraft"], 1, "any"),
    Category("DIY model", 3, 100, 11, 40, ["Handicraft", "homebody"], 0, "any"),
    Category("Needlework organizer", 3, 100, 4, 20, ["Handicraft"], 0, "any"),
    Category(
        "Cross-stitching set", 3, 100, 5, 20, ["Handicraft", "homebody"], 2, "any"
    ),
    Category(
        "Diamond embroidery kit", 3, 100, 2, 30, ["Handicraft", "homebody"], 2, "any"
    ),
    Category("Screwdriver", 3, 100, 2, 25, ["Handicraft"], 1, "any"),
    Category("Electrical screwdriver", 3, 100, 10, 45, ["Handicraft"], 1, "any"),
    Category("Travel bag", 3, 100, 5, 50, ["Tourism"], 0, "any"),
    Category("Folding furniture", 3, 100, 20, 120, ["Tourism"], 0, "any"),
    Category("Portable Grill", 3, 100, 10, 500, ["Tourism"], 0, "any"),
    Category("Sleeping bag", 3, 100, 5, 100, ["Tourism"], 0, "any"),
    Category("Inflatable furniture", 3, 100, 15, 100, ["Tourism"], 0, "any"),
    Category("Tourist burner", 3, 100, 15, 100, ["Tourism"], 0, "any"),
    Category("Road accessories", 3, 100, 2, 200, ["Tourism"], 0, "any"),
    Category("Tourist backpack", 3, 100, 25, 100, ["Tourism"], 0, "any"),
    Category("Thermos", 3, 100, 10, 40, ["Tourism"], 0, "any"),
    Category("Tent", 3, 100, 50, 150, ["Tourism"], 0, "any"),
]

universal_categories = [
    Category("Postcards", 0, 100, 0, 100, ["for_all_param"], 0, "any"),
    Category("Postage stamp", 0, 100, 0, 100, ["for_all_param"], 0, "any"),
    Category("Souvenirs", 0, 100, 0, 100, ["for_all_param"], 0, "any"),
    Category("Chocolate", 0, 100, 0, 100, ["for_all_param"], 0, "any"),
    Category("Cookies", 0, 100, 0, 100, ["for_all_param"], 0, "any"),
    Category("Toys", 0, 100, 0, 100, ["for_all_param"], 0, "any"),
    Category("Towels", 0, 100, 0, 100, ["for_all_param"], 0, "any"),
    Category("Keychains", 0, 100, 0, 100, ["for_all_param"], 0, "any"),
    Category("Cups", 0, 100, 0, 100, ["for_all_param"], 0, "any"),
    Category("Books", 0, 100, 0, 100, ["for_all_param"], 0, "any"),
]


def recommend_product_categories(questionnaire: dict) -> List[str]:
    # reworked the search for products using a list generator instead of if-else,
    # and removed the checking using the range() iterator.
    # due to these changes, a lot of redundant code from else was removed
    # And the search speed also increased because you no longer need to create
    # iterations of numbers for comparison
    recommended_categories: List[str] = [
        category.name
        for category in categories
        if category.min_age <= int(questionnaire["age"]) <= category.max_age
        and category.min_budget <= int(questionnaire["budget"]) <= category.max_budget
        and questionnaire["hobbies"] in category.hobbies
        and (int(questionnaire["male"]) == category.gender or category.gender == 0)
        and (questionnaire["date_type"] == category.event or category.event == "any")
    ][
        :10
    ]
    # But because it searches for all matching products, you need to return
    # the first 10 items through slices.
    # Perhaps later we will change unsatisfactory products through pagination or in
    # another way, and you will not even need to make slices

    if len(recommended_categories) == 10:
        return recommended_categories

    # If there are not enough recommended categories, add random categories from
    # universal_categories
    else:
        while len(recommended_categories) < 10:
            random_category = random.choice(universal_categories)
            recommended_categories.append(random_category.name)
        return recommended_categories


def get_right_thumb_size(url, new_thumb_size):
    last_dot_index = url.rfind(".")
    return (
        url
        if last_dot_index < 1
        else url[: last_dot_index - 3] + new_thumb_size + url[last_dot_index:]
    )


def create_ebay_api():
    try:
        return Finding(
            domain="svcs.ebay.com",
            debug=False,
            appid="BillGen-Tobigift-PRD-c83448d6e-8a50c0ae",
            config_file=None,
            site_id="EBAY_US",
        )
    except ConnectionError as e:
        print(f"ConnectionError while creating API connection: {e}")
        return None


def get_gift_data_ebay(
    api, category: str, max_price: int, recursion_depth: int = 0
) -> dict:
    if recursion_depth == 2:
        print(f"Recursion limit reached for category: {category}")

    try:
        request = {
            "keywords": category,
            "itemFilter": [
                {"name": "MinPrice", "value": max_price * 0.8},
                {"name": "MaxPrice", "value": max_price},
            ],
            "outputSelector": ["SellerInfo", "PictureURLSuperSize"],
            "sortOrder": ["CurrentPriceHighest"],
        }
        response_find = api.execute("findItemsAdvanced", request)

        if response_find.reply.ack == "Success":
            search_result = response_find.reply.searchResult

            if search_result._count == "0":
                print(f"No products found for category: {category}")
                return get_gift_data_ebay(
                    api, category, max_price * 2, recursion_depth + 1
                )

            item_ebay = search_result.item[
                random.randint(0, int(search_result._count) - 1)
            ]
            gift_data = {
                "name": item_ebay.title,
                "price": str(item_ebay.sellingStatus.currentPrice.value),
                "image_url": get_right_thumb_size(item_ebay.galleryURL, "500"),
                "link": item_ebay.viewItemURL,
            }
            return gift_data

    except Exception as e:
        print(f"Error: {e}")


def get_list_product_data(recommended_categories: list, budget: int) -> list[dict]:
    with ThreadPoolExecutor(max_workers=10) as executor:
        api = create_ebay_api()

        if api:
            futures = [
                executor.submit(get_gift_data_ebay, api, gift, budget)
                for gift in recommended_categories
            ]

            # Collect results as they become available
            list_of_gifts_data = [
                future.result()
                for future in as_completed(futures)
                if future.result() is not None
            ]

            # Has to be checked/modified if suits to this func
            for gift in list_of_gifts_data:
                try:
                    RecommendedProduct(**gift)
                except ValidationError as e:
                    print("Validation error:", e)

            return list_of_gifts_data
