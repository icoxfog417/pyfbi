var TABLE = (function(stats){
    var files = Object.keys(stats);
    var dataSet = stats[files[0]];
    var $dropdown = $("<select class='fileFilter'></select>");
    for(f in stats){
        $dropdown.append("<option value='@'>@</option>".replace(/@/g, f));
    }
    $dropdown.change(function(){
        var value = this.value;
        TABLE.clear();
        TABLE.rows.add(STATS[value]);
        TABLE.draw();
    })

    var table = $("#stat_table").DataTable({
        data: dataSet,
        columns: [
            { title: "cnt", data: "ncalls" },
            { title: "self", data: "tottime", render: $.fn.dataTable.render.number(",", ".", 3)},
            { title: "/call", data: "percall_tot", render: $.fn.dataTable.render.number(",", ".", 3)},
            { title: "all", data: "cumtime", render: $.fn.dataTable.render.number(",", ".", 3)},
            { title: "/call", data: "percall_cum", render: $.fn.dataTable.render.number(",", ".", 3)},
            { title: "name", data: "file_name" },
            { title: "@", data: "location" },
            { title: "path", data: "dir_name" }
        ],
        "scrollY": "400px",
        "scrollCollapse": true,
        "paging": false,
        "initComplete": function(){
            $("#stat_table_filter").prepend($dropdown);
        }
    });

    $("#stat_table")

    return table;

})(STATS);

var CHART = (function(element, stats, limit){
    var labels = {};
    var series = {};
    var colors = palette("cb-Pastel2", Object.keys(stats).length);
    for(var f in stats){
        var sData = {};
        for(var i = 0; i < stats[f].length; i++){
            var s = stats[f][i];
            if(s.is_builtin){
                continue;
            }else{
                var index = s.file_name + " " + s.location;
                if(!(index in labels)){
                    labels[index] = s.percall_cum;
                }else{
                    labels[index] += s.percall_cum;
                }
                sData[index] = s.percall_cum;
            }
        }
        series[f] = sData;
    }
    var labelsPairs = Object.keys(labels).map(function(key) {
        return [key, labels[key]];
    });
    labelsPairs.sort(function(first, second) {
        return second[1] - first[1];
    });
    var sortedLabels = labelsPairs.map(function(kv){ return kv[0];});
    sortedLabels = sortedLabels.slice(0, limit)
    labels = [];
    var sortedSeries = [];
    var index = 0
    for(f in series){
        var sorted = sortedLabels.map(function(lb){
            if(lb in series[f]){
                return series[f][lb];
            }else{
                return 0;
            }
        });
        var s = {
            "label": f,
            "data": sorted,
            "backgroundColor": "#" + colors[index]
        }
        sortedSeries.push(s);
        index++;
    }
    series = {};
    var data = {
        labels: sortedLabels,
        datasets: sortedSeries
    }
    
    var ctx = document.getElementById(element).getContext("2d");
    var chart = new Chart(ctx, {
        type: "horizontalBar",
        data: data,
        options: {
            title:{
                display:false,
                text:"Function's Stacked Percall Cumtime"
            },
            tooltips: {
                mode: "index",
                intersect: false
            },
            responsive: true,
            scales: {
                xAxes: [{
                    stacked: true,
                }],
                yAxes: [{
                    stacked: true
                }]
            }
        }
    });

    return chart;

})("statChart", STATS, 30);
