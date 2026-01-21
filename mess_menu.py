
from datetime import date

# --- MESS MENU DATA ---
MESS_MENU = {
    # --- PREVIOUS WEEKEND ---
    # Saturday (6/12/2025)
    date(2025, 12, 6): {
        "Breakfast": """
        * Dal Pakwan with Chutney
        * Fruit + Daliya + Khakhra
        """,
        "Lunch": """
        * Gobi Tamatar Capsicum Curry
        * Veg Kofta
        * Dal Fry & Jeera Rice
        * Roti
        * Green Salad, Onion Lemon
        * Plain Curd
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Chole Bhature & Kulcha
        * Dal Fry & Jeera Rice
        * Roti
        * Green Chilli Fry
        * Ring Onion
        * Masala Papad
        * Buttermilk
        """
    },
    # Sunday (7/12/2025)
    date(2025, 12, 7): {
        "Breakfast": """
        * Mix Paratha with Curd + Pickle
        * Fruit + Toast
        """,
        "Lunch": """
        * **South Indian Special:**
        * Masala Dosa
        * Mix Uttapam
        * Idli Sambhar & Vada Sambhar
        * Lemon Rice & Aloo Vada
        * Coconut Chutney
        * Sweet Lassi
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Paneer Pasanda
        * Chana Methi Masala
        * Dal Fry & Jeera Rice
        * Roti
        * Onion + Lemon
        * Frymes
        * **Ice Cream**
        """
    },

    # --- NEW WEEK (08/12 - 13/12) ---
    
    # Monday (08/12/2025)
    date(2025, 12, 8): {
        "Breakfast": """
        * Indori Poha, Lemon Onion, Sev
        * Fruit + Mix Sprout + Veg Sandwich
        """,
        "Lunch": """
        * Gajar Methi Mutter
        * Kadi Pakoda
        * Dal Fry & Plain Rice
        * Roti
        * Green Salad, Onion + Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Cheese Kofta Masala
        * Aloo Chips Masala
        * Dal Fry & Jeera Rice
        * Roti
        * Onion + Lemon
        * Frymes
        """
    },
    # Tuesday (09/12/2025)
    date(2025, 12, 9): {
        "Breakfast": """
        * Sandwich Dhokla with Green Chutney
        * Fruit + Methi ka Thepla with Curd & Pickle
        """,
        "Lunch": """
        * Paneer Handi Masala
        * Loki Chana Dal
        * Dal Fry & Plain Rice
        * Roti
        * Chana Chaat Salad
        * Onion + Lemon
        * Butter Milk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * **Sweet Jalebi**
        * Pav Bhaji & Veg Pulav
        * Boondi Raita
        * Manchurian Noodles
        * Sev Roll with Chutney
        * Roasted Papad
        * Onion + Lemon
        """
    },
    # Wednesday (10/12/2025)
    date(2025, 12, 10): {
        "Breakfast": """
        * Masala Mix Uttapam, Sambhar, Chutney
        * Fruit Poha Sambhar + Toast
        """,
        "Lunch": """
        * Veg Makhanwala
        * Kala Chana Dry
        * Dal Mix Tadka & Jeera Rice
        * Roti
        * Green Salad, Onion Lemon
        * Plain Curd
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * **Cheese Corn Soup**
        * Chinese Samosa
        * Aloo Mutter Tamatar
        * Plain Kadi & Rajwadi Khichdi
        * Lasan ki Chatni
        * Methi Thepla & Roti
        * **Pineapple Halwa**
        """
    },
    # Thursday (11/12/2025)
    date(2025, 12, 11): {
        "Breakfast": """
        * Sev Khamani with Green Chutney
        * Fruit Bread Pakoda + Khakhra + Bhakhri
        """,
        "Lunch": """
        * Palak Corn Capsicum
        * Rajma Masala
        * Dal Tadka & Mutter Rice
        * Roti
        * Green Salad, Onion Lemon
        * Butter Milk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Gobi Mutter Tamatar
        * Moong Masala
        * Hot Pot Rice
        * Palak Paneer Paratha
        * Masala Papad, Onion Lemon
        * Plain Curd
        * Roti
        """
    },
    # Friday (12/12/2025)
    date(2025, 12, 12): {
        "Breakfast": """
        * Dabeli with Chutney
        * Fruit + Masala Maggi + Corn Flakes
        """,
        "Lunch": """
        * Paneer Bhurji Masala
        * Jeera Aloo Masala
        * Dal Fry & Plain Rice
        * Roti
        * Green Salad, Onion Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * **Dal Batti Rajasthani**
        * **Churma Sweet**
        * Besan ka Gatta Masala
        * Lasan ki Chatni, Ghee & Gud
        * Plain Rice
        * Onion Lemon, Butter Milk
        * Roti
        """
    },
    # Saturday (13/12/2025)
    date(2025, 12, 13): {
        "Breakfast": """
        * Puri Bhaji
        * Fruit Daliya + Veg Sandwich
        """,
        "Lunch": """
        * Veg Jalfrezi Masala Dry
        * Paneer Kofta
        * Dal Mix Tadka & Jeera Rice
        * Roti
        * Green Salad, Onion Lemon
        * Butter Milk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Mix Pakoda
        * **Sarso ka Saag**
        * Sev Tamatar
        * Plain Kadi & Rajwadi Khichdi
        * Lasan ki Chatni
        * **Makai ki Roti**
        * Ghee + Gud
        * Onion + Lemon, Butter Milk
        """
    },
    
    date(2025, 12, 14): {
        "Breakfast": """
        * Mix Paratha with Curd & Pickle
        * Fruit
        * Toast
        """,
        "Lunch": """
        * Masala Dosa
        * Mix Uttapam
        * Idli Sambhar
        * Vada Sambhar
        * Lemon Rice
        * Aloo Vada
        * Coconut Chutney
        * Lassi
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Hara Bhara Kabab
        * Chinese Samosa
        * Paneer Pesawari
        * Mushroom Mutter
        * Dal Makhani
        * Jeera Rice
        * Palak Paratha
        * Puri
        * Frymes
        * Gajar Halwa
        * Kesar Badam Milk
        """
    },
    date(2025, 12, 15): {
        "Breakfast": """
        * Badaka Poha, Lemon Onion, Sev
        * Vegetable Sandwich
        * Jemny Sprout
        * Tea, Milk, Coffee
        * Fruit
        """,
        "Lunch": """
        * Mix Veg Masala Dry
        * Kadi Pakoda
        * Dal Fry
        * Plain Rice
        * Roti
        * Green Salad
        * Onion, Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea, Milk, Coffee
        """,
        "Dinner": """
        * Bengan ka Bharta
        * Lasaniya Aloo
        * Mix Dal Tadka
        * Mutter Rice
        * Bajre ki Roti
        * Lasoon ki Chutney
        * Frymes
        * Onion, Lemon
        * Butter Milk
        """
    },
    # Tuesday (16/12/2025)
    date(2025, 12, 16): {
        "Breakfast": """
        * Sandwich Dhokla with Green Chutney
        * Fruit
        * Methi Ka Thepla with Curd & Pickle
        """,
        "Lunch": """
        * Palak Paneer Masala
        * Rajma Masala
        * Dal Fry
        * Plain Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Butter Milk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Tomato Soup
        * **Sweet: Gulab Jamun**
        * Aloo Paneer Paratha
        * Plain Curd
        * Manchurian Fried Rice
        * Papdi Chat
        * Pani Puri
        * Masala Papad
        * Chana Jor Garam
        * Mix Pickle
        """
    },

    # Wednesday (17/12/2025)
    date(2025, 12, 17): {
        "Breakfast": """
        * Mix Uttapam (Sambhar, Chutney)
        * Fruit + Idli Sambhar Chutney + Toast
        """,
        "Lunch": """
        * Gajar Mutter Dry
        * Kadi Pakoda
        * Dal Tadka
        * Plain Rice
        * Roti
        * Chana Chat Salad
        * Onion + Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Aloo Capsicum
        * Moong Masala
        * Dal Fry
        * Plain Rice
        * Roti
        * Onion + Lemon
        * Frymes
        """
    },

    # Thursday (18/12/2025)
    date(2025, 12, 18): {
        "Breakfast": """
        * Vada Pav with Chutney
        * Fruit + Masala Maggi + Cornflakes
        """,
        "Lunch": """
        * Veg Tawa Sabji
        * Paneer Handi Masala
        * Dal Fry
        * Jeera Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Plain Curd
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Broccoli Soup
        * Live Dhokla
        * Aloo Rasevala
        * Plain Kadi
        * Rajwadi Khichdi
        * Methi Ka Thepla
        * Roti
        * Lasun Ki Chatni
        * Frymes
        * **Sweet: Suji Ka Halwa**
        """
    },

    # Friday (19/12/2025)
    date(2025, 12, 19): {
        "Breakfast": """
        * Dal Pakwan with Chutney
        * Fruit
        * Aloo Mutter Sandwich + Toast
        """,
        "Lunch": """
        * Veg Jaipuri
        * Kala Chana
        * Dal Mix Tadka
        * Jeera Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Butter Milk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * **Sweet: Jalebi**
        * Pav Bhaji
        * Veg Pulao
        * Boondi Raita
        * Manchurian Noodles
        * Sev Roll with Chutney
        * Roasted Papad
        * Onion + Lemon
        """
    },

    # Saturday (20/12/2025)
    date(2025, 12, 20): {
        "Breakfast": """
        * Suji Ka Upma with Coconut Chutney
        * Fruit + Moong
        * Oat Chilla with Chutney
        """,
        "Lunch": """
        * Gobi Mutter Capsicum
        * Malai Kofta
        * Dal Fry
        * Plain Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Hot 'n' Sour Soup
        * Mix Pakoda
        * Chole Bhature
        * Kulcha
        * Dal Mix Tadka
        * Jeera Rice
        * Roti
        * Green Chilli Fry
        * Onion + Lemon
        * Masala Papad
        """
    },
  date(2025, 12, 21): {
        "Breakfast": """
        * Gobi Paneer Aloo Paratha
        * Plain Curd
        * Pickle
        * Cornflakes
        * Bread Butter
        * Bread Jam
        * Tea, Milk, Coffee
        * Fruit
        """,
        "Lunch": """
        * Masala Dosa
        * Mix Uttapam
        * Medu Vada
        * Sambhar
        * Aloo Vada
        * Lemon Rice
        * Idli
        * Coconut Chutney
        * Sweet Lassi
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Paneer Do Pyaza
        * Soya Mutter Dry
        * Dal Fry
        * Jeera Rice
        * Roti
        * Onion + Lemon
        * Frymes
        * **Ice Cream**
        """
    },
    # Monday (22/12/2025) - Jay Sita Ram
    date(2025, 12, 22): {
        "Breakfast": """
        * Indori Poha (Lemon, Onion, Sev)
        * Aloo Mutter Sandwich
        * Cornflakes
        * Bread Butter
        * Bread Jam
        * Tea / Milk / Coffee
        * Fruit
        """,
        "Lunch": """
        * Veg Makhanwala
        * Rajma Masala
        * Dal Fry
        * Jeera Rice
        * Roti
        * Green Salad
        * Lemon & Onion
        * Buttermilk
        """,
        "Hi-Tea": """
        * Tea / Milk / Coffee
        """,
        "Dinner": """
        * Mix Pakoda
        * Baingan ka Bharta
        * Aloo Capsicum Chips Dry
        * Rajwadi Khichdi
        * Plain Kadhi
        * Lasoon ki Chutney
        * Bajre ki Roti
        * Puri
        * Cabbage Sambhara
        """
    },

    # Tuesday (23/12/2025)
    date(2025, 12, 23): {
        "Breakfast": """
        * Methi ka Thepla with Curd & Pickle
        * Fruit
        * Sandwich / Chilla with Green Chutney
        * Regular Menu Items
        """,
        "Lunch": """
        * Palak Paneer Masala
        * Kala Chana Dry
        * Dal Fry
        * Jeera Rice
        * Roti
        * Green Salad
        * Onion & Lemon
        * Plain Curd
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * **Sweet: Gajar ka Halwa**
        * Veg Jaipuri
        * Red Pasta
        * Dal Fry
        * Mutter Rice
        * Palak Paneer Paratha
        * Roti
        * Roasted Papad
        * Sweet Corn Soup
        """
    },

    # Wednesday (24/12/2025)
    date(2025, 12, 24): {
        "Breakfast": """
        * (Menu not provided in images)
        """,
        "Lunch": """
        * (Menu not provided in images)
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * (Menu not provided in images)
        """
    },

    # Thursday (25/12/2025) - CHRISTMAS
    date(2025, 12, 25): {
        "Breakfast": """
        * Suji ka Upma with Coconut Chutney
        * Fruit
        * Dabeli with Chutney & Toast
        * Regular Menu Items
        """,
        "Lunch": """
        * Shahi Paneer Masala
        * Chole Masala
        * Dal Fry
        * Plain Rice
        * Roti
        * Green Salad
        * Onion & Lemon
        * Buttermilk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Tomato Soup
        * Aloo Paneer Paratha
        * Plain Curd & Pickle
        * Manchurian Fried Rice
        * Papdi Chaat
        * Pani Puri
        * Chana Jor Garam
        * Masala Papad
        * **Sweet**
        """
    },

    # Friday (26/12/2025)
    date(2025, 12, 24): {
        "Breakfast": """
        * Masala Idli with Chutney
        * Fruit
        * Mix Uttapam
        * Sambhar
        * Regular Menu Items
        """,
        "Lunch": """
        * Gobhi Mutter Capsicum Dry
        * Paneer Kofta
        * Dal Fry
        * Plain Rice
        * Roti
        * Green Salad
        * Onion & Lemon
        * Buttermilk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Aloo Bhindi Masala
        * Moong Masala
        * Dal Fry
        * Plain Rice
        * Roti
        * Onion & Lemon
        * Fryums
        """
    },
  date(2025, 12, 26): {
        "Breakfast": """
        * Dal Pakwan with Chutney
        * Sev Khamani
        * Green Chutney
        * Cornflakes
        * Bread Butter
        * Bread Jam
        * Tea, Milk, Coffee
        * Fruit
        """,
        "Lunch": """
        * Veg Jal Fraizi Dry
        * Loki Kofta
        * Dal Fry
        * Jeera Rice
        * Roti
        * Green Salad
        * Lemon, Onion
        * Boondi Raita
        """,
        "Hi-Tea": """
        * Tea, Milk, Coffee
        """,
        "Dinner": """
        * **Sweet: Malpuva**
        * Chinese Samosa
        * Subzi Ka Saag
        * Sev Tamatar
        * Veg Biryani
        * Plain Curd
        * Lasoon Ki Chutney
        * Makai Ki Roti
        * Ghee Chana
        * Masala Papad
        """
    },
   date(2025, 12, 27): {
        "Breakfast": """
        * Poori Bhaji
        * Khakhra
        * Fruit
        * Veg Sandwich
        """,
        "Lunch": """
        * Gajar Methi Mutter
        * Kadhi Pakoda
        * Dal Fry
        * Plain Rice
        * Roti
        * Chana Chaat Salad
        * Onion + Lemon
        * Jal Jeera Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Cheese Corn Soup
        * Sev Roll with Chutney
        * Chole Bhature
        * Kulcha
        * Dal Makhani
        * Jeera Rice
        * Roti
        * Green Chilli Fry
        * Onion + Lemon
        * Roasted Papad
        """
    },

    # Monday (29/12/2025)
    date(2025, 12, 29): {
        "Breakfast": """
        * Bataka Poha, Lemon, Onion, Sev
        * Fruit + Aloo Matar Sandwich
        * Regular Menu
        """,
        "Lunch": """
        * Veg Kolhapuri
        * Rajma Masala
        * Dal Mix Tadka
        * Plain Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Buttermilk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Tomato Soup
        * Live Dhokla
        * Aloo Matar Rasevala
        * Plain Kadhi
        * Rajwadi Khichdi
        * Methi Thepla
        * Roti
        * Lasun Ki Chutney
        * Fryums
        * **Pineapple Halwa**
        """
    },

    # Tuesday (30/12/2025)
    date(2025, 12, 30): {
        "Breakfast": """
        * Suji Ka Upma with Coconut Chutney
        * Fruit Daliya + Veg Sandwich
        """,
        "Lunch": """
        * Palak Paneer Masala
        * Moong Masala Dry
        * Dal Mix Tadka
        * Jeera Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * **Sweet: Jalebi**
        * Pav Bhaji
        * Veg Pulao
        * Boondi Raita
        * Manchurian Noodles
        * Sev Roll with Chutney
        * Roasted Papad
        * Onion + Lemon
        """
    },

    # Wednesday (31/12/2025) - NEW YEAR'S EVE
    date(2025, 12, 31): {
        "Breakfast": """
        * Methi Ka Thepla with Curd & Pickle
        * Fruit + Sandwich Dhokla with Green Chutney
        * Regular Menu
        """,
        "Lunch": """
        * Aloo Capsicum Dry
        * Methi Matar Malai
        * Dal Fry
        * Plain Rice
        * Roti
        * Chana Chaat Salad
        * Onion + Lemon
        * Buttermilk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Hot n Sour Soup
        * Mix Pakoda
        * Paneer Bhurji
        * Dal Makhani
        * Jeera Rice
        * Red Pasta
        * Palak Tawa Paratha
        * Roasted Fryums
        * Roti
        * Onion + Lemon
        """
    },

    # Thursday (01/01/2026) - NEW YEAR'S DAY
    date(2026, 1, 1): {
        "Breakfast": """
        * Idli Sambar Chutney
        * Mix Uttapam + Fruit + Toast
        """,
        "Lunch": """
        * Veg Makhanwala
        * Kala Chana Dry
        * Dal Fry
        * Matar Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * **Sweet: Boondi**
        * Baingan Ka Bharta
        * Aloo Capsicum Chips Dry
        * Dal Fry
        * Matar Rice Plain
        * Bajra Ki Roti + Puri Methi
        * Onion + Lemon
        * Masala Papad
        * Plain Curd
        """
    },

    # Friday (02/01/2026)
    date(2026, 1, 2): {
        "Breakfast": """
        * Puri Bhaji + Toast
        * Fruit + Veg Sandwich
        """,
        "Lunch": """
        * Lauki Chana Masala
        * Kadhi Pakoda
        * Dal Mix Tadka
        * Plain Rice
        * Roti
        * Mix Sprout Salad
        * Onion + Lemon
        * Buttermilk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Gobi Tomato Matar Dry
        * Moong Masala
        * Dal Fry
        * Plain Rice
        * Roti
        * Onion + Lemon
        * Fryums
        * **Sweet: Gulab Jamun**
        """
    },

    # Saturday (03/01/2026)
    date(2026, 1, 3): {
        "Breakfast": """
        * Masala Maggi + Daliya
        * Fruit + Nylon Khaman with Kadhi
        * Regular Menu
        """,
        "Lunch": """
        * Veg Jalfrezi
        * Paneer Kofta
        * Dal Fry
        * Plain Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Plain Curd
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Veg Manchow Soup
        * Corn Tikki
        * Chole Bhature
        * Kulcha
        * Dal Mix Tadka
        * Jeera Rice
        * Green Chilli Fry
        * Ring Onion + Lemon
        * Roasted Papad
        * Roti
        """
    },

    # Sunday (04/01/2026)
    date(2026, 1, 4): {
        "Breakfast": """
        * Mix Paratha with Curd & Pickle
        * Fruit + Khakhra
        * Regular Menu
        """,
        "Lunch": """
        * Masala Dosa
        * Mix Uttapam
        * Masala Idli
        * Vada Sambar
        * Aloo Vada
        * Tomato Rice
        * Coconut Chutney
        * Sweet Lassi
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Paneer Pasanda
        * Soya Matar Dry
        * Dal Makhani
        * Plain Rice
        * Roti + Puri
        * Fryums
        * Onion + Lemon
        * **Ice Cream**
        """
    },

    # Monday (05/01/2026)
    date(2026, 1, 5): {
        "Breakfast": """
        * Indori Poha, Lemon, Onion, Sev
        * Fruit + Toast + Daliya + Veg Sandwich
        """,
        "Lunch": """
        * Mix Veg Dry
        * Rajma Masala
        * Dal Fry
        * Plain Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Buttermilk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Veg Manchurian Dry
        * Kaju Curry
        * Dal Fry
        * Jeera Rice
        * Roti
        * Onion + Lemon
        * Roasted Papad
        """
    },

    # Tuesday (06/01/2026)
    date(2026, 1, 6): {
        "Breakfast": """
        * Bread Pakoda with Green Chutney & Sauce
        * Fruit + Suji Ka Upma with Coconut Chutney + Toast
        """,
        "Lunch": """
        * Palak Paneer Masala
        * Chole Masala
        * Dal Fry
        * Plain Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Rasna
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * **Sweet: Rice Kheer**
        * Live Dhokla
        * Aloo Matar Rasevala
        * Plain Kadhi
        * Plain Khichdi
        * Tawa Paratha
        * Roti
        * Lasun Ki Chutney
        * Fryums
        * Onion + Lemon
        """
    },

    # Wednesday (07/01/2026)
    date(2026, 1, 7): {
        "Breakfast": """
        * Idli Sambar + Vada Sambar, Coconut Chutney
        * Fruit + Khakhra
        """,
        "Lunch": """
        * Veg Makhanwala
        * Chole Masala
        * Dal Mix Tadka
        * Plain Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Buttermilk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Hot n Sour Soup
        * Mix Pakoda
        * Paneer Bhurji
        * Dal Makhani
        * Jeera Rice
        * Red Pasta
        * Palak Paratha
        * Roti
        * Onion + Lemon
        """
    },

    # Thursday (08/01/2026)
    date(2026, 1, 8): {
        "Breakfast": """
        * Dal Pakwan with Chutney
        * Fruit + Toast
        * Veg Sandwich
        """,
        "Lunch": """
        * Gajar Matar Dry
        * Kadhi Pakoda
        * Dal Fry
        * Plain Rice
        * Roti
        * Chana Chaat Salad
        * Onion + Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * **Sweet: Pineapple Halwa**
        * Chinese Samosa
        * Sarson Ka Saag
        * Sev Tomato Masala
        * Dal Fry
        * Matar Rice
        * Makai Ki Roti
        * Lasun Ki Chutney
        * Ghee + Gud (Jaggery)
        * Masala Papad
        * Roti
        """
    },

    # Friday (09/01/2026)
    date(2026, 1, 9): {
        "Breakfast": """
        * Methi Ka Thepla with Curd & Pickle
        * Fruit + Sandwich Dhokla with Green Chutney
        """,
        "Lunch": """
        * Paneer Lababdar
        * Cabbage Matar Dry
        * Dal Fry
        * Jeera Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Jal Jeera
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * **Sweet: Rasgulla**
        * Tomato Soup
        * Aloo Paneer Paratha
        * Manchurian Fried Rice
        * Papdi Chaat
        * Pani Puri
        * Chana Jor Garam
        * Plain Curd & Pickle
        * Fryums
        """
    },

    # Saturday (10/01/2026)
    date(2026, 1, 10): {
        "Breakfast": """
        * Moong Oat Chilla with Chutney + Cornflakes
        * Fruit + Sev Khamani with Chutney
        """,
        "Lunch": """
        * Veg Tawa Sabji
        * Mix Kathol
        * Dal Fry
        * Plain Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Buttermilk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Veg Manchow Soup
        * Sev Roll with Chutney
        * Pav Bhaji
        * Veg Biryani
        * Boondi Raita
        * Roasted Papad
        * Onion + Lemon
        * Red Veg Hakka Noodles
        """
    },

    # Sunday (11/01/2026)
    date(2026, 1, 11): {
        "Breakfast": """
        * Mix Paratha with Curd & Pickle
        * Fruit + Khakhra
        """,
        "Lunch": """
        * Masala Dosa
        * Idli Masala
        * Mix Uttapam
        * Vada Sambar
        * Aloo Vada
        * Coconut Chutney
        * Tomato Rice
        * Sweet Lassi
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Paneer Butter Masala
        * Jeera Aloo Dry
        * Dal Makhani
        * Jeera Rice
        * Roti + Puri
        * Green Salad
        * Onion + Lemon
        * Rasna Water
        """
    },
    # Monday (12/01/2026)
    date(2026, 1, 12): {
        "Breakfast": """
        * Idli Poha
        * Lemon Onion Sev
        * Fruit
        * Mix Sprout
        * Veg Sandwich
        """,
        "Lunch": """
        * Veg Kolhapuri Masala
        * Rajma Masala
        * Dal Mix Tadka
        * Mutter Pulao
        * Roti
        * Green Salad
        * Onion + Lemon
        * Buttermilk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Dal Baati
        * **Churma (Sweet)**
        * Besan Gatta Masala
        * Tomato Rice
        * Ghee + Gud
        * Lasun Chutney
        * Roti
        * Roasted Papad
        * Buttermilk
        * Onion + Lemon
        """
    },

    # Tuesday (13/01/2026)
    date(2026, 1, 13): {
        "Breakfast": """
        * Bread Pakoda
        * Green Chutney
        * Fruit
        * Suji Ka Upma
        * Coconut Chutney
        """,
        "Lunch": """
        * Gajar Mutter Capsicum
        * Kadhi Pakoda
        * Dal Mix Tadka
        * Plain Rice
        * Roti
        * Chana Chaat Salad
        * Onion + Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * **Sweet: Rice Kheer**
        * Baingan Ka Bharta
        * Aloo Chips Masala Dry
        * Dal Fry
        * Plain Rice
        * Bajra Ki Roti
        * Methi Puri
        * Onion + Lemon
        * Masala Papad
        """
    },

    # Wednesday (14/01/2026) - MAKAR SANKRANTI
    date(2026, 1, 14): {
        "Breakfast": """
        * Idli Sambar
        * Chutney
        * Fruit
        * Mix Uttapam
        * Toast
        """,
        "Lunch": """
        * Undhiyu Gujarati
        * Paneer Kadai Masala
        * Dal Mix Tadka
        * Mutter Rice
        * Methi Puri
        * Roti
        * Green Salad
        * Onion + Lemon
        * **Sweet: Jalebi**
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Tomato Soup
        * Aloo Paneer Paratha
        * Plain Curd
        * Pickle
        * Manchurian Fried Rice
        * Papdi Chaat
        * Pani Puri
        * Chana Jor Garam
        * Masala Papad
        """
    },

    # Thursday (15/01/2026)
    date(2026, 1, 15): {
        "Breakfast": """
        * Masala Maggi
        * Daliya
        * Fruit
        * Nylon Khaman
        * Kadhi
        """,
        "Lunch": """
        * Veg Tawa Sabji
        * Mix Kathol
        * Dal Fry
        * Plain Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Boondi Raita
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Methi Mutter Malai
        * Aloo Chips Masala Dry
        * Dal Fry
        * Jeera Rice
        * Roti
        * Onion + Lemon
        * Fryums
        """
    },

    # Friday (16/01/2026)
    date(2026, 1, 16): {
        "Breakfast": """
        * Methi Ka Thepla
        * Curd
        * Pickle
        * Fruit
        * Aloo Mutter Sandwich
        * Green Chutney
        """,
        "Lunch": """
        * Paneer Do Pyaza
        * Cabbage Mutter Capsicum Dry
        * Dal Mix Tadka
        * Plain Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * **Sweet: Gajar Ka Halwa**
        * Cheese Corn Soup
        * Chole Bhature
        * Veg Pulao
        * Tomato Raita
        * Onion Rings
        * Green Chilli Fry
        * Kulcha
        * Roasted Papad
        """
    },

    # Saturday (17/01/2026)
    date(2026, 1, 17): {
        "Breakfast": """
        * Dal Pakwan
        * Chutney
        * Daliya
        * Fruit
        * Veg Sandwich
        """,
        "Lunch": """
        * Paneer Kofta
        * Gobi Mutter Dry
        * Dal Fry Tadka
        * Plain Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Buttermilk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Tomato Soup
        * Live Dhokla
        * Aloo Tamatar Rasewala
        * Plain Kadhi
        * Rajwadi Khichdi
        * Lasun Ki Chutney
        * Methi Thepla
        * Roti
        * Fryums
        * **Sweet: Mal Pua**
        """
    },

    # Sunday (18/01/2026)
    date(2026, 1, 18): {
        "Breakfast": """
        * Mix Paratha
        * Curd
        * Pickle
        * Fruit
        * Khakhra
        * Corn Flakes
        """,
        "Lunch": """
        * Masala Dosa
        * Mix Uttapam
        * Masala Idli
        * Lemon Rice
        * Aloo Vada
        * Vada Sambar
        * Coconut Chutney
        * Sweet Lassi
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Cheese Butter Masala
        * Veg Manchurian Dry
        * Dal Mix Tadka
        * Jeera Rice
        * Roti
        * Puri
        * Onion + Lemon
        * Fryums
        """
    },
{
    Date(2026, 1, 19): {
        "Breakfast": """
        * Poha, Lemon, Onion, Sev
        * Fruit
        * Mix Sprout
        * Veg Sandwich
        """,
        "Lunch": """
        * Mix Veg Masala (Dry)
        * Kadi Pakoda
        * Dal Mix Tadka & Plain Rice
        * Roti
        * Green Salad, Onion + Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Chinese Samosa
        * Sarso Ka Saag & Makai Ki Roti
        * Sev Tamato Masala
        * Mix Dal Tadka & Jeera Rice
        * Lasun Ki Chatni
        * Boondi Raita
        * Ghee & Gud
        * Masala Papad
        """
    },
    Date(2026, 1, 20): {
        "Breakfast": """
        * Suji Ka Upma With Coconut Chatni
        * Fruit
        * Bread Pakoda With Green Chatni Sauce
        """,
        "Lunch": """
        * Palak Paneer Masala
        * Choli Masala
        * Dal Fry & Plain Rice
        * Roti
        * Green Salad, Onion + Lemon
        * Plain Curd
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Sweet Boondi
        * Hot & Sour Soup
        * Sev Roll With Chatni
        * Pav Bhaji
        * Veg Pulao & Veg Hakka Noodles
        * Boondi Raita
        * Masala Papad
        * Onion + Lemon
        """
    },
    Date(2026, 1, 21): {
        "Breakfast": """
        * Idli Sambhar Chatni + Toast
        * Fruit + Mix Uttapam Sambhar Chatni
        """,
        "Lunch": """
        * Tomato Corn Bharta
        * Rajma Masala
        * Aloo Capsicum
        * Dal Fry & Plain Rice
        * Roti
        * Chana Chat Salad
        * Onion + Lemon
        * Butter Milk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Veg Crispy (Dry)
        * Sev Dungari Masala
        * Hot Pot Rice
        * Palak Tawa Paratha
        * Roti
        * Onion + Lemon
        * Frymes
        * Pineapple Halwa
        """
    },
    Date(2026, 1, 22): {
        "Breakfast": """
        * Methi Ka Thepla With Curd & Pickle
        * Fruit
        * Sev Khamani With Chatni
        * Cornflakes
        """,
        "Lunch": """
        * Veg Makhanwala
        * Rajma Masala
        * Dal Mix Tadka & Jeera Rice
        * Roti
        * Green Salad, Onion + Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Dum Aloo Masala
        * Gobi Manchurian (Dry)
        * Dal Makhani & Mutter Rice
        * Roti + Puri
        * Onion + Lemon
        * Roasted Papad Masala
        """
    },
    Date(2026, 1, 23): {
        "Breakfast": """
        * Masala Maggi + Fruit
        * Sandwich / Dhokla With Green Chatni
        """,
        "Lunch": """
        * Paneer Kadai Masala
        * Loki Chana Masala
        * Dal Mix Tadka & Plain Rice
        * Roti
        * Green Salad, Onion + Lemon
        * Plain Curd
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Rice Kheer
        * Baingan Ka Bharta
        * Aloo Capsicum Chips (Dry)
        * Dal Fry & Jeera Rice
        * Bajre Roti + Puri
        * Onion + Lemon
        * Fry Papad
        """
    },
    Date(2026, 1, 24): {
        "Breakfast": """
        * Paratha / Dal Pakwan With Chatni
        * Fruit
        * Veg Sandwich
        """,
        "Lunch": """
        * Veg Jaipuri Masala
        * Moong Masala
        * Dal Fry & Jeera Rice
        * Roti
        * Green Salad, Onion + Lemon
        * Jal Jeera
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Cheese Corn Soup
        * Naylon Samosa
        * Chole Bhature & Kulcha
        * Veg Pulao
        * Tomato Raita
        * Ring Onion & Green Chilli Fry
        * Masala Papad
        """
    },
    Date(2026, 1, 25): {
        "Breakfast": """
        * Mix Paratha With Curd & Pickle
        * Fruit + Khakra
        """,
        "Lunch": """
        * Masala Dosa
        * Mix Uttapam
        * Masala Idli
        * Vada Sambhar & Aloo Vada
        * Lemon Rice
        * Coconut Chatni
        * Lassi With Fruit
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Paneer Bhurji Masala
        * Soya Mutter Masala
        * Dal Mix Tadka & Jeera Rice
        * Roti
        * Onion + Lemon
        * Ice Cream
        """
    }
}

