/**
 * Chart functions and related
 **/
//-----------------------------------------------------------------
// constants and configurations
//-----------------------------------------------------------------
var chartWidth = 700;
var chartHeight = 280;
var idFrequencies = "frequencies";
var orders = {
    "survival": ["Survived", "Died"],
    "sex": ["Male", "Female"],
    "pclass": ["Upper", "Middle", "Lower"],
    "age": ["Children", "Adults", "Seniors"],
    "pgroup": ["Children", "Male Adults", "Female Adults", "Seniors"]
};
var defaultColors = [
    "dimple-first",
    "dimple-second",
    "dimple-third",
    "dimple-fourth"
];
var ageGroups = {
    "children": "0 - 14",
    "adults": "15 - 64",
    "seniors": "65 - ∞"
};
var survivalRateExplanations = {
	"": "Only 41% of the passengers survived in the Titanic disaster.",
	"sex": "Females had the greatest chance (>75%) to survive. ",
	"age": "Children had the greatest chance (>59%) to survive. ",
	"pclass": "Passengers in the upper class had the greatest chance (>65%) to survive.",
	"age_pclass": "Adults from the upper class had the greatest chance (>67%) to survive.",
	"pclass_sex": "Females from the upper class had the greatest chance (>96%) to survive.",
	"age_sex": "Female adults in the upper class had the greatest chance (>77%) to survive.",
	"age_pclass_sex": "Female adults in the upper class had the greatest chance (>97%) to survive."
};
var distributionExplanations = {
	"": "Only 41% of the passengers survived in the Titanic disaster.",
	"sex": "Most passengers were male.",
	"age": "Most passengers were adults.",
	"pclass": "Most passengers were in the lower class.",
	"age_pclass": "In all three ticket classes there were mainly adults. In lower classes there were more children. Most of the seniors were in the upper class.",
	"pclass_sex": "There were consistently more males than females in all classes. Most of the males were in the lower class. ",
	"age_sex": "Most of the passengers were adults and male. All seniors were male.",
	"age_pclass_sex": "Most children and male adults were in the lower class. Female adults were almost equally distributed in all classes. Most seniors were in the upper class."
};

//-----------------------------------------------------------------
// main chart functions
//-----------------------------------------------------------------
var charts = [];

function plotCharts() {
    removeCharts();

    var categories = splitIgnoreEmptyString(d3.select("#categories").property("value"));
    var showDistributions = d3.select("#showDistributions").property("checked");
    var dataFile = getDataFile(categories);

    d3.csv(dataFile, function (data) {
        d3.select("#chart-title")
            .text(getChartTitle(showDistributions, categories));
		d3.select("#chart-description")
			.text("- " + getChartDescription(showDistributions, categories));

        // draw chart(s) depending on the selected categories		
        switch (categories.length) {
        case 1:
        case 2:
        case 3:
			if (showDistributions) {
				createChart("survival_freq", categories, data);
			} else {
				createChart("survival_rate", categories, data);
			}
            break;
        default:
            createChart("survival", categories, data);
            break;
        }
    });
}

// create chart(s) of a specific type and depending on the selected categories
function createChart(type, selectedCategories, data) {
    switch (selectedCategories.length) {
    case 2:
    case 3:
        var keyCategory = getKeyCategory(selectedCategories);
        var groups = orders[keyCategory];
        for (var i = 0; i < groups.length; i++) {
            var group = groups[i];
            var filteredData = dimple.filterData(data, keyCategory, group);
            filteredData.columns = data.columns.slice(1);
            var chart = createBaseChart(type, filteredData);
            drawCategoryChart(chart, type, selectedCategories, group);
            chart.draw(600);
        }
        break;
    default:
        var chart = createBaseChart(type, data);
        drawCategoryChart(chart, type, selectedCategories);
        chart.draw(600);
        break;
    }
}

// create a basic chart
function createBaseChart(type, data) {
    var svg = dimple.newSvg("#charts", chartWidth, chartHeight)
        .attr("class", "svg-chart");
    var chart = new dimple.chart(svg, data);
    chart.ease = "bounce";
    chart.setMargins(40, 70, 60, 60);
    chart.customClassList = {
        axisLabel: "writing",
        axisTitle: "writing",
        axisTitle: "writing",
        colorClasses: defaultColors
    };
    chart.defaultColors = defaultColors;
    data.totals = calculateFeatureTotals(data);
    charts.push(chart);
    return chart;
}

// draw category specific chart properties
function drawCategoryChart(chart, type, selectedCategories, group = "") {
    var data = chart.data;
	var svg = chart.svg;
    var keyCategory = data.columns[0];
    var categoryColumns = getCategoryColumnsByType(type, data.columns);
    var measureColumns = getMeasureColumnsByType(type, data.columns);

    // create x axis
    var xAxis = chart.addCategoryAxis("x", categoryColumns);
    xAxis.addOrderRule(orders[keyCategory]);
    xAxis.addGroupOrderRule(orders[categoryColumns.last]);

    // create y axis
    var yAxis = chart.addMeasureAxis("y", measureColumns);
    yAxis.hidden = true;

    // create series
    var series = chart.addSeries(keyCategory, dimple.plot.bar);
    if (type == "survival_rate") {
        series.barGap = 0.2;
    } else {
        series.barGap = 0.4;
    }
    series.addOrderRule(orders[keyCategory]);
    series.afterDraw = function (s, d) {
        updateTitleTextAndPosition(xAxis, type, keyCategory, group);
        drawPercentValue(chart, type, s, d);
    };
    series.addEventHandler("mouseover", function (e) {
        addTooltip(chart, type, e);
    });
    series.addEventHandler("mouseleave", function (e) {
        removeTooltips(chart);
    });

    // create legend
    if (type == "survival_rate") {
        drawLegend(svg, "Survived", "dimple-survived");
        drawLegend(svg, "Died", "dimple-died", 1);
    } else if (selectedCategories.length == 3 && selectedCategories[0] == "pclass") {
        drawLegend(svg, ageGroups["children"], defaultColors[0]);
        drawLegend(svg, ageGroups["adults"], [defaultColors[1], defaultColors[2]], 1);
        drawLegend(svg, ageGroups["seniors"], defaultColors[3], 2);
    } else if (lastElement(selectedCategories) == "age") {
        drawLegend(svg, ageGroups["children"], defaultColors[0]);
        drawLegend(svg, ageGroups["adults"], defaultColors[1], 1);
        drawLegend(svg, ageGroups["seniors"], defaultColors[2], 2);
    } else if ($.inArray(group, ["Children", "Adults", "Seniors", "Male Adults", "Female Adults"]) >= 0) {
        var mainGroup = lastElement(group.split(" "));
        drawLegend(svg, mainGroup + ": " + ageGroups[mainGroup.toLowerCase()], []);
    }
}


function drawLegend(svg, text, cssClass, num = 0) {
    var yPos = num * 26 + 18;
    var xPos = chartWidth - 92;

    if (cssClass.constructor === Array) {
        if (cssClass.length >= 2) {
            svg.append("polygon")
                .attr("class", cssClass[1])
                .attr("points", toPoints([
                    [xPos + 10, yPos],
                    [xPos + 10, yPos + 20],
                    [xPos, yPos + 20]
                ]))
                .style("pointer-events", "none");
            svg.append("polygon")
                .attr("class", cssClass[0])
                .attr("points", toPoints([
                    [xPos, yPos],
                    [xPos + 10, yPos],
                    [xPos, yPos + 20]
                ]))
                .style("pointer-events", "none");
        } else {
            xPos -= 30;
        }
    } else {
        svg.append("rect")
            .attr("class", cssClass)
            .attr("x", xPos)
            .attr("y", yPos)
            .attr("height", 20)
            .attr("width", 10)
            .style("pointer-events", "none");
    }
    svg.append("text")
        .attr("class", "dimple-legend")
        .attr("x", xPos + 16)
        .attr("y", yPos + 16)
        .style("pointer-events", "none")
        .text(text);

}

function getChartDescription(showDistributions, categories) {	
	// compose chart explanation
	var explanationKey = Array.prototype.slice.call(categories)
		.sort().join("_");
	if (showDistributions) {
		return distributionExplanations[explanationKey];
	} else {
		return survivalRateExplanations[explanationKey];
	}
}

function getChartTitle(showDistributions, categories) {	
    var title = "Titanic";
	if (categories && showDistributions) {
		title += " Passenger Distribution";
	} else {
		title += " Survivers";
	}
    if (categories) {	
		// compose chart title
        title += " By: ";
        var first = true;
        for (var i = 0; i < categories.length; i++) {
            if (first) {
                first = false;
            } else if (i < categories.length - 1) {
                title += ", ";
            } else {
                title += " and ";
            }
            title += "'" + translate(categories[i]) + "'";
        }
    }
    return title;
}

function getTitleByType(type, keyCategory, group) {
    switch (type) {
    case "survival":
        return "Titanic Survival Rate";
    case "survival_freq":
        if (group) {
            return "'" + group + "' - '" + translate(keyCategory) + "' Distribution";
        } else {
            return "'" + translate(keyCategory) + "' Distribution";
        }
    case "survival_rate":
        if (group) {
            return "Survival Rate By '" + group + "' and '" + translate(keyCategory) + "'";
        } else {
            return "Survival Rate By '" + translate(keyCategory) + "'";
        }
    default:
        return keyCategory;
    }
}

function drawPercentValue(chart, type, s, d) {
    var shape = d3.select(s);
    var sum = getTotalByType(type, chart.data.totals, d.x);
    chart.svg.append("text")
        .attr("x", parseFloat(shape.attr("x")) + parseFloat(shape.attr("width") / 2 - 20))
        .attr(
            "y",
            parseFloat(shape.attr("y")) +
            (shape.attr("height") > 30 ? (shape.attr("height") / 2 + 8) : -10)
        )
        .style("pointer-events", "none")
        .attr("class", "writing")
        .text(toPercent(d.yValue, sum));
}

function addTooltip(chart, type, point) {
    var svg = chart.svg;
    var labelX = parseFloat(point.selectedShape.attr("x")) +
        parseFloat(point.selectedShape.attr("width")) * 0.7;
    var labelY = parseFloat(point.selectedShape.attr("y")) - 40;

    var currentItem = getCurrentItem(type, point.selectedShape);
    svg.append("text")
        .attr("class", "tooltip writing")
        .attr("x", labelX)
        .attr("y", labelY)
        .style("pointer-events", "none")
        .style("text-anchor", "middle")
        .html(currentItem + " (" + point.yValue + ")");
    svg.append("path")
        .attr("class", "tooltip line")
        .attr("transform", "translate(" + labelX + "," + labelY + ")")
        .attr("d", "M 12 8 L -10 40 L -16 25 L 8 36 L -10 38");
}


//-----------------------------------------------------------------
// chart related functions
//-----------------------------------------------------------------

function getCategoryColumnsByType(type, columns) {
    switch (type) {
    case "survival_rate":
        return columns.slice(0, 2);
    default:
        return columns[0];
    }
}

function getMeasureColumnsByType(type, columns) {
    return lastElement(columns);
}

function toPoints(arr) {
    var points = "";
    var first = true;
    for (var i = 0; i < arr.length; i++) {
        if (first) {
            first = false;
        } else {
            points += " ";
        }
        var xy = arr[i];
        points += xy[0] + "," + xy[1];
    }
    return points;
}

function getKeyCategory(categories) {
    if (categories.length == 3) {
        if (categories[0] == "pclass") {
            return "pclass";
        } else {
            return "pgroup";
        }
    } else {
        return categories[0];
    }
}

function getDataFile(categories) {
    var dataFile = "data/survival";
    if (categories.length < 3) {
        for (var i = 0; i < categories.length; i++) {
            dataFile += "_" + categories[i];
        }
    } else {
        if (categories[0] == "pclass") {
            dataFile += "_pclass_pgroup";
        } else {
            dataFile += "_pgroup_pclass";
        }
    }
    return dataFile + ".csv";
}

function removeCharts() {
    while (charts.length) {
        var chart = charts.pop();
        chart.svg.selectAll("*")
            .remove();
    }
    d3.selectAll("#charts *")
        .transition()
        .remove();
}

function removeTooltips(chart) {
    chart.svg.selectAll(".tooltip")
        .remove();
}

function updateTitleTextAndPosition(x, type, keyCategory, group) {
    var title = getTitleByType(type, keyCategory, group);
    var shape = x.titleShape;
    if (title) {
        x.titleShape.text(title);
    }
    shape.attr("y", 20);
}

function calculateFeatureTotals(data) {
    var totals = {};
    var columns = data.columns;
    var freqId = lastElement(columns);
    var sum = 0;
    for (var j = 0; j < columns.length - 1; j++) {
        var catId = columns[j];
        for (var i = 0; i < data.length; i++) {
            var d = data[i];
            var k = d[catId];
            var v = parseInt(d[freqId]);
            if (k in totals) {
                totals[k] += v;
            } else {
                totals[k] = v;
            }
            if (j == 0) {
                sum += v;
            }
        }
    }
    totals['sum'] = sum;
    console.log(totals);
    return totals;
}

function toPercent(fraction, total, precision = 1) {
    if (fraction && total) {
        return (100.0 * fraction / total)
            .toFixed(precision) + "%";
    } else {
        return "NaN";
    }
}

function getCurrentItem(type, selectedShape) {
    var selectedGroups = selectedShape._groups[0][0].__data__.xField;
    if (type == "survival_rate") {
        return selectedGroups[1];
    } else {
        return selectedGroups[0];
    }
}

function getTotalByType(type, totals, xVal) {
    switch (type) {
    case "survival_rate":
        return totals[xVal];
    default:
        return totals["sum"];
    }
}
