# AireLogicCLI
## Introduction
Welcome to my CLI app for the AireLogic application process.
The aim of the app is to have an application which, when given a name of an artist will provide the average word count of the songs of said artist.
My CLI has this, along with a few additional features.

## Running CLI app + Tests
In order to run the CLI app, you should only have to run main.py via python 3.
I found that running it in bash doesn't update in real time so best results are in an IDE I think (I used VSCode)
Only the extension "requests" is required to run the program.
Install using:

`python -m pip install requests`

To run the tests, use a console with the command: 

`python -m unittest discover -p 'test_*' -b`

## Comments
This is my first time coding a full stack project. I've tried my best over the past few weeks to research what is the best way to do x, y and z when it came to the project, however, as you likely know there is about 30 ways to do some things in python sometimes so without professional guidance I just had to pick the one that made most sense to me and the project.
I tried to have my code as module as I could think of and seperate into layers (like data access layer, business logic and then frontend).

Although I have managed to query the api to get the songs of artists, I feel like there are other ways to do it that would provide a larger amount of data that i could have played with.
I tried a few methods, however, each one of them had artists that didn't work (mostly due to groups vs solo artists) but this method seemed to work tthe best for me.

I've worked on it for a few hours most days monday-friday however, with a full time job and a family to care for it took me longer than I'd hoped for.
Any questions email me at elydoodson@hotmail.co.uk :).