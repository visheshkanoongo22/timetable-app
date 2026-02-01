
from datetime import date

# --- MESS MENU DATA ---
MESS_MENU = {
    # --- PREVIOUS WEEKEND ---
    # 
    date(2026, 1, 24): {
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
    date(2026, 1, 25): {
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
    },

    date(2026, 1, 27): {
        "Breakfast": """
        * Suji Upma
        * Coconut Chutney
        * Dabeli
        * Green Chutney
        * Bread Butter
        * Bread Jam
        * Tea
        * Coffee
        * Milk
        * Fruit
        """,
        "Lunch": """
        * Palak Paneer Masala
        * Moong Masala
        * Mix Dal Tadka
        * Jeera Rice
        * Roti
        * Green Chutney
        * Lemon
        * Onion
        * Plain Curd
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Sweet Jalebi
        * Chinese Samosa
        * Pav Bhaji
        * Dum Biryani
        * Boondi Raita
        * Roasted Papad
        * Veg Hakka Noodles
        * Lemon
        * Onion
        """
    },

    date(2026, 1, 28): {
        "Breakfast": """
        * Masala Idli
        * Green Chutney
        * Mix Uttapam
        * Sambhar
        * Coconut Chutney
        * Bread Butter & Jam
        * Tea, Coffee, Milk
        * Fruit
        """,
        "Lunch": """
        * Gobi Capsicum Mutter Dry
        * Mix Kathol
        * Dal Fry
        * Plain Rice
        * Roti
        * Green Salad
        * Onion, Lemon
        * Butter Milk
        """,
        "Hi-Tea": """
        * Tea, Coffee, Milk
        """,
        "Dinner": """
        * Veg Manchow Soup
        * Live Dhokla
        * Aloo Rasewala
        * Plain Kaddi
        * Rajwadi Khichadi
        * Methi Thepla
        * Lasoon Ki Chutney
        * Roti
        * Frymes
        * Onion, Lemon
        * Suji Ka Halwa
        """
    },
    
    date(2026, 1, 29): {
        "Breakfast": """
        * Methi Ka Thepla With Curd & Pickle
        * Sandwich Dhokla Green Chutney
        """,
        "Lunch": """
        * Veg Makhanwala
        * Rajma Masala
        * Mix Dal Tadka
        * Jeera Rice
        * Roti
        * Green Salad
        * Onion, Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Palak Corn Capsicum
        * Chole Masala
        * Dal Mix Tadka
        * Plain Rice
        * Roti + Puri
        * Onion + Lemon
        * Cabbage Sambharo
        """
    },
    date(2026, 1, 30): {
        "Breakfast": """
        * Bread Pakoda With Chutney & Toast
        * Fruit + Moong Dal Chilla With Chutney
        """,
        "Lunch": """
        * Mutter Paneer Masala
        * Sukhi Bhaji
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
        * Tomato Soup
        * Lilva Kachori
        * Aloo Paneer Paratha
        * Manchurian Fried Rice
        * Papadi Chat
        * Pani Puri
        * Masala Papad
        * Chana Jor Garam
        * Plain Curd
        * Pickle
        """
    },
    date(2026, 1, 31): {
        "Breakfast": """
        * Paneer Paratha
        * Curd
        * Pickle
        * Fruit
        * Veg Sandwich
        """,
        "Lunch": """
        * Veg Jai Puri Masala
        * Masala Maggi
        * Dal Fry
        * Jeera Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Jeera Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Cheese Corn Soup
        * Navratan Samosa
        * Chole Bhature
        * Kadhi
        * Veg Pulao
        * Tomato Raita
        * Ring Onion
        * Green Chilli Fry
        * Masala Papad
        """
    },

    date(2026, 2, 1): {
        "Breakfast": """
        * Mix Paratha
        * Curd
        * Pickle
        * Fruit
        * Veg Sandwich
        """,
        "Lunch": """
        * Mix Veg Masala
        * Ragi Pakoda
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
        * Cheese Butter Masala
        * Soya Mutter Masala
        * Dal Mix Tadka
        * Jeera Rice
        * Roti
        * Onion + Lemon
        * Ice Cream
        """
    },

    date(2026, 2, 2): {
        "Breakfast": """
        * Indori Sev Poha
        * Veg Sandwich
        * Cornflakes
        * Fruit
        * Bread Butter & Jam
        * Tea & Coffee
        """,
        "Lunch": """
        * Veg Handi
        * Mix Kathol
        * Dal
        * Mutter Rice
        * Roti
        * Salad
        * Butter Milk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Paneer Tikka Masala
        * Moong Masala
        * Dal Tadka
        * Rice
        * Roti
        * Frymes
        """
    },
    date(2026, 2, 3): {
        "Breakfast": """
        * Methi Thepla
        * Sev Khamni
        * Toast
        * Bread Butter & Jam
        * Tea & Coffee
        """,
        "Lunch": """
        * Palak Paneer Masala
        * Lauki Chana Masala
        * Dal
        * Rice
        * Roti
        * Dahi
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Chole Bhature / Kulcha
        * Cheese Corn Soup
        * Chinese Samosa
        * Dal
        * Veg Pulav
        * Boondi Raita
        * Roti
        """
    },
    date(2026, 2, 4): {
        "Breakfast": """
        * Sandwich Dhokla
        * Masala Idli - Sambhar
        * Bread Butter & Jam
        * Tea & Coffee
        """,
        "Lunch": """
        * Paneer Patiala
        * Kala Chana Masala
        * Dal Fry
        * Plain Rice
        * Roti
        * Salad
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Ghee - Gud
        * Baigan Ka Bhartha
        * Makke Di Roti / Bajra Ni Roti
        * Veg Crispy
        * Kadhi - Khichdi
        * Gulab Jamun
        """
    },
    date(2026, 2, 5): {
        "Breakfast": """
        * Bread Pakoda
        * Nylon Khaman
        * Bread Butter & Jam
        * Tea & Coffee
        * Fruit
        """,
        "Lunch": """
        * Veg Makhanwala
        * Rajma
        * Dal Tadka
        * Jeera Rice
        * Roti
        * Salad
        * Buttermilk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Pani Puri
        * Aloo Paneer Parotha
        * Papdi Chaat
        * Chana Jor Garam
        * Dahi Vada
        * Dum Biryani
        * Curd
        * Pickle
        """
    },
    date(2026, 2, 6): {
        "Breakfast": """
        * Dabeli
        * Suji Upma
        * Bread Butter & Jam
        * Tea & Coffee
        * Fruit
        """,
        "Lunch": """
        * Paneer Lababdar
        * Guvar Masala
        * Dal Tadka
        * Rice
        * Roti
        * Salad
        * Limbu Pani
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Cheese Butter Masala
        * Dum Aloo
        * Rice
        * Puri
        * Thepla
        * Rosted Papad
        * Butter Milk
        """
    },
    date(2026, 2, 7): {
        "Breakfast": """
        * Dal Pakwaan
        * Toast
        * Bread Butter & Jam
        * Tea & Coffee
        * Fruit
        """,
        "Lunch": """
        * Mix Veg Masala
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
        * Tamato Soup
        * Pav Bhaji
        * Veg Biryani
        * Boondi Raita
        * Masala Papad
        * Gajar-Halwo
        """
    },
    date(2026, 2, 8): {
        "Breakfast": """
        * Aloo Paratha / Paneer Paratha
        * Khakhra
        * Bread Butter & Jam
        * Tea & Coffee
        * Fruit
        """,
        "Lunch": """
        * Veg - Jaipuri Masala
        * Choli Masala
        * Dal Fry
        * Rice
        * Roti
        * Corn Salad
        * Shiro
        * ButterMilk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Daal Baati
        * Churma
        * Besan Gatta Masala
        * Chatni
        * Ghee-Gud
        * Roti
        * Lasun Chutney
        * Ice Cream
        * Buttermilk
        """
    }
}

