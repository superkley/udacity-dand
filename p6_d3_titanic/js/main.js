/**
 * Titanic visualization main functions and related
 **/
//-----------------------------------------------------------------
// variables, constants and utilities
//-----------------------------------------------------------------
// i18n dictionaries
var translations = {
    "survival": "Survival Status",
    "pclass": "Ticket Class",
    "sex": "Sex",
    "age": "Age Group",
    "pgroup": "Sex/Age Group"
};


// simple translate function
function translate(msg) {
    return translations[msg];
}

// return empty array if string is empty otherwise return split string
function splitIgnoreEmptyString(value, sep = ",") {
    var split = value.split(sep);
    if (split[0]) {
        return split;
    } else {
        return [];
    }
}

// return last array element
function lastElement(arr) {
    return arr[arr.length - 1];
}


//-----------------------------------------------------------------
// page navigation
//-----------------------------------------------------------------

function selectStepByName(name) {
    // set active step
    $(".ui.steps .step")
        .removeClass("active");
    $(".ui.steps *[data-name='" + name + "']")
        .addClass("active");
    // set active tab
    $.tab("change tab", name);
    // prevent default browser behaviour in <a>
    return false;
}

function selectCategories(selected) {
    // set selected categories
    $(".ui.dropdown")
        .dropdown("set selected", selected);
}


//-----------------------------------------------------------------
// page initialization
//-----------------------------------------------------------------
var tableInitialized = false;

function initializeMenu() {
    $(".menu.main")
        .visibility({
            type: "fixed"
        });
}

function initializeTabs() {
    // initialize ui controls
    $(".ui.dropdown")
        .dropdown();
    $("#categories")
        .on("change", plotCharts);
    $("#showDistributions")
        .on("change", plotCharts);
    selectStepByName("read");
    selectCategories(["pclass"]);
}

function initializeSteps() {
    $(".ui.steps .step")
        .on("click", function () {
            var name = $(this)
                .data("name");
            selectStepByName(name);
			
			// step specific actions
            if (name == "explore") {
                plotCharts();
            } else if (name == "dig" && !tableInitialized) {
                tableInitialized = true;
                initializeTable();
            }
        });
}

//-----------------------------------------------------------------
// document ready
//-----------------------------------------------------------------

$(document)
    .ready(function () {
        initializeMenu();
        initializeTabs();
        initializeSteps();
    });
