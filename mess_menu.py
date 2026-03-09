
from datetime import date

# --- MESS MENU DATA ---
MESS_MENU = {
    # --- PREVIOUS WEEKEND ---
   
    date(2026, 2, 20): {
        "Breakfast": """
        * Suji Upma with Chutney
        * Bhakhri
        * Fruit
        * Veg Sandwich
        * Tea & Coffee
        """,
        "Lunch": """
        * Veg Kolhapuri
        * Moong Masala
        * Dal Fry
        * Jeera Rice
        * Roti
        * Green Salad
        * Onion & Lemon
        * Jeera Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Tomato Soup
        * Chinese Samosa
        * Pav Bhaji
        * Veg Pulao
        * Boondi Raita
        * Manchurian Noodles
        * Onion + Lemon
        * Masala Papad
        """
    },
    date(2026, 2, 21): {
        "Breakfast": """
        * Dal Pakwan with Chutney
        * Fruit
        * Sandwich Dhokla with Green Chutney
        * Tea & Coffee
        """,
        "Lunch": """
        * Paneer Kadai Masala
        * Loki Chana Masala
        * Dal Mix Tadka
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
        * Live Dhokla with Chutney
        * Aloo Rasewala
        * Baingan Bharta
        * Puri & Roti
        * Papad Chaat
        * Dal Fry
        * Plain Rice
        * Hot Pot Rice
        * Suji Halwa
        """
    },
    date(2026, 2, 22): {
        "Breakfast": """
        * Mix Paratha with Curd & Pickle
        * Fruit
        * Veg Sandwich
        * Tea & Coffee
        """,
        "Lunch": """
        * Veg Masala
        * Idli Sambhar
        * Veg Uttapam
        * Dal Fry
        * Jeera Rice
        * Roti
        * Coconut Chutney
        * Sweet Lassi
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Cheese Corn Soup
        * Mix Pakoda
        * Paneer Bhurji
        * Dal Makhani
        * Jeera Rice
        * Potato Paneer Paratha
        * Roti
        * Onion & Lemon
        * Ice Cream
        """
    },

    date(2026, 2, 24): {
        "Breakfast": """
        * Methi Thepla with Curd & Pickle
        * Fruit & Bread Pakoda with Chutney
        """,
        "Lunch": """
        * Palak Paneer Masala
        * Chole Masala
        * Dal Fry
        * Jeera Rice
        * Roti
        * Green Salad
        * Onion & Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Veg Manchow Soup
        * Nadiyad Samosa
        * Chole Bhature
        * Dal Mix Tadka
        * Plain Rice
        * Roti
        * Kulcha
        * Buttermilk
        * Fried Mirch
        * Sweet Shrikhand
        """
    },
    date(2026, 2, 25): {
        "Breakfast": """
        * Masala Idli with Chutney
        * Fruit & Mix Uttapam, Sambar, Chutney
        """,
        "Lunch": """
        * Veg Kolhapuri Masala
        * Jeera Aloo Masala Dry
        * Dal Fry
        * Jeera Rice
        * Roti
        * Green Salad
        * Onion & Lemon
        * Jaljeera Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Tomato Soup
        * Lilva Kachori with Chutney
        * Aloo Paneer Paratha
        * Plain Curd & Pickle
        * Pani Puri
        * Papdi Chaat
        * Chana Jor Garam
        * Hot Pot Rice
        * Sweet Dahi Vada
        """
    },
    date(2026, 2, 26): {
        "Breakfast": """
        * Masala Maggi & Cornflakes
        * Fruit & Sandwich Dhokla with Green Chutney
        """,
        "Lunch": """
        * Paneer Butter Masala
        * Cabbage Mutter Dry
        * Dal Fry
        * Plain Rice
        * Roti
        * Green Salad
        * Onion & Lemon
        * Plain Curd
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Sweet Gulab Jamun
        * Aloo Tamatar Rasawala
        * Plain Kadhi
        * Rajwadi Khichdi
        * Methi Puri
        * Roti
        * Onion & Lemon
        * Roasted Papad
        """
    },
    date(2026, 2, 27): {
        "Breakfast": """
        * Suji Ka Upma with Coconut Chutney
        * Fruit & Veg Sandwich & Bhakri
        """,
        "Lunch": """
        * Veg Jaipuri Masala
        * Rajma Masala
        * Dal Mix Tadka
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
        * Cheese Butter Masala
        * Gobi Manchurian
        * Dal Fry
        * Jeera Rice
        * Roti
        * Onion & Lemon
        * Fryums
        """
    },
    date(2026, 2, 28): {
        "Breakfast": """
        * Vada Pav with Chutney & Cornflakes
        * Fruit & Sev Khamani with Chutney
        """,
        "Lunch": """
        * Gajar Mutter Capsicum
        * Kadhi Pakoda
        * Dal Fry
        * Plain Rice
        * Roti
        * Mix Sprout Salad
        * Onion & Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Methi
        * Palak Corn Capsicum
        * Chole Masala
        * Dal Fry
        * Plain Rice
        * Roti & Puri
        * Onion & Lemon
        * Fryums
        """
    },

    date(2026, 3, 2): {
        "Breakfast": """
        * Indori Sev Poha
        * Veg sandwich
        * Fruit
        * Bread Butter & Jam
        * Tea & Coffee
        """,
        "Lunch": """
        * Veg Kohlapuri
        * Mix Kathol
        * Butter milk
        * Dal
        * Mutter Rice
        * Roti
        * Salad
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Paneer Tikka Masala
        * Moong Masala
        * Frymes
        * Dal tadka
        * Rice
        * Roti
        """
    },
    date(2026, 3, 3): {
        "Breakfast": """
        * Methi Thepla
        * Sev Khamni
        * Bread Butter & Jam
        * Tea & Coffee
        * Cornflakes
        """,
        "Lunch": """
        * Palak paneer Masala
        * Choli masala
        * Dahi
        * Dal
        * Rice
        * Roti
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Nargis kofta
        * Veg Crispy
        * Roti
        * Butter Milk
        * Frymes
        * Dal Fry
        * Plain Rice
        """
    },
    date(2026, 3, 4): {
        "Breakfast": """
        * Mix Uttapam
        * Masala Idli - sambhar
        * Bread Butter & Jam
        * Tea & Coffee
        """,
        "Lunch": """
        * Paneer Patiala
        * Loki Chana masala
        * Lemon water
        * Plain Rice
        * Dal Fry
        * Roti
        * Salad
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Chole Bhature/Kulcha
        * Cheese Corn Soup
        * Chineese Samosa
        * Dal
        * Plain Veg Pulav
        * Boondi Raita
        * Roti
        """
    },
    date(2026, 3, 5): {
        "Breakfast": """
        * Bread Pakoda
        * Nylon Khaman
        * Bread Butter & Jam
        * Tea & Coffee
        * Fruit
        """,
        "Lunch": """
        * Gajar Mutter
        * Rajma
        * Buttermilk
        * Jeera Rice
        * Dal Tadka
        * Roti
        * Salad
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Pani Puri
        * Aloo paneer parotha
        * Papdi chaat
        * Chana jor garam
        * Dahi vada
        * Dum Biryani
        * Curd
        * Pickle
        """
    },
    date(2026, 3, 6): {
        "Breakfast": """
        * Veg Sandwich
        * Dal Pakwan
        * Bread Butter & Jam
        * Tea & Coffee
        * Fruit
        """,
        "Lunch": """
        * Paneer Lababdar
        * Kala Chana
        * Dal Tadka
        * Rice
        * Limbu Pani
        * Roti
        * Salad
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Sweet-Srikhand
        * Cheese butter Masala
        * Aloo Chips
        * Rice
        * Puri
        * Butter milk
        * Rosted Papad
        """
    },
    date(2026, 3, 7): {
        "Breakfast": """
        * Dabeli
        * Suji Upma
        * Boil Chana Rajma
        * Bread Butter & Jam
        * Tea & Coffee
        * Fruit
        """,
        "Lunch": """
        * Mix Veg masala
        * Malai Kofta
        * Dal Fry
        * Rice
        * Roti
        * Salad
        * Dahi
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Kaju Curry
        * Veg Manchurian
        * Dal Tadka Rice
        * Gulab Jamun
        * Fryms
        """
    },
    date(2026, 3, 8): {
        "Breakfast": """
        * Aloo Paratha / Paneer Paratha
        * Khakhra
        * Bread Butter & Jam
        * Tea & Coffee
        * Fruit
        """,
        "Lunch": """
        * Mix Uttapam
        * Masala Dosa
        * Idli, Medu Vada
        * Sambhar
        * Coconut Chutney
        * Schezwan Rice
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Tomato Soup
        * Pav Bhaji
        * Hara Bhara Kabab
        * Veg Biryani
        * Boondi Raita
        * Masala Papad
        * Ice Cream
        """,
    },
    date(2026, 3, 9): {
        "Breakfast": """
        * Indori Poha (With Lemon, Onion, Sev)
        * Fruit
        * Veg Sandwich
        """,
        "Lunch": """
        * Veg Kolhapuri
        * Puri
        * Mix Kothal
        * Dal Fry
        * Mutter Rice
        * Roti
        * Green Salad
        * Onion & Lemon
        * Buttermilk
        """,
        "Hi-Tea": """
        * Tea, Milk, Coffee
        """,
        "Dinner": """
        * Cheese Corn Soup
        * Live Dhokla
        * Aloo Tamatar
        * Plain Kadhi
        * Rajwadi Khichdi
        * Lasun Ki Chatni
        * Palak Tawa Paratha
        * Roti
        * Frymes
        * Onion & Lemon
        """
    },
    date(2026, 3, 13): {
        "Breakfast": """
        * Dal Pakwan With Chatni
        * Fruit + Sev Khamani With Chatni
        """,
        "Lunch": """
        * Veg Kadai Masala
        * Kala Chana Masala
        * Dal Fry
        * Plain Rice
        * Roti
        * Green Salad
        * Onion & Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Tomato Corn Bharta
        * Aloo Bhindi Masala
        * Dal Makhani
        * Jeera Rice
        * Roti
        * Onion & Lemon
        * Frymes
        * Pineapple Halwa
        """
    },
    date(2026, 3, 14): {
        "Breakfast": """
        * Suji Ka Upma With Coconut Chatni
        * Fruit
        * Veg Sandwich + Mix Sprouts
        """,
        "Lunch": """
        * Paneer Handi Masala
        * Cabbage Mutter Dry
        * Dal Mix Tadka
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
        * Tomato Soup
        * Navtad Samosa
        * Pav Bhaji
        * Dum Biryani
        * Boondi Raita
        * Masala Papad
        * Veg Hakka Noodles
        * Onion & Lemon
        * Sweet Shrikhand
        """
    },
    date(2026, 3, 15): {
        "Breakfast": """
        * Paneer Paratha With Curd & Pickle
        * Fruit + Khakra
        """,
        "Lunch": """
        * Masala Dhosa
        * Idli Masala
        * Mix Uttapam
        * Aloo Vada
        * Tomato Rice
        * Vada Sambhar
        * Coconut Chatni
        * Sweet Lassi
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Tawa Paneer Masala
        * Soya Mutter Dry
        * Dal Mix Tadka
        * Jeera Rice
        * Roti + Puri
        * Onion & Lemon
        * Ice Cream
        """
    }

}

