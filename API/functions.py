from gift_finder.functions import recommend_product_categories, get_list_product_data


def process_gift_picking(questionnaire_answers):
    product_categories = recommend_product_categories(questionnaire_answers)
    list_of_product_data = get_list_product_data(product_categories, int(questionnaire_answers['budget']))

    return list_of_product_data


