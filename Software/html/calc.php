 <?php
   // test=$( curl -s --data-binary '{"jsonrpc": "2.0", "methgetreport", "id": 0}' -H 'Accept:' 127.0.0.1:31415 )



session_start();

    
 
                                                         

if(isset($_POST['unset']))
{
     session_unset();
      


 }
 


if(isset($_POST['update']))
{
    /*
$test= exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "getreport", "id": 0}\' -H \'Accept:\' 127.0.0.1:31415');
$json = json_decode($test);
print $json->{'result'};
$manstring = $json->{'result'};
$_SESSION['batmotor']=substr($manstring,16,5);
$_SESSION['batcontrol']=substr($manstring,40,5);





$test= exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "sendcommand", "params":["time#####"],"id": 0}\' -H \'Accept:\' 127.0.0.1:31415');
$json = json_decode($test);
$_SESSION['uptime']=$json->{'result'};
*/
$test= exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "get_state","id": 0}\' -H \'Accept:\' 127.0.0.1:8080');
$json = json_decode($test);
$tmp_res=$json->{'result'};
$teile = explode(";", $tmp_res);

$n_data=json_decode(file_get_contents('data.json'), true);
$arrne['date'] = time();
$arrne['units'] = $teile[13];
array_push( $n_data, $arrne );
file_put_contents("data.json",json_encode($n_data));
$_SESSION['batmotor']=$teile[13];

$n_data=json_decode(file_get_contents('data3.json'), true);
$arrne['date'] = time();
$arrne['units'] = $teile[12];
array_push( $n_data, $arrne );
file_put_contents("data3.json",json_encode($n_data));
$_SESSION['batcontrol']=$teile[12];


}

if(isset($_POST['turngraspA']))
    {
        $test = exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "send_cmd", "params":["turnauto#A"], "id": 1}\' -H \'Accept:\' 127.0.0.1:8080');
    }
    
if(isset($_POST['turngraspB']))
    {
        $test = exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "send_cmd", "params":["turnauto#B"], "id": 1}\' -H \'Accept:\' 127.0.0.1:8080');
    }
    
if(isset($_POST['opengrabA']))
    {
        $test = exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "send_cmd", "params":["opengrab#A"], "id": 1}\' -H \'Accept:\' 127.0.0.1:8080');
    }

if(isset($_POST['opengrabB']))
    {
        $test = exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "send_cmd", "params":["opengrab#B"], "id": 1}\' -H \'Accept:\' 127.0.0.1:8080');
    }
    
if(isset($_POST['closegrabA']))
    {
        $test = exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "send_cmd", "params":["closegrabA"], "id": 1}\' -H \'Accept:\' 127.0.0.1:8080');
    }
    
if(isset($_POST["closegrabB"]))
    {
        $test = exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "send_cmd", "params":["closegrabB"], "id": 1}\' -H \'Accept:\' 127.0.0.1:8080');
    }
    
if(isset($_POST["checkcam"]))
    {
        $test = exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "send_cmd", "params":["turnauto#B"], "id": 1}\' -H \'Accept:\' 127.0.0.1:8080');
    }
    
if(isset($_POST["swap"]))
    {
        //$test= exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "swap", "id": 0}\' -H \'Accept:\' 127.0.0.1:31415');
        $tmp_var = 'swap#####';
        $test = exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "send_cmd", "params":["swap#####"], "id": 1}\' -H \'Accept:\' 127.0.0.1:8080');
        echo $test;
    }
    
if(isset($_POST["setswap"]))
    {
        $tmp_var = '1000';
        if(isset($_POST["setswapvar"]))
        {
            $tmp_var=$_POST["setswapvar"];
        }
        
        
        $test = exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "send_cmd", "params": ["set_swap#' . $tmp_var . '"], "id": 1}\' -H \'Accept:\' 127.0.0.1:8080');
        
    }
    
if(isset($_POST["cv"]))
    {
        $test = exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "send_cmd", "params":["switchir#0\n\r"], "id": 1}\' -H \'Accept:\' 127.0.0.1:8080');
    }
    
if(isset($_POST["shot"]))
    {
        $test = exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "send_cmd", "params":["switchir#1\n\r"], "id": 1}\' -H \'Accept:\' 127.0.0.1:8080');
    }
    
if(isset($_POST["move"]))
    {
        $test= exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "opengrabB", "id": 0}\' -H \'Accept:\' 127.0.0.1:31415');
        $test= exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "turnA", "id": 0}\' -H \'Accept:\' 127.0.0.1:31415');
        $test= exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "orientation", "id": 0}\' -H \'Accept:\' 127.0.0.1:31415');
        $test= exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "closegrabB", "id": 0}\' -H \'Accept:\' 127.0.0.1:31415');
        $test= exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "swap", "id": 0}\' -H \'Accept:\' 127.0.0.1:31415');
        
        $test= exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "opengrabA", "id": 0}\' -H \'Accept:\' 127.0.0.1:31415');
        $test= exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "turnB", "id": 0}\' -H \'Accept:\' 127.0.0.1:31415');
        $test= exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "orientation", "id": 0}\' -H \'Accept:\' 127.0.0.1:31415');
        $test= exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "closegrabA", "id": 0}\' -H \'Accept:\' 127.0.0.1:31415');
        $test= exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "swap", "id": 0}\' -H \'Accept:\' 127.0.0.1:31415');
        
        
    }
    

    


$return_url = (isset($_POST['return_url']))?urldecode($_POST['return_url']):''; //return url
header('Location:'.$return_url);                                                                               
 
?>