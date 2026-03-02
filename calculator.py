def calculate_totals(app_data):
    plant_totals = {}
    grand_total = 0.0

    for plant in app_data:
        plant_name = plant["tab_name"]
        plant_total = 0.0

        for prod_name, rows in plant["products"].items():
            for row in rows:
                plant_total += row["price"] * row["qty"]

        plant_totals[plant_name] = plant_total
        grand_total += plant_total

    return plant_totals, grand_total
