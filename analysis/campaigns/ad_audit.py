import json

class ad_audit:
    def __init__(self):
        self.level = 1
        self.struct =  {
        1: {
            'title': 'Are they getting impressions?', 
            True: {
                2: {
                    'title': 'Are they getting clicks?',
                    True: {
                        3: {
                            'title': 'Is the ad copy and targeting congruent with the landing page copy and graphics?',
                            True: {
                                4: {
                                    'title': 'Are you a/b testing audiences?',
                                    True: {
                                        5: {
                                            'title': 'Are you retargeting and following up via email?',
                                            True: {
                                                6: {
                                                    'title': "Are you a/b testing offers?",
                                                    True: {
                                                        7: {
                                                            'action': 'add more channels'
                                                        }
                                                    },
                                                    False: {
                                                        7: {
                                                            'action': 'a/b test offers'
                                                        }
                                                    }
                                                }
                                            },
                                            False: {
                                                6: {
                                                    'action': 'a/b test audiences'
                                                }
                                            }
                                        }
                                    },
                                    False: {
                                        5: {
                                            'action': 'a/b test audiences'
                                        }
                                    }
                                }
                            },
                            False: {
                                4: {
                                    'action': 'Align campaign architecture'
                                }
                            }
                        }
                    },
                    False: {
                        3: {
                            'action': 'optimize creative and copy'
                        }
                    }
                }
            },
            False: {
                2: {
                    'title': 'Is the ad showing at all?',
                    True: {
                        3: {
                            'action': 'Broaden audience using spyfu or facebook audiences'
                        }
                    },
                    False: {
                        3: {
                            'action': 'Optimize bids'
                        }
                    }
                }
            }
        }
    }

    def validate_answer(self, answer) -> bool:
        affirmative_answers = ['true', 'yes', 'y', 'yup', 'high']
        negative_answers = ['false', 'no', 'n', 'nope', 'low']

        if answer.lower() in affirmative_answers:
            return True
        elif answer.lower() in negative_answers:
            return False
        else:
            return "error"


    def answer(self, answer, struct, level) -> dict:    
        result = self.traverse(answer, struct, level)
        if result == False:
            return 'Error: input not accepted'
        else:
            return json.dumps(result)

    def traverse(self, answer, struct, level):
        struct = json.loads(struct)
        proceed = self.validate_answer(answer)
        if proceed != 'error':
            struct = struct[level][str(proceed).lower()]
            return struct
        else:
            return False

    def parse(self, struct, level) -> str:
        struct = json.loads(struct)
        question = struct[str(level)].get('title')
        if question:
            return True, question
        elif question == None:
            action = struct[str(level)].get('action')
            return False, action
