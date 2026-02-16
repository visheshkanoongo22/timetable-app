
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
    },

    date(2026, 2, 9): {
        "Breakfast": """
        * Bataka Poha Sev
        * Veg Sandwich
        * Toast
        * Fruit
        * Bread Butter & Jam
        * Tea & Coffee
        """,
        "Lunch": """
        * Palak Paneer Masala
        * Chole Masala
        * Dal Fry
        * Plain Rice
        * Roti
        * Green Salad
        * Onion Lemon
        * Plain Curd
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Gobhi Mutter Capsicum
        * Dum Aloo Masala
        * Dal Mix Tadka
        * Jeera Rice
        * Roti
        * Onion Lemon
        * Frymes
        """
    },
    date(2026, 2, 10): {
        "Breakfast": """
        * Idli Sambhar Chatni
        * Toast
        * Fruit
        * Bread Butter Jam
        * Mix Uttapam Sambhar
        """,
        "Lunch": """
        * Veg Kohlapuri Masala
        * Rajma Masala
        * Dal Fry
        * Plain Rice
        * Onion Lemon
        * Butter Milk
        * Roti
        * Green Salad
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Sweet Boondi
        * Veg Crispy Dry
        * Dal Mix Tadka
        * Jeera Rice
        * Palak Paratha
        * Roti
        * Onion Lemon
        * Frymes
        """
    },
    date(2026, 2, 11): {
        "Breakfast": """
        * Sandwich Dhokla
        * Bread Pakoda
        * Bread Butter & Jam
        * Tea & Coffee
        * Fruit
        """,
        "Lunch": """
        * Paneer Patiala
        * Kala Chana Masala
        * Lemon Water
        * Plain Rice
        * Dal Fry
        * Roti
        * Salad
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Thepla
        * Kadi Khichdi
        * Bataka Sabji
        * Sev Tameta
        * Tomato Soup
        * Roti
        * Jalebi
        """
    },
    date(2026, 2, 12): {
        "Breakfast": """
        * Upma
        * Corn Flakes
        * Nylon Khaman
        * Bread Butter & Jam
        * Tea & Coffee
        * Fruit
        """,
        "Lunch": """
        * Gajar Mutter
        * Kadi Pakoda
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
        * Aloo Paneer Parotha
        * Papdi Chaat
        * Chana Jor Garam
        * Dahi Vada
        * Dum Biryani
        * Curd
        * Pickle
        """
    },
    date(2026, 2, 13): {
        "Breakfast": """
        * Vada Pav
        * Aloo Sandwich
        * Bread Butter & Jam
        * Tea & Coffee
        * Fruit
        """,
        "Lunch": """
        * Paneer Lababdar
        * Loki Chana
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
        * Cheese Butter Masala
        * Aloo Chips
        * Rice
        * Puri
        * Thepla
        * Butter Milk
        * Roasted Papad
        """
    },
    date(2026, 2, 14): {
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
        * Manchow Soup
        * Pav Bhaji
        * Veg Biryani
        * Boondi Raita
        * Masala Papad
        * Chinees Samosa
        """
    },
    date(2026, 2, 15): {
        "Breakfast": """
        * Aloo Paratha / Paneer Paratha
        * Khakhra
        * Bread Butter & Jam
        * Tea & Coffee
        * Fruit
        """,
        "Lunch": """
        * Rose Lassi
        * Masala Dosa
        * Idli, Aloo Vada
        * Mix Uttapam
        * Mendu Vada Sambhar
        * Coconut Chutney
        * Tomato Rice
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Ice Cream
        * Manchurian Dry
        * Chole Bhature
        * Cheese Corn Soup
        * Frymes
        * Roti
        """
    },

    date(2026, 2, 16): {
        "Breakfast": """
        * Indori Poha with Sev, Lemon + Onion
        * Fruit
        * Veg Sandwich
        * Tea & Coffee
        """,
        "Lunch": """
        * Palak Paneer Masala
        * Moong Chana Mix
        * Dal Mix Tadka
        * Jeera Rice
        * Roti
        * Green Salad
        * Onion + Lemon
        * Buttermilk
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Veg Makhanwadi
        * Jeera Aloo
        * Dal Fry
        * Mutter Rice
        * Raita
        * Onion + Lemon
        * Papad
        """
    },
    date(2026, 2, 17): {
        "Breakfast": """
        * Methi Thepla with Curd & Pickle
        * Fruit
        * Oats Upma
        * Avocado with Chutney
        * Tea & Coffee
        """,
        "Lunch": """
        * Cabbage Mutter Capsicum
        * Rajma Masala
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
        * Sweet Kheer
        * Sarson ka Saag
        * Sev Tamatar
        * Plain Kadhi
        * Rajwadi Khichdi
        * Makai ki Roti
        * Roti
        * Cabbage Sambharo
        * Ghee & Gud
        * Buttermilk
        """
    },
    date(2026, 2, 18): {
        "Breakfast": """
        * Masala Idli with Chutney
        * Fruit
        * Uttapam with Chutney
        * Tea & Coffee
        """,
        "Lunch": """
        * Aloo Ghiloda Masala
        * Kala Chana
        * Dal Fry
        * Plain Rice
        * Roti
        * Onion + Lemon
        * Lemon Water
        """,
        "Hi-Tea": """
        * Tea / Coffee
        """,
        "Dinner": """
        * Veg Broccoli Soup
        * Soy Roll with Chutney
        * Chinese Samosa
        * Mushroom Butter Masala
        * Paneer Butter Masala
        * Dal Makhani
        * Jeera Matar Pulao
        * Palak Paratha
        * Puri
        * Roasted Papad
        * Cold Drinks
        * Malpua
        * Boondi Laddoo
        """
    },
    date(2026, 2, 19): {
        "Breakfast": """
        * Dabeli with Chutney
        * Fruit
        * Nylon Khaman with Kadhi
        * Tea & Coffee
        """,
        "Lunch": """
        * Chole Masala
        * Gajar Mutter Masala
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
        * Cheese Butter Masala
        * Aloo Chips Masala
        * Dal Makhani
        * Plain Rice
        * Roti
        * Puri
        * Roasted Papad
        * Onion & Lemon
        * Malpua
        """
    },
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
    }

}

