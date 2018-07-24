<?php

session_start();





if(!isset($_SESSION["batcontrol"])) { $_SESSION['batcontrol'] = '0';}
if(!isset($_SESSION["batmotor"])) {$_SESSION['batmotor'] = '0';}
if(!isset($_SESSION["uptime"])) {$_SESSION['uptime'] = '0';}
if(!isset($_SESSION["server"])) {$_SESSION['server'] = 0;}


if(!isset($_SESSION["$diagram_mot"])) {
$_SESSION["$diagram_mot"]=json_decode(file_get_contents('array.json'), true)
;}





?>


<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<style>
	@import 'style.css';
</style>
<script src="jquery.js"></script>
<script src="chart.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.13.0/moment.min.js"></script>




  <head>
  
  </head>
  <body>
    <div class="section">
    
            <div class="container_control"  >
                
                <form action='calc.php' method='POST'>
                  
                <!--<input type="submit" value="Time" name="time" />
                <input type="submit" value="Battery" name="battery" />-->

                <input type="submit" value="Unset" name="unset" /><br>

                <input type="submit" value="Update" name="update" />
                <input type="hidden" name="return_url" value="<?php 
                $current_url = urlencode($url="http://".$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI']);
                echo $current_url; ?>" />

                </form>
            </div>

            <div class="container">

                <b>Batterie</b><br>
                   
                   <?php
                            
                            echo '<span style="color:red">Control: </span>'.$_SESSION['batcontrol'].' V <br>';
                            echo '<span style="color:blue">Motor  : </span>'.$_SESSION['batmotor'].' V <br>';
                        
                   ?>
                <br>
                <b>Uptime</b><br>
                <?php
                            
                            echo 'Uptime: '.$_SESSION['uptime'].' m <br>';
                           
                        
                   ?>


            </div>

            <div class="container">

                <?php
                echo '<b>Diagramm</b><br /><img src="dia01.php" alt="Fehler beim anzeigen" /><br>';

                for ($i=0; $i<count($_SESSION["$diagram_mot"]); $i++)
                {
                   //echo "Mot: ".$i." ".$_SESSION["$diagram_mot"][$i][0]." - ".$_SESSION["$diagram_mot"][$i][1]." - ".$_SESSION["$diagram_mot"][$i][2]."<br>";
                }

                ?>

            </div>
            
            <div class="container" style="padding-left: 10px">

              <canvas id="myLineChart" width="400" height="200"></canvas>

            </div>
     
    </div>
    
    
    
    <div class="section">
    
         <div class="container_control"  >
                
                <form action='calc.php' method='POST'>
                
                    <b>Grasp A</b><br>
                            
                    <input type="submit" value="Relax Grasp" name="opengrabA" /><br>
                    <input type="submit" value="Make Grasp" name="closegrabA" />
                    <input type="submit" value="Turn Grasp" name="turngraspA" />
                    
                    
                    <input type="hidden" name="return_url" value="<?php $current_url = urlencode($url="http://".$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI']); echo $current_url; ?>" />

                </form>
                
                <br><br>
                <form action='calc.php' method='POST'>
                
                    <b>Grasp B</b><br>
                            
                    <input type="submit" value="Relax Grasp" name="opengrabB" /><br>
                    <input type="submit" value="Make Grasp" name="closegrabB" />
                    <input type="submit" value="Turn Grasp" name="turngraspB" />
                    
                    
                    <input type="hidden" name="return_url" value="<?php $current_url = urlencode($url="http://".$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI']); echo $current_url; ?>" />

                </form>
                
                
                
            </div>
            
        <div class="container"  style="width:50%">
        
                <div style="width:100%; display:inline-block">
        
                <img style="width:49%;float:left " src="shot1.jpg" alt="Capture" />
                 <img style="width:49%;float:right " src="shot2.jpg" alt="Lines" />
               
                 </div><br>
                                
                <br>
                 <form action='calc.php' method='POST'>
                
                    <b>Camera Control</b><br>
                    
                     <input type="submit" value="CV" name="cv" /><br> 
                     <input type="submit" value="Capture" name="shot" /><br> <br>
                          
                    <input type="submit" value="Orientation" name="checkcam" /><br>
                    
                    <input type="submit" value="Swap" name="swap" style="width:32%" /> 
                    
                    <input maxlength="4" name="setswapvar" size="4" type="text" style="width:32%"/>
                    <input type="submit" value="Set Swap" name="setswap" style="float:right;width:32%"/><br>
                    
                    <input type="submit" value="Move" name="move" /><br>
                    
                    
                    
                    <input type="hidden" name="return_url" value="<?php $current_url = urlencode($url="http://".$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI']); echo $current_url; ?>" />

                </form>
                </div>
                
         
               
        <div id="demo">
        <?php var_dump($n_data)?>
        </div>
        
         <div class="container_control" id="con_log" style="float:right"  >
                
                
                
        </div>
        
        </div>
    
    
    
  </body>
  <script>
  
var dataPoints = [];
var dataPoints2 = [];

function newDateString(days) {
			return moment().add(days, 'd').format();
		}
        
Date.prototype.formatMMDDYYYY = function() {
      var dd =  (this.getMonth() + 1) +
      "/" +  this.getDate() +
      "/" +  this.getFullYear();
      
  }
  
  
 
    

        
function addData(data) {
  
     // Add a helper to format timestamp data
     
  
 
    
	for (var i = 0; i < data.length; i++) {
		dataPoints.push({
			x: new Date(data[i].date*1000),
			y: data[i].units
		});
	}
	
   
   console.log(dataPoints)

};
function addData2(data) {
  
     // Add a helper to format timestamp data
     
  
 
    
	for (var i = 0; i < data.length; i++) {
		dataPoints2.push({
			x: new Date(data[i].date*1000),
			y: data[i].units
		});
	}
	
   
   console.log(dataPoints)

};

$.getJSON("data.json", addData);
$.getJSON("data3.json", addData2);




  
function drawLineChart() {
   
    // Create the chart.js data structure using 'labels' and 'data'
    var tempData = {
      datasets : [{
          label: "Control",
          fillColor             : "rgba(0,0,255,0.2)",
          strokeColor           : "rgba(0,0,255,1)",
          pointColor            : "rgba(151,187,205,1)",
          pointStrokeColor      : "#fff",
          pointHighlightFill    : "#fff",
          pointHighlightStroke  : "rgba(0,0,255,1)",
          //data                  : [{x:newDateString(0),y:1},{x:newDateString(1),y:5},{x:newDateString(2),y:2}]
          data                  : dataPoints
         
      },{
          label: "Motor",
          fillColor             : "rgba(151,187,205,0.2)",
          strokeColor           : "rgba(255,0,0,1)",
          pointColor            : "rgba(151,187,205,1)",
          pointStrokeColor      : "rgba(255,0,0,1)",
          pointHighlightFill    : "#fff",
          pointHighlightStroke  : "rgba(255,0,0,1)",
          //data                  : [{x:newDateString(0),y:1},{x:newDateString(1),y:5},{x:newDateString(2),y:2}]
          data                  : dataPoints2
         
      }]
    };

    // Get the context of the canvas element we want to select
       
    
    var ctx = document.getElementById("myLineChart").getContext('2d');
    var myChart = new Chart(ctx, {type: 'line', data: tempData,options: {
				responsive: true,
				title:{
					display:true,
					text:"Battery Management"
				},
				scales: {
					xAxes: [{
						type: "time",
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Date'
						},
                        ticks: {
                            major: {
                                fontStyle: "bold",
                                fontColor: "#FF0000"
                            }
                        }
					}],
					yAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Volt'
						}
					}]
				}
    }});
    
};


drawLineChart();

setTimeout(function(){ 

        drawLineChart();
    }, 1000);  

</script>
<script>
var auto_refresh = setInterval(
(function () {
    $("#con_log").load("log.php"); //Load the content into the div
    
}), 1000);
</script>
</html>

