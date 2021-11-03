"""
|
|   file:       intent_store.py
|
|   brief:
|   author:     
|   email:      
|   copyright:  © IDA - All rights reserved
"""

Database = {
    "users": {

        "User1": {
            "vocabulary": ["User one", "User number one", "User1"],
            "sub_option_1": {}
        },

        "User2": {
            "vocabulary": ["User two", "User number two"],
            "sub_option_1": {}
        },
    },
    "permission": {

        "allowed": {
            "vocabulary": ["allowed", "can"],
            "sub_option_1": {}
        },

        "blocked": {
            "vocabulary": ["blocked", "can not"],
            "sub_option_1": {}
        },
    },
    "asset": {

        "Domain11": {
            "vocabulary": ["domain 1"],
            "sub_option_1": {}
        },

        "Domain12": {
            "vocabulary": ["domain 2"],
            "sub_option_1": {}
        },

        "realm1": {
            "vocabulary": ["realm 1"],
            "sub_option_1": {}
        },

        "realm2": {
            "vocabulary": ["realm 2"],
            "sub_option_1": {}
        },

        "organization1": {
            "vocabulary": ["organization 1"],
            "sub_option_1": {}
        },
    },
    "spot": {

        "Spot1": {
            "vocabulary": ["Spot1"],
            "sub_option_1": {}
        },

        "Spot2": {
            "vocabulary": ["Spot2"],
            "sub_option_1": {}
        },
    },
    "timeframes": {

        "Morningshift": {
            "vocabulary": ["Morningshift", "Morning"],
            "value": "6 AM - 2 PM",
            "sub_option_1": {}
        },

        "Lateshift": {
            "vocabulary": ["Lateshift", "Late"],
            "value": "2 PM - 10 PM",
            "sub_option_1": {}
        },

        "Nightshift": {
            "vocabulary": ["Nightshift", "Night", "lil"],
            "value": "10 PM - 6 AM",
            "sub_option_1": {}
        },
    },
}
