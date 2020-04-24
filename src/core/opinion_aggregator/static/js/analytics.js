$('#jobsPieChart').ready(function(){
    // Load google charts
    window.alert = function() {};
    google.charts.load('current', {'packages':['corechart']});
});

$('#skillsPieChart').ready(function(){
    // fetch data from db
    $.getJSON("/get_chart_data", {'question': $('#skills').val()}, function(j) {
        google.charts.setOnLoadCallback(function () {
            var categories = [];
            for(key in j){
                categories.push([key, j[key]]);
            }
            drawChart(categories, 'skillsPieChart', 'Skills Popularity');
         });
    })

});

$('#jobsPieChart').ready(function(){
    // fetch data from db
    $.getJSON("/get_chart_data", {'question': $('#jobs').val()}, function(j) {
        google.charts.setOnLoadCallback(function () {
            var categories = [];
            for(key in j){
                categories.push([key, j[key]]);
            }
            drawChart(categories, 'jobsPieChart', 'Job Popularity');
         });
    })

});

// Draw the chart and set the chart values
function drawChart(categories, id, title) {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Categories');
    data.addColumn('number', 'Popularity');
    data.addRows(categories);
    // Optional; add a title and set the width and height of the chart
    var options = {'title':title, 'width':550, 'height':400};

    // Display the chart inside the <div> element with id="piechart"
    var chart = new google.visualization.PieChart(document.getElementById(id));
    chart.draw(data, options);
}