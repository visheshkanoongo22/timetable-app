
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
    }
}
