import json

print('Follow the instructions below to input the necessary information into a json for the bot to access.')

data = {}
data['keyword'] = input('What is the keyword or keyphrase that you are looking for? \n')
data['message'] = input('What is the initial message? \n')
data['winphrase'] = input('What is the winning response? \n')
data['winner_subject'] = input('What is the subject to the pm that will be sent to the winner? \n')
data['winner_message'] = input('What is the message that will be sent to the winner? \n')
data['max_winners'] = int(input('How many people will win? \n'))
data['max_calls'] = input('What is the maximum amount of posts that you would like to return today? (it can be however large you want). \n')
data['game_over_message'] = input('What would you like the message to be once the game finishes? \n')

with open('reddit_games_info.txt', 'w') as outfile:
    json.dump(data, outfile)

print('Done. your data file has been created.')
