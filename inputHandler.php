<!DOCTYPE html>
<html>
<body>


<?php
$temp_icsFile = fopen("tempData.txt","w")
foreach ($i=0;$i<7;$i++){
    fwrite($temp_icsFile,$_GET)
}

?>


</body>
</html>