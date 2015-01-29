$(document).ready(function(){

    function update(data){
        $("#move").text(data.turn);
        $("#board").text(getBoardText(data.board));
        if (data.game_over){
            alert(data.winning_team + " wins!")
        }
    }

    function debug(data){
        $("#debug").text(data);
    }

    function getBoardText(board){
        text = "";
        for (var r = 0; r < board.length; r++){
            row = board[r];
            for (var c = 0; c < row.length; c++){
                text += row[c] + " ";
            }
            text += "\n";
        }
        return text;
    }

    function newGame(){
        $.post("/ttt/new", "", update, "json");
    }

    function makeMove(){
        var coords = {"row": $("#row").val(), "col": $("#col").val()};
        $.ajax({
            type: "POST",
            url: "/ttt/move",
            data: JSON.stringify(coords),
            success: update,
            dataType: "json",
            contentType: "application/json; charset=UTF-8"});
    }

    function getStatus(){
        $.get("/ttt/status", "", update, "json")
    }

    getStatus()
    $("#new").click(newGame);
    $("#move").click(makeMove);
})

