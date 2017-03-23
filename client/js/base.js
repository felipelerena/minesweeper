var game_id = null;

function init(){
    superagent
        .post('/games')
        .send({"cols": 20, "rows": 20, "mines": 50})
        .end(game_created);
}

function game_created(err, data){
    game_id = data.body.game_id;
    populate_table(data.body); 
}

function populate_table(data){
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
    // TODO: should manage any kind of error that can happen here.
    var dataset = event.target.dataset;
    if(dataset.clicked == "false"){
        superagent
            .put('/cells/' + game_id + "/" + dataset.row + "/" + dataset.col)
            .send({"action": "click"})
            .end(game_updated);
    }
}

function game_updated(err, data){
    // TODO: should manage any kind of error that can happen here.
    populate_table(data.body); 
}
