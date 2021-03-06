$('#jobsPieChart').ready(function(){
    // Load google charts
    window.alert = function() {};
    google.charts.load('current', {'packages':['corechart']});
});

$('#skillsPieChart').ready(function(){
    // fetch data from db
    $.getJSON("/get_pie_chart_data", {'question': $('#skills').val()}, function(j) {
        google.charts.setOnLoadCallback(function () {
            var categories = [];
            for(key in j){
                categories.push([key, j[key]]);
            }
            drawChart(categories, 'skillsPieChart', 'Skills Popularity', 'pie');
         });
    })

});

$('#jobsPieChart').ready(function(){
    // fetch data from db
    $.getJSON("/get_pie_chart_data", {'question': $('#jobs').val()}, function(j) {
        google.charts.setOnLoadCallback(function () {
            var categories = [];
            for(key in j){
                categories.push([key, j[key]]);
            }
            drawChart(categories, 'jobsPieChart', 'Job Popularity', 'pie');
         });
    })

});

$('#hobbyBarChart').ready(function(){
    // fetch data from db
    $.getJSON("/get_pie_chart_data", {'question': $('#hobby').val()}, function(j) {
        google.charts.setOnLoadCallback(function () {
            var categories = [];
            for(key in j){
                categories.push([key, j[key]]);
            }
            drawChart(categories, 'hobbyBarChart', 'Hobby Popularity', 'pie');
         });
    })

});


$('#industryBarChart').ready(function(){
    // fetch data from db
    $.getJSON("/get_bar_chart_data", {'question': $('#industry').val()}, function(j) {
        google.charts.setOnLoadCallback(function () {
            var categories = [];
            for(key in j){
                categories.push([key, j[key]]);
            }
            drawChart(categories, 'industryBarChart', 'Industry Popularity', 'pie');
         });
    })

});


$('#leadershipPieChart').ready(function(){
    // fetch data from db
    $.getJSON("/get_bar_chart_data", {'question': $('#leadership').val()}, function(j) {
        google.charts.setOnLoadCallback(function () {
            var categories = [];
            for(key in j){
                categories.push([key, j[key]]);
            }
            drawChart(categories, 'leadershipPieChart', 'Leadership', 'pie');
         });
    })
});


$('#businessLeadershipPieChart').ready(function(){
    // fetch data from db
    $.getJSON("/get_bar_chart_data", {'question': $('#businessLeadership').val()}, function(j) {
        google.charts.setOnLoadCallback(function () {
            var categories = [];
            for(key in j){
                categories.push([key, j[key]]);
            }
            drawChart(categories, 'businessLeadershipPieChart', 'Business Leadership', 'pie');
         });
    })

});


$('#majorBarChart').ready(function(){
    // fetch data from db
    $.getJSON("/get_bar_chart_data", {'question': $('#major').val()}, function(j) {
        google.charts.setOnLoadCallback(function () {
            var categories = [];
            for(key in j){
                categories.push([key, j[key]]);
            }
            drawChart(categories, 'majorBarChart', 'Major Popularity', 'bar');
         });
    })

});

$('#neededJobsBarChart').ready(function(){
    // fetch data from db
    $.getJSON("/get_bar_chart_data", {'question': $('#neededJobs').val()}, function(j) {
        google.charts.setOnLoadCallback(function () {
            var categories = [];
            for(key in j){
                categories.push([key, j[key]]);
            }
            drawChart(categories, 'neededJobsBarChart', 'Needed Jobs', 'bar');
         });
    })

});

$('#unneededJobsBarChart').ready(function(){
    // fetch data from db
    $.getJSON("/get_bar_chart_data", {'question': $('#unneededJobs').val()}, function(j) {
        google.charts.setOnLoadCallback(function () {
            var categories = [];
            for(key in j){
                categories.push([key, j[key]]);
            }
            drawChart(categories, 'unneededJobsBarChart', 'Jobs out of favor', 'bar');
         });
    })

});

// Draw the chart and set the chart values
function drawChart(categories, id, title, type) {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Categories');
    data.addColumn('number', 'Popularity');
    data.addRows(categories);

    var screenWidth = $( window ).width();
    if (screenWidth > 1024){
        var options = {'title':title, 'width':'50%', 'height':400};
    }else if(screenWidth > 767 && screenWidth < 1024){
        var options = {'title':title, 'width':'50%', 'height':250};
    }else {
        var options = {'title':title, 'width':'100%', 'height':220};
    }

    // Display the chart inside the <div> element with id="piechart"
    if(type == 'pie'){
        var chart = new google.visualization.PieChart(document.getElementById(id));
        chart.draw(data, options);
    }else{
        var chart = new google.visualization.BarChart(document.getElementById(id));
        chart.draw(data, options);
    }
}