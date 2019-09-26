import json

class ad_audit:
    def __init__(self):
        self.level = 1
        self.struct =  {
        1: {
            'title': 'Are they getting impressions?\n', 
            True: {
                2: {
                    'title': 'Are they getting clicks?\n',
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
                                                'action': 'add more channels'
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
                                    6: {
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
                    'title': 'Is the ad showing at all?\n',
                    True: {
                        3: {
                            'action': 'Broaden audience using spyfu or facebook audiences'
                        }
                    },
                    False: {
                        'action': 'Optimize bids'
                    }
                }
            }
        }
    }

    def validate_answer(self, answer):
        affirmative_answers = ['yes', 'y', 'yup', 'high']
        negative_answers = ['no', 'n', 'nope', 'low']

        if answer.lower() in affirmative_answers:
            return True
        elif answer.lower() in negative_answers:
            return False
        else:
            return "error"

    def run(self, struct):
        struct = json.loads(struct)
        question = struct[str(self.level)].get('title')

        if question:
            return True, question
        elif question == None:
            action = struct[str(self.level)].get('action')
            return False, action

    def answer(self, answer, struct):    
        proceed = self.traverse(answer, struct)
        if proceed == False:
            return 'Error: input not accepted'
            # answer = input(question)
            # proceed = self.traverse(answer, struct)

    def traverse(self, answer, struct):
        proceed = self.validate_answer(answer)
        if proceed != 'error':
            struct = json.dumps(struct[str(self.level)][str(proceed).lower()])
            self.level = self.level + 1
            self.run(struct)
        else:
            return False

