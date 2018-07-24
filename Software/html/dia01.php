<?php
session_start();
header("Content-type: image/png");
$imgWidth = '200';
$imgHeight = '100';
$theImage = imagecreate($imgWidth, $imgHeight);
$colorGrey = imagecolorallocate($theImage, 241, 241, 241);
$colorBlue = imagecolorallocate($theImage, 0, 50, 255);
$colorRed = imagecolorallocate($theImage, 255, 50,0);


//Control
$countBalken = count($_SESSION["$diagram_mot"]);
//for($i=0;$i<$countBalken;$i++){
//if($maxHeight < $_SESSION["$diagram_mot"][$i][1]*1000-3400){
$maxHeight = 4200-3400;

//

//}



for($i=1;$i<$countBalken;$i++){
if($maxWidth < $_SESSION["$diagram_mot"][$i][0]){
$maxWidth = $_SESSION["$diagram_mot"][$i][0];
}}
$minWidth=$maxWidth-1;
for($i=1;$i<$countBalken;$i++){



if($minWidth > $_SESSION["$diagram_mot"][$i][0]){
$minWidth = $_SESSION["$diagram_mot"][$i][0];
}

}
//}
$dynWidth = round(($imgWidth-2) / ($maxWidth-$minWidth), 0);
@$dynHeight = ($imgHeight-1) / $maxHeight;
for ($i=2; $i<$countBalken; $i++)
{

    $aktNewSize = @round($dynHeight * ($_SESSION["$diagram_mot"][$i-1][1]*1000-3400));
    $aktNewSize2 = @round($dynHeight * ($_SESSION["$diagram_mot"][$i][1]*1000-3400));
    $aktNewSize3 = @round($dynHeight * ($_SESSION["$diagram_mot"][$i-1][2]*1000-3400));
    $aktNewSize4 = @round($dynHeight * ($_SESSION["$diagram_mot"][$i][2]*1000-3400));
    
   


    if($i < $countBalken)
    {
        imageline($theImage, ($_SESSION["$diagram_mot"][$i-1][0]-$minWidth)*$dynWidth, ($imgHeight-$aktNewSize),
        ($_SESSION["$diagram_mot"][$i][0]-$minWidth)*$dynWidth, ($imgHeight-$aktNewSize2), $colorBlue);
        
        imageline($theImage, ($_SESSION["$diagram_con"][$i-1][0]-$minWidth)*$dynWidth, ($imgHeight-$aktNewSize3),
        ($_SESSION["$diagram_con"][$i][0]-$minWidth)*$dynWidth, ($imgHeight-$aktNewSize4), $colorRed);
        
        
    }
    
}


imagestring($theImage,2,90,6,urldecode($dynWidth),$colorBlue);
imagestring($theImage,2,170,6,urldecode("4.2 V"),$colorBlue);
imagestring($theImage,2,170,70,urldecode("3.4 V"),$colorBlue);

imagestring($theImage,2,160,85,urldecode($maxWidth." min"),$colorBlue);

imagepng($theImage);
imagedestroy($theImage);
?>