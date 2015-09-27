function show_details(){
    document.getElementById('details').className = "show-result";
    document.getElementById('result').className = "hide-result";
}

document.getElementById('show-details').onclick = show_details;

function hide_details(){
    document.getElementById('details').className = "hide-result";
    document.getElementById('result').className = "show-result";
}

document.getElementById('hide-details').onclick = hide_details;

function result_insect(result){


    if (result.length == 1) {
        document.getElementById('result-img').className = "no-insect";
        document.getElementById('result-text').innerHTML = "No insect call(s) found";
        document.getElementById("citation").innerHTML = ""
        var errorMessage = "</br></br></br>"
        document.getElementById('filename').innerHTML = errorMessage.concat(result[0]);
        document.getElementById('details-text-insects').innerHTML = "";
    }

    else {
        var summary = "</br></br> Name";
        summary = summary.concat(" : ", String(result[0]), "</br> </br>");

        var insects = ["Cicada", "Bush Cricket", "Cricket", "Grasshopper", "Mole Cricket", "No Insect"];
        var classNames = ["cicada", "bush-cricket", "cricket", "grasshopper", "mole-cricket", "no-insect"];
        
        var probs = " : "
        probs = probs.concat(String(result[1]));
        probs = probs.concat("s");

        probs = probs.concat("</br> : ", String(result[2]), "</br></br>");

        probs = probs.concat(": Probabilities </br>");

        
        var max = 0;
        var maxInsect;
        var maxClass;

        for (i=3; i<result.length; i++ ){
            probs = probs.concat(" : ", String(result[i]), "</br>");
            prob = parseFloat(result[i]);
            if (prob > max){
                max = prob;
                maxInsect = insects[i-3];
                maxClass = classNames[i-3];
            }
        }

        var main_result = maxInsect.concat(" call(s) found.");
        document.getElementById("result-img").className = maxClass;
        document.getElementById("result-text").innerHTML = main_result;
        if (maxInsect == "Cicada" || maxInsect == "No Insect"){
            document.getElementById("citation").innerHTML = ""
        }
        else {
            document.getElementById("citation").innerHTML = "Credit: Orthoptera Recording Scheme, <a href=\"http://www.orthoptera.org.uk/\">http://www.orthoptera.org.uk/</a>"
        }

        document.getElementById("filename").innerHTML = summary;
        document.getElementById("details-text-probs").innerHTML = probs;

    }

}


document.getElementById('goback1').onclick = reload_page;
document.getElementById('goback2').onclick = reload_page;

function reload_page(){
    document.location = window.location;
}