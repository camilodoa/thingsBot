#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAADwyctfcz8BAOxu2fzoZChYSHqgy5TYHuwZAsg1Do4mGN99cvXH3PcJNbbht5TRXsOo4trqwvpehXNLqcuLYZA40TBtZC0ZCVsdzsqztStWIBJBtuUDBbjINJCtazf1pN2HTBbqLCZAQOZC0wMWO0FIeZARiiZBImajtp88xIRbSOQZDZD'
VERIFY_TOKEN = 'ohtokenmytoken'
bot = Bot(ACCESS_TOKEN)

gameInit = False
gameStart = False
participants = []
gameMaster = []
n = 0

thingsQuestions = ['Things cannibals think about while dinning',
'Things dogs are actually saying when they bark', 'Things grown-ups wish they could still do',
'Things you should never put in your mouth', "Things you shouldn't do in a hospital",
"Things you shouldn't do while driving", "Things you shouldn't tell your mother",
"Things paramedics shouldn't say to a patient on the way to the hospital",
"Things you should do when no one is looking", "Things that are harder than they look",
"Things that confirm your life is going downhill", "Things that jiggle",
"Things that make you uncomfortable", "Things that shouldn't be made into video games",
"Things that smell terrible", "Things that squirt", "Things that you can trip over",
"Things you shouldn't do in public", "Things that you shouldn't swallow",
"Things you shouldn't throw off of a building", "Things that your parents would kill you for",
"Things that would be fun to do in an elevator", "Things that would keep you out of heaven",
"Things you wouldn't want to be allergic to", "Things you can never find",
"Things you do to relieve stress", "Things you do to stay warm", "Things you don't want to find in your bed",
"Things you might find in a library", "Things you should be thankful for",
"Things you should give as birthday gifts", "Things you shouldn't put in your mouth",
"Things you shouldn't do while babysitting", "Things you shouldn't do when naked",
"Things you shouldn't do with glue", "Things you shouldn't give trick-or-treaters",
"Things you shouldn't lick", "Things you shouldn't say to your in-laws",
"Things you shouldn't say when walking out of the bathroom", "Things you shouldn't tie to the roof of your car",
"Things you shouldn't carve into a pumpkin", "Things you wish for",
"Things you would buy if you were rich", "Things you would do if you were Bill Gates",
"Things you would rather forget", "Things you wouldn't do for a million dollars"]

usedQuestions = []



#We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        global n
        global gameInit
        global gameStart
        global participants
        global gameMaster

        # #need startgame!
        if not gameInit:
            output = request.get_json()

            for event in output['entry']:
                messaging = event['messaging']

                for message in messaging:

                    if message.get('message'):
                        recipient_id = message['sender']['id']

                        if message['message'].get('text') == 'start':
                            gameInit = True
                            gameMaster = recipient_id
                            send_message(gameMaster, "game is starting -- when you're ready for the first question, message me 'ready'")
                            return 'Message Processed'
                        else:
                            send_message(recipient_id, "message the word 'start' to begin playing!")


        elif gameInit and not gameStart:
            #ask for names
            output = request.get_json()

            messaging = output['entry'][-1]['messaging']

            for message in messaging:

                if message.get('message'):
                    if message['sender']['id'] == gameMaster:
                        if message['message'].get('text') == 'ready':
                            gameStart = True
                            send_message(gameMaster, "to get the next question, message 'next'")

                            send_message(gameMaster, random.choice(thingsQuestions))

                            # if n == len(participants)-1:
                            #     n = 0
                            #     return 'Message Processed'
                            # else:
                            #     n += 1

                            return 'Message Processed'

                        elif message['message'].get('text') == 'next':
                            send_message(gameMaster, random.choice(thingsQuestions))

                            # if n == len(participants)-1:
                            #     n = 0
                            #     return 'Message Processed'
                            # else:
                            #     n += 1

                            return 'Message Processed'

                        elif  message['message'].get('text') == 'stop':
                            send_message(participants[n][0], "bye!")
                            gameStart = False
                            gameInit = False
                            participants[:] = []
                            gameMaster = []
                            return 'Message Processed'


                        else:
                            recipient_id = message['sender']['id']

                            name = message['message'].get('text')
                            #id and name
                            participants.append([recipient_id, name ])

                            send_message(recipient_id, 'Got it, ' + str(name))
                            return 'Message Processed'


                    else:
                        recipient_id = message['sender']['id']

                        name = message['message'].get('text')
                        #id and name
                        participants.append([recipient_id, name ])

                        send_message(recipient_id, 'Game name is ' + name )
                        # send_message(recipient_id, "When you're ready, send 'ready'!")
                        return 'Message Processed'



        else:
            output = request.get_json()


            messaging = output['entry'][-1]['messaging']

            for message in messaging:

                if message.get('message'):
                    if message['sender']['id'] == gameMaster:
                        if message['message'].get('text') == 'stop':
                            send_message(gameMaster, "bye!")
                            gameStart = False
                            gameInit = False
                            participants[:] = []
                            gameMaster = []
                            return 'Message Processed'


                        elif message['message'].get('text') == 'next':
                            send_message(gameMaster, random.choice(thingsQuestions))

                            # if n == len(participants)-1:
                            #     n = 0
                            #     return 'Message Processed'
                            # else:
                            #     n += 1

                            return 'Message Processed'


            return "Message Processed"


       #  # get whatever message a user sent the bot
       # output = request.get_json()
       # print("got json")
       #
       # for event in output['entry']:
       #    messaging = event['messaging']
       #
       #    for message in messaging:
       #
       #      if message.get('message'):
       #          #Facebook Messenger ID for user so we know where to send response back to
       #          recipient_id = message['sender']['id']
       #
       #          if message['message'].get('text'):
       #              response_sent_text = get_message()
       #              print("sending message")
       #              send_message(recipient_id, response_sent_text)
       #
       #          #if user sends us a GIF, photo,video, or any other non-text item
       #          if message['message'].get('attachments'):
       #              print("sending message")
       #              response_sent_nontext = get_message()
       #              send_message(recipient_id, response_sent_nontext)

    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")

    return '983004798'


#chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!", "We're greatful to know you :)"]

    # return selected item to the user
    return random.choice(sample_responses)



#uses PyMessenger to send response to user
def send_message(recipient_id, response):

    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)

    return "success"

if __name__ == "__main__":

    app.run()
