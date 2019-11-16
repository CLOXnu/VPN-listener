<?php
header("content-type:text/html;charset=utf-8");

$to = $argv[1];
$subject = $argv[2];
$txt = $argv[3];
$headers = "";

$res = mail($to,$subject,$txt,$headers);
var_dump($res);
?>
