# messageanalysisbot  
Discord bot that reads the past 10,000 messages in the current channel for the requested user(s) messages and displays the top 3 most frequent message themes.
Uses Google Natural Language API for word processing

Required software:
1. Google Cloud SDK
2. Natural Language API access
3. DiscordPy
4. Discord Bot setup
5. Beautiful Soup
6. Requests 

On every run:
1. set environment variable: $env:GOOGLE_APPLICATION_CREDENTIALS="discordbot-sentence-analysis-e100955d75a7.json" in PowerShell


Backstory:
It started in my university's Discord server. There was this person who was constantly setting herself up for jokes by saying stuff like 
"back in my day" or "when I was your age", and got slightly annoyed when the jokes were made. 
So, I set out to create a bot that would scan a user's messages and come up with a number that would show a % of messages fitting a theme; 
in this example, it would scan her messages and return a number showing that she did or did not have a propensity to set herself up for the ensuing jokes.
Then, I realized that instead of building my own primitive way of doing this - using webscraping to find synonyms for the requested theme and then check those against the messages sent by the user, 
and instead use a much more robust API, provided by Google, to make this project a lot cleaner, accurate and efficient.

Added features: 
1. Picture search - used webscraping techniques, powered by Requests and BeautifulSoup to make the bot post 3 of the top results for a particular search term
2. Urban dictionary definition lookup