function assignDiceToContainer(dice, container){
    // Assigns dice image to a container
    container.appendChild(dice);
}

function emptyContainer(container){
    // Reset dice assigned to this container
    const dices = container.querySelectorAll('.dice-img');
    if (dices == null) {
        return;
    }
    dices.forEach((dice) => {
        resetDice(dice)
    })
}

function allowDrop(event) {
    event.preventDefault();
}

function dragStart(event) {
    // Set the dragged element's ID
    event.dataTransfer.setData("dice-id", event.target.id);
}

function drop(event) {
    event.preventDefault();
    const diceId = event.dataTransfer.getData("dice-id");
    const dice = document.getElementById(diceId);
    const target = event.target;

    var container = null;

    if (!(dice.classList.contains("dice-img"))) {
        return;
    }

    if (target.classList.contains("dice-img")) {
        container = target.parentNode;
    }
    else if ((target.classList.contains("drop-container") | (target.classList.contains("start-container")))) {
        container = target;
    }
    else {
        return;
    }

    emptyContainer(container);

    // Check if the drop target is a valid container
    assignDiceToContainer(dice, container);

    // Calculate and display the sum for the group
    updateGroupSolution(0);
    updateGroupSolution(1);
}


function resetDice(dice) {
    // Get original container
    const imageId = dice.getAttribute("image-id");
    const defaultContainer = document.getElementById(`start${imageId}`);
    defaultContainer.appendChild(dice);
}

function resetDices() {
    const dices = document.querySelectorAll('.dice-img');
    dices.forEach((dice) => {
        resetDice(dice)
    })

    // Reset group sums
    updateGroupSolution(0);
    updateGroupSolution(1);
}

document.addEventListener("dragstart", function (event) {
    dragStart(event);
});


function updateOperations(group, operator) {
    // Get value
    const operation = document.getElementById(`operation-${group}-${operator}`).value;
    // Set value to the other operator
    const otherOperator = 1 - operator;
    document.getElementById(`operation-${group}-${otherOperator}`).value = operation;

    // Reset group sums
    updateGroupSolution(0);
    updateGroupSolution(1);
}


function calculateGroupSolution(group) {
    const operation = document.getElementById(`operation-${group}-0`).value;

    var values = [];
    // Retrieve values
    for (var i = 0; i < 3; i++) {
        const dice = document.getElementById(`drop-container${group}-${i}`).querySelector(".dice-img");;
        var value = null
        // Assign neutral values if no image
        if (dice == null) {
            if ((operation == "+") | (operation == "-")) {
                value = 0;
            }
            if ((operation == "x") | (operation == "÷")) {
                value = 1;
            }
        } else {
            value = parseInt(dice.getAttribute("num-value"));
        }
        values.push(value);
    }

    // Calculate result
    var result = null;
    switch (operation) {
        case "+":
            result = values[0] + values[1] + values[2];
            break;
        case "-":
            result = values[0] - values[1] - values[2];
            break;
        case "x":
            result = values[0] * values[1] * values[2];
            break;
        case "÷":
            result = values[0] / values[1] / values[2];
            break;
    }

    return result;
}


function updateGroupSolution(group) {
    result = calculateGroupSolution(group);

    document.getElementById(`group${group}-sum`).textContent = `=${result}`;
}


function savePlayerName() {
    playerName = document.getElementById('player_name_inp').value;
    playerName = playerName.replace(" ", "_");
    document.cookie = 'player_name=' + encodeURIComponent(playerName);
    location.reload();
}


function forfeit() {
    $.ajax({
        type: 'POST',
        url: '/forfeit/',
        success: function(response) {
            localStorage.setItem('response_text', response);
            location.reload();
        },
        error: function(xhr, status, error) {
            console.error('AJAX Error:', error);
            console.log(xhr.responseText);  // Log the response text for more details
        }
    })

}

function checkAllAssigned() {
    var allAssigned = true;
    const dices = document.querySelectorAll(".dice-img");
    dices.forEach((dice) => {
        const container = dice.parentNode;
        if (!(container.classList.contains("drop-container"))) {
        allAssigned = false;
    }
    })
    return allAssigned;
}

function submitSolution() {
    var call_url;
    if ((calculateGroupSolution(0) == calculateGroupSolution(1)) & (checkAllAssigned())){
        call_url = "/solution/"
    } else {
        call_url = "/invalid/"
    }

    $.ajax({
        type: 'POST',
        url: call_url,
        success: function(response) {
            localStorage.setItem('response_text', response);
            location.reload();
        },
        error: function(xhr, status, error) {
            console.error('AJAX Error:', error);
            console.log(xhr.responseText);  // Log the response text for more details
        }
    })
}

$(document).ready(function() {
    // Check if there is a forfeit response in local storage
    var storedResponse = localStorage.getItem('response_text');
    if (storedResponse == null) {
        storedResponse = "Senat Kaszub czeka na Twoje rozwiązanie...";
    } else {
        localStorage.removeItem('response_text');
    }
    $('#response').text(storedResponse);
});