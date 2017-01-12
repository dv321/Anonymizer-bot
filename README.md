# Anonymizer Bot

Anonymizer Bot is a slack app that receives direct messages and posts them anonymously to a specified channel - it's great for companies loooking to collect feedback from employees. The app is currently configured to run on Heroku, but ngrok works well for local development. See https://github.com/slackapi/Slack-Python-Onboarding-Tutorial for more info.

### Installation steps

Setting up Slack apps is a mess, abandon all hope ye who enter here:

* Create a new slack app and set the client id and client secret as SLACK_CLIENT_ID and SLACK_CLIENT_SECRET env vars, respectively

* Go to https://api.slack.com/docs/oauth-test-tokens and set the token as the SLACK_TEST_TOKEN env var

* Run the app

* Paste the address of the app and append '/listening' into the 'request url' field in the Event Subscriptions page. The app should successfully be verified

* Go back to Basic Information and copy the verification token and set it as the SLACK_VERIFICATION_TOKEN env var

* Restart app

* Go to Bot Users, add the name of the bot you want users to interact with. The default is 'anonymizer-bot', update the `BOT_NAME` variable in 'bot.py' if you change it

* In the OAuth Settings page, paste the address of the app and append '/oauth' into the redirect urls form

* Go to localhost:5000/install and authorize the app

* Subscribe to the message.im bot event in the Event Subscriptions. You may have to reauthorize the '/listening' url

* For whatever reason it was necessary to reauthorize the oauth url by going to localhost:5000/install
