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
    "object": {

        "internet_traffic": {
            "vocabulary": ["internet_traffic", "internet traffic"],
            "sub_option_1": {}
        },

        "intranet_traffic": {
            "vocabulary": ["intranet_traffic", "intranet traffic"],
            "sub_option_1": {}
        },

        "all_traffic": {
            "vocabulary": ["all_traffic", "all traffic"],
            "sub_option_1": {}
        },

        "supply_chain_operator": {
            "vocabulary": ["supply_chain_operator", "supply chain operator"],
            "sub_option_1": {}
        },

        "island_operator": {
            "vocabulary": ["island_operator", "island operator"],
            "sub_option_1": {}
        },
    },

    "subject": {

        "ip_address": {
            "vocabulary": ["ip_address", "192.168.1.2"],
            "sub_option_1": {}
        },

        "username": {
            "vocabulary": ["username1", "username2"],
            "sub_option_1": {}
        },

        "wallet_id": {
            "vocabulary": ["some_wallet_id", "some wallet id"],
            "sub_option_1": {}
        },

        "did": {
            "vocabulary": ["some_did", "some did"],
            "sub_option_1": {}
        },
    },

    "condition": {

        "if": {
            "vocabulary": ["if", "IF", "If"],
            "sub_option_1": {}
        },
    },

    "reaction": {

        "then": {
            "vocabulary": ["then", "Then", "THEN"],
            "sub_option_1": {}
        },
    },
    
    "occurance": {

        "occurance": {
            "vocabulary": ["appears", "accurs"],
            "sub_option_1": {}
        },
    },

    "time": {

        "time": {
            "vocabulary": ["time", "times"],
            "sub_option_1": {}
        },
    },

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
            "vocabulary": ["blocked", "can not", "no_authorise_access", "not authorize"],
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
