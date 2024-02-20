import random
import numpy as np
import skfuzzy as fuzz
import skfuzzy.control as ctrl

severity = ctrl.Antecedent(np.arange(0, 11, 1), 'severity')
severity['poor'] = fuzz.trimf(severity.universe, [0, 0, 5])
severity['moderate'] = fuzz.trimf(severity.universe, [0, 5, 10])
severity['severe'] = fuzz.trimf(severity.universe, [5, 10, 10])


response = ctrl.Consequent(np.arange(0, 11, 1), 'response')
response['ignore'] = fuzz.trimf(response.universe, [0, 0, 5])
response['respond'] = fuzz.trimf(response.universe, [0, 5, 10])
response['emergency'] = fuzz.trimf(response.universe, [5, 10, 10])

# Define fuzzy rules
rule1 = ctrl.Rule(severity['poor'], response['ignore'])
rule2 = ctrl.Rule(severity['moderate'], response['respond'])
rule3 = ctrl.Rule(severity['severe'], response['emergency'])

response_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
response_sim = ctrl.ControlSystemSimulation(response_ctrl)

def game(chatop, chatip,voiceRec):
    score = 0
    while True:
        # Generate a random road issue
        road_issues = ['pothole', 'debris on the road', 'broken traffic light','roadworks','flooding']
        issue = random.choice(road_issues)
        chatop('There is a ' + issue + ' on the road.')

        # Get player input for severity of the road issue
        chatop('How severe is the road issue? Enter a number between 0 and 10: ')
        severity_input = int(chatip(voiceRec))
        response_sim.input['severity'] = severity_input
        response_sim.compute()
        response_level = response_sim.output['response']
        chatop('Your response level is:' + str(response_level))
        if (issue == 'pothole' and response_level >= 5) or (issue == 'debris on the road' and response_level >= 1 and response_level <= 5) or (issue == 'broken traffic light' and response_level >= 8) or (issue == 'roadworks' and response_level >= 6) or (issue == 'flooding' and response_level >= 6):
            score += 10
            chatop('You responded well. Your score is : ' + str(score))
        else:
            score = +0
            chatop('You responded poorly! Your score is : ' + str(score))

        # Ask player if they want to play again
        chatop('Do you want to play again? Enter or say  y or n: ')
        play_again = chatip(voiceRec)
        if play_again == 'n':
            break