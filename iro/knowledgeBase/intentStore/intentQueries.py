


def query_single_vocab(word):
    query =  {
        "query": {
            "nested": {
                "path": "vocabularies",
                "query": {
                    "nested": {
                        "path": "vocabularies.vocab_values",
                        "query": {
                            "bool": {
                                "must": [
                                    { "match": { "vocabularies.vocab_values.vocab_value.ngrams": word } }
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        }
    return query
def query_two_vocab(word1, word2):
    query = {
        "query": {
            "nested": {
                "path": "vocabularies",
                "query": {
                  "bool": {
                    "must": [
                        {
                            "nested": {
                                "path": "vocabularies.vocab_values",
                                "query": {
                                    "bool": {
                                        "must": [
                                            { "match": { "vocabularies.vocab_values.vocab_value.ngrams": word1 } }
                                            ]
                                        }
                                    }
                                }
                            },
                        {
                            "nested": {
                                "path": "vocabularies.vocab_values",
                                "query": {
                                    "bool": {
                                        "must": [
                                            { "match": { "vocabularies.vocab_values.vocab_value.ngrams": word2 } }
                                            ]
                                        }
                                    }   
                                }
                            }
                        ]
                     }
                    }
                }
            }
        }
    return query
def query_intentname(word):
    query = {
        "query": {
            "match": { "intentname.ngrams": word }
            }
        }
    return query

def query_all():
    query = {
        "query" : {
            "match_all" : {}
            }
        }
    return query