/**
 * Table functions and related
 **/
function initializeTable() {
    d3.csv("data/simplified_titanic_data.csv", function (data) {
        // load csv
        var tr = d3.select("#dig-table")
            .append("tbody")
            .selectAll("tr")
            .data(data)
            .enter()
            .append("tr");

        // create rows
        tr.append("td")
            .html(function (d) {
                return d.Name;
            });
        tr.append("td")
            .html(function (d) {
                switch (d.Pclass) {
                case "1":
                    return "Upper";
                case "2":
                    return "Middle";
                default:
                    return "Lower";
                }
            });
        tr.append("td")
            .html(function (d) {
                return d.Sex;
            });
        tr.append("td")
            .html(function (d) {
                return d.Age;
            });
        tr.append("td")
            .html(function (d) {
                switch (d.Survived) {
                case "1":
                    return "<span class='survived'><i class='smile icon'></i> Yes</span>";
                default:
                    return "<span class='died'><i class='frown icon'></i> No</span>";
                }
            });

        // initialize dynatable
        $("#dig-table")
            .dynatable({
                table: {
                    defaultColumnIdStyle: 'trimDash'
                }
            });
    })
}
