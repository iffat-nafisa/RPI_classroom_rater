//For SearchBar
function openSearch(){
    const building = document.getElementById("buildingSearch").value;
    const room = document.getElementById("roomSearch").value;

    //Neither Input provided
    if (building == "" && room == ""){
        //Display error message "User input not provided"
    }
    //Building is not provided (it must be provided)
    else if (building == ""){
        //Display error message "Building input not provided"
    } 
    //Incorrect Format (numbers, symbols, special characters included):
    
    
    //Once basic test cases are done, move on. 
    //Go through the Database and check the information: 
        //Note: room can be user giving room # OR features they want
        //So display results accordingly
    

    //Display that information in the appropriate format: 
    

    //Based on that information recovered, display the following:

    
    //Depending on the user input, do the following:


    if (building == "DCC" && room == "230"){
        window.open("https://pixabay.com/images/search/correct/")
    }
    //If building name input is VALID, then "Add New Classroom" Button is displayed
    else if (building =="DCC"){
        document.getElementById("addNewClassroom").style.display = "block"
    }
    else{
        window.open("https://www.rpi.edu/")
    }

}