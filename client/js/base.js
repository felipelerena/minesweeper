var game_id = null;

function init(){
    /*
    Creates a new game.
    */
    superagent
        .post('/games')
        .send({"cols": 20, "rows": 20, "mines": 30})
        .end(game_created);
}

function game_created(err, data){
    /*
    * called when received the response for the game created.
    * Arguments:
    *    err -- the error code in case of an error.
    *    data -- the data received from the request.
    */

    // TODO: should manage any kind of error that can happen here.
    // I save the game id and populate the table
    game_id = data.body.game_id;
    populate_table(data.body); 
}

function populate_table(data){
    /*
    * Populates the table.
    *
    * Arguments:
    *   data -- the response.
    */
    var tmpl_source = document.getElementById("tmpl_game");
    var template = Handlebars.compile(tmpl_source.innerHTML);
    var rendered = template({"cells": data.cells});
    
    var game = document.getElementById("game");
    game.innerHTML = rendered;
    var cells = document.querySelectorAll('.cell');
    for (var i=0; i < cells.length; i++) {
        var cell = cells[i];
        cell.addEventListener('click', click_cell);
    }
}

function click_cell(event){
    /*
    * called when received the response for the game created.
    * Arguments:
    *   event -- a click event object.
    */
    // TODO: should manage any kind of error that can happen here.
    var dataset = event.target.dataset;
    var action = null;
    
    if(dataset.clicked == "false"){
        var flagged = document.getElementById("flag").checked;
        if(flagged){
            if(dataset.flagged != "true"){
                action = "flag";
            } else {
                action = "clear"
            }
        } else if(dataset.flagged == "false"){
            action = "click"; 
        }
        if(action != null){
            superagent
                .put('/cells/' + game_id + "/" + dataset.row + "/" + dataset.col)
                .send({"action": action})
                .end(game_updated);
        }
    }
}

function game_updated(err, data){
    /*
    * called when received the response for the game created.
    * Arguments:
    *    err -- the error code in case of an error.
    *    data -- the data received from the request.
    */

    // TODO: should manage any kind of error that can happen here.
    populate_table(data.body); 
}
