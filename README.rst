OK, I have five hours to do this, so my strategy will be to treat it as if I'm doing a (verbose) proof of concept

Required items
==============
* Design and implement a documented RESTful API for the game (think of a mobile app for your API)
* Implement an API client library for the API designed above. Ideally, in a different language, of your preference, to the one used for the API
* When a cell with no adjacent mines is revealed, all adjacent squares will be revealed (and repeat)
* Ability to 'flag' a cell with a question mark or red flag
* Detect when game is over
* Persistence
* Time tracking
* Ability to start a new game and preserve/resume the old ones
* Ability to select the game parameters: number of rows, columns, and mines
* Ability to support multiple users/accounts

Log
===
I will start by creating the repo, setting the basic structure for the project.

The "game part" took me more than expected. I still don't have a client and persistance.
I don't know if I will have time to validate anything or handling many errors.

I fixed the API, now I'm starting with the client.

I created a basic client, i'm serving the static files from the same flask instance because of time constraints.

I finished the game. I didn't implement the question mark because I'm running out of time, but I think I can implement it in half an hour.
The finished game doesn't look very nice, with the flag and the mine in the same cell. I can make that super nice in half an hour.
