// Activity over time
function createCoverGraphs(){
    var data = {
        labels: ["January", "February", "March", "April", "May", "June", "July"],
        datasets: [
            {
                label: "My First dataset",
                fillColor: "rgba(220,220,220,0.2)",
                strokeColor: "rgba(220,220,220,1)",
                pointColor: "rgba(220,220,220,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(220,220,220,1)",
                data: [65, 59, 80, 81, 56, 55, 40]
            },
            {
                label: "My Second dataset",
                fillColor: "rgba(151,187,205,0.2)",
                strokeColor: "rgba(151,187,205,1)",
                pointColor: "rgba(151,187,205,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(151,187,205,1)",
                data: [28, 48, 40, 19, 86, 27, 90]
            }
        ]
    };
   var options = {
      bezierCurveTension : 0.3,
      scaleShowGridLines : false,
      scaleFontColor: "#FFFFFFF",
   };
   var ctx = document.getElementById("graph").getContext("2d");
   var myLineChart = new Chart(ctx).Line(data, options);
}

function createProfileGraphs(){
  var data = [
      {
          value: 100,
          color:"#F7464A",
          highlight: "#FF5A5E",
          label: "Anime"
      },
      {
          value: 40,
          color: "#46BFBD",
          highlight: "#5AD3D1",
          label: "TV"
      },
      {
          value: 60,
          color: "#FDB45C",
          highlight: "#FFC870",
          label: "Manga"
      },
      {
          value: 40,
          color: "#BBB45C",
          highlight: "#CCC45C",
          label: "Games"
      },
      {
          value: 30,
          color: "#FDB4BB",
          highlight: "#FFC4CC",
          label: "Books"
      }
  ]
   var options = {};
   var ctx = document.getElementById("main-pie").getContext("2d");
   var myPieChart = new Chart(ctx).Pie(data,options);
// 

  var data = [
      {
          value: 100,
          color:"#27464A",
          highlight: "#2F5A5E",
          label: "Anime"
      },
      {
          value: 40,
          color: "#4600BD",
          highlight: "#5A00D1",
          label: "TV"
      },
      {
          value: 60,
          color: "#FD245C",
          highlight: "#FF2870",
          label: "Manga"
      },
  ]

   var ctx = document.getElementById("genre-pie").getContext("2d");
   var myPieChart = new Chart(ctx).Pie(data,options);

//
   var data = {
    labels: ["1", "2", "3", "4", "5", "6","7","8","9","10"],
    datasets: [
        {
            label: "My First dataset",
            fillColor: "rgb(220,220,0)",
            strokeColor: "rgba(220,220,220,0.8)",
            highlightFill: "rgba(220,220,10,0.75)",
            highlightStroke: "rgba(220,220,10,1)",
            data: [65, 59, 80, 81, 56, 55, 40,20,51,67]
        }
    ]
   };
   var options = {
     scaleShowGridLines : false,
   }
   var ctx = document.getElementById("rating-barchart").getContext("2d");
   var myPieChart = new Chart(ctx).Bar(data,options);



}