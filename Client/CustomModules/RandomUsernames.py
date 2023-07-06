import random



adjectives = ['abject', 'able', 'abnormal', 'aboard', 'above', 'absent', 'absurd', 'actual', 'admiring', 'adorable', 'adoring', 'adventurous',
              'affected', 'aggressive', 'agreeable', 'alert', 'alive', 'aloof', 'amazed', 'amazing', 'amused', 'ancient', 'angry',
              'annoyed', 'anxious', 'ardent', 'arrogant', 'artistic', 'ashamed', 'attractive', 'average', 'awed', 'awful',
              'bad', 'beautiful', 'betrayed', 'better', 'big', 'bitter', 'black', 'blissful', 'blue', 'boastful', 'bold', 'bored', 'brainy',
              'brave', 'brief', 'bright', 'broad', 'bubbly', 'busy', 'calm', 'careful', 'cautious', 'charming', 'cheap', 'cheerful', 'chic',
              'clean', 'clear', 'clever', 'close', 'cocky', 'cold', 'colorful', 'comfortable', 'common', 'confident', 'conscious', 'considerate',
              'constant', 'content', 'conventional', 'cool', 'courageous', 'crazy', 'creative', 'critical', 'cruel', 'crummy',
              'crushed', 'cultured', 'curious', 'cute', 'cynical', 'dark', 'dazzling', 'dead', 'dear', 'debonair', 'decimal',
              'dejected', 'delightful', 'determined', 'difficult', 'diligent', 'discreet', 'distant', 'dopey', 'doubtful', 'dreadful', 'dreamy',
              'dreary', 'dynamic', 'eager', 'eager', 'easy', 'ecstatic', 'efficient', 'elated', 'elegant', 'embarrassed', 'emotional', 'empathic',
              'empty', 'enraged', 'enthusiastic', 'envious', 'equable', 'erratic', 'euphoric', 'exacting', 'excited', 'excluded', 'expensive',
              'extravagant', 'fair', 'faithful', 'famous', 'fancy', 'fantastic', 'fascinated', 'fashionable', 'fast', 'fat', 'fearful', 'fervent',
              'fierce', 'finicky', 'flawless', 'flexible', 'fond', 'forsaken', 'fortunate', 'frank', 'free', 'fresh', 'full', 'funny', 'generous',
              'gentle', 'giddy', 'glamorous', 'gleaming', 'gleeful', 'gloomy', 'goofy', 'graceful', 'greedy', 'grizzled', 'grudging', 'grumpy',
              'guilty', 'guttural', 'happy', 'harmonious', 'hateful', 'healthy', 'helpful', 'helpless', 'high', 'hilarious', 'holistic', 'honest',
              'horrible', 'hot', 'huge', 'humorous', 'hungry', 'hushed', 'ill', 'imaginative', 'impartial', 'imported', 'independent', 'indifferent',
              'innocent', 'innocent', 'insecure', 'interesting', 'intrigued', 'irate', 'jealous', 'jolly', 'joyful', 'joyous', 'jubilant',
              'judgmental', 'jumpy', 'keen', 'kind', 'large', 'lazy', 'lethal', 'little', 'lonely', 'loud', 'lovely', 'lovesick', 'lucky',
              'ludicrous', 'lying', 'mad', 'mad', 'magnificent', 'majestic', 'malicious', 'mean', 'meek', 'melancholic', 'mellow', 'merciful',
              'mere', 'meticulous', 'mild', 'modern', 'morbid', 'murky', 'mysterious', 'nasty', 'naughty', 'needful', 'needy', 'nervous', 'nice',
              'obnoxious', 'obsessed', 'odd', 'offended', 'optimistic', 'outlying', 'overjoyed', 'pacified', 'panicky', 'passionate', 'peaceful',
              'peaceful', 'perfect', 'persistent', 'pesky', 'petty', 'pitiful', 'playful', 'pleasant', 'pleased', 'plucky', 'prideful', 'proud',
              'punctual', 'puzzled', 'quarrelsome', 'quick', 'quiet', 'rebellious', 'reliable', 'relieved', 'remarkable', 'resilient', 'resolved',
              'rich', 'romantic', 'rude', 'sad', 'scared', 'scornful', 'selfish', 'serious', 'shallow', 'shameful', 'sharp', 'sheepish', 'shiny',
              'short', 'shy', 'silly', 'similar', 'sincere', 'smart', 'solemn', 'solid', 'somber', 'somber', 'sore', 'spirited', 'stingy', 'strange',
              'stressed', 'successful', 'sugary', 'superior', 'surprised', 'suspicious', 'taut', 'thoughtful', 'thrifty', 'thrilled', 'tight',
              'tired', 'tolerant', 'tough', 'troubled', 'truculent', 'trusting', 'truthful', 'truthful', 'ugly', 'unhappy', 'unusual', 'vain',
              'vengeful', 'vivacious', 'wakeful', 'warm', 'weak', 'wealthy', 'weary', 'weird', 'winged', 'wonderful', 'worldly', 'wornout', 'worried',
              'worried', 'wrathful', 'yearning', 'young', 'zany', 'zealed', 'zealous', 'zealous', 'zebra', 'zenithal', 'zephyrian', 'zeroed',
              'zeroth', 'zestful', 'zestless', 'zesty', 'zigzag', 'zinciferous', 'zincoid', 'zincous', 'zippy', 'zirconic', 'zirconium', 'zodiacal',
              'zoic', 'zonal', 'zonked', 'zooecium', 'zoogamous', 'zoogenic', 'zoogloeic', 'zoographical', 'zoolatrous', 'zoolithic', 'zoological',
              'zoomantic', 'zoometric', 'zoomorphic', 'zoonal', 'zoophagous', 'zoophoric', 'zoopsychological', 'zootic', 'zootomic', 'zootrophic',
              'zooty', 'zygomorphic', 'zygotic', 'zygous', 'zymogenic', 'zymotic', 'zythum']

nouns = ['abalone', 'alpaca', 'anchovy', 'anemone', 'antelope', 'apples', 'apricots', 'artichoke', 'asparagus', 'aspic', 'avocado',
         'baboon', 'badger', 'bagels', 'baguette', 'barracuda', 'basmati', 'bass', 'beagle', 'bear', 'beetroot', 'bellpepper', 'bison',
         'bittern', 'blackbird', 'blueberry', 'bluefin', 'boa', 'boars', 'bobolink', 'broccoli', 'bruschetta', 'buck', 'budgie',
         'buffalo', 'bull', 'burdock', 'burritos', 'bustard', 'butterfly', 'buzzard', 'cabbage', 'cake', 'camel', 'capybara', 'cardinal',
         'caribou', 'carp', 'carrot', 'caterpillar', 'cauliflower', 'caviar', 'celery', 'cereal', 'chaffinch', 'chamois', 'char',
         'cheese', 'cheesecake', 'cheetah', 'cherry', 'chicken', 'chile', 'chimpanzee', 'chips', 'chocolate', 'chough', 'chowder',
         'chutney', 'clam', 'cloudberry', 'coati', 'cockatoo', 'cockroach', 'coconut', 'cod', 'condor', 'conger', 'cordial', 'coriander',
         'corn', 'couscous', 'cow', 'crab', 'crabapple', 'crackers', 'crane', 'crocodile', 'crow', 'cucumber', 'cupcake', 'cur', 'curd',
         'curlew', 'cuttlefish', 'dachshund', 'damson', 'deer', 'dill', 'dingo', 'dinosaur', 'donkey', 'dorada', 'dotterel', 'doughnut',
         'dove', 'doves', 'duck', 'dunbird', 'durian', 'eagle', 'eclair', 'eel', 'eggs', 'eland', 'elephant', 'empanada', 'emu', 'fajita',
         'falafel', 'falcon', 'ferret', 'ferret', 'fig', 'finch', 'fish', 'flamingo', 'flan', 'fondue', 'frog', 'fruitcake', 'garlic',
         'gatorade', 'gazelle', 'gazpacho', 'gecko', 'gelding', 'gerbil', 'ginger', 'giraffe', 'gnat', 'gnocchi', 'gnu', 'goat',
         'gooseberry', 'gorgonzola', 'gorilla', 'granola', 'grouper', 'guava', 'gull', 'haddock', 'haggis',
         'halibut', 'hamster', 'hare', 'hawk', 'hazelnut', 'hedgehog', 'heron', 'hippopotamus', 'hoopoe', 'hummus',
         'hyena', 'ibis', 'icecream', 'iguana', 'iguana', 'impala', 'inchworm', 'jackal', 'jaguar', 'jambalaya',
         'jelly', 'jerky', 'kangaroo', 'kitten', 'kiwi', 'koala', 'krill', 'kudu', 'ladybug', 'lamprey',
         'lapwing', 'lard', 'lasagna', 'lemongrass', 'lemur', 'lentils', 'leopard', 'linguine', 'lion', 'lizard', 'llama', 'lobster',
         'locust', 'locust', 'lollies', 'lychee', 'macadamia', 'macaroni', 'macaw', 'mackerel', 'magpie', 'magpie', 'maize', 'mallard',
         'manatee', 'mandrill', 'mango', 'mare', 'marmalade', 'marzipan', 'mastiff', 'meadowlark', 'meatball', 'meerkat', 'melon',
         'minnow', 'mint', 'moose', 'morel', 'mosquito', 'moth', 'muesli', 'muffin', 'mullet', 'mung beans', 'mushroom', 'mussel',
         'mussels', 'nachos', 'nectarine', 'newt', 'nougat', 'nutmeg', 'oatcake', 'oatmeal', 'ocelot', 'octopus', 'oil', 'okra', 'olive',
         'omelette', 'onion', 'orange', 'oryx', 'ostrich', 'otter', 'owl', 'oyster', 'paella', 'pancake', 'panda', 'pangolin', 'papaya',
         'parmesan', 'parrot', 'partridge', 'peach', 'peanut', 'pear', 'peasant', 'pelican', 'penguin', 'pepper', 'pepperoni', 'periwinkle',
         'pheasant', 'pie', 'pigeon', 'piglet', 'pike', 'pineapple', 'piranha', 'platypus', 'plover', 'plum', 'polenta',
         'pomegranate', 'ponie', 'popcorn', 'porcupine', 'porpoise', 'potato', 'poultry', 'prawn', 'pretzels', 'prune', 'pudding', 'puffin',
         'puma', 'pumpkin', 'pup', 'quail', 'quiche', 'quinoa', 'rabbit', 'raccoon', 'radish', 'raisins', 'ram', 'raspberry', 'rat',
         'ravioli', 'reindeer', 'relish', 'rhino', 'rhinoceros', 'rice', 'risotto', 'rooster', 'ruffs', 'salamander', 'salami', 'salmon',
         'salt', 'sardines', 'sauerkraut', 'sausage', 'scallops', 'seafowl', 'seagull', 'seahorse', 'sealion', 'shads', 'shark', 'sheep',
         'shrimp', 'skunk', 'sloth', 'smelt', 'snail', 'snapper', 'snipe', 'souffle', 'sparrow', 'spatula', 'spinach', 'squid', 'squirrel',
         'steak', 'stingray', 'stork', 'strawberry', 'swan', 'swift', 'syrup', 'tacos', 'tangerine', 'tarantula', 'tarragon', 'tart', 'teal',
         'termite', 'thrush', 'thrushe', 'toad', 'toadstool', 'tofu', 'tomato', 'tomatoe', 'tortilla', 'tortoise', 'toucan', 'toucan',
         'tripe', 'truffle', 'tuna', 'turkey', 'turtle', 'unicorn', 'venison', 'viper', 'walnut', 'wasp', 'wasp', 'watercress', 'watermelon',
         'weaver', 'wheat', 'whippet', 'whiting', 'widgeon', 'wigeon', 'wildebeest', 'wildfowl', 'wolf', 'wombat', 'yam', 'zebra', 'zebu', 'zucchini']



def generate_username(num_results: int=1, include_numbers: bool=True):
    """
    Generates a random username from a list of adjectives and nouns.
    
    Args:
        num_results (int): The number of usernames to generate. Defaults to 1.
        include_numbers (bool): Whether to include a random number at the end of the username. Defaults to True.
    
    Returns:
        list: A list of usernames.
    """
    usernames = []
    for _ in range(num_results):
        adjective = random.choice(adjectives)
        noun = random.choice(nouns).capitalize()
        num = random.randint(0, 9999)
        if include_numbers:
            usernames.append(f"{adjective}{noun}{num}")
        else:
            usernames.append(f"{adjective}{noun}")
    
    return usernames



