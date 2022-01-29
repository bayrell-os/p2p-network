<?php

$msg = "Тест";
$s1 = base64_encode($msg);
$s2 = base64_decode($s1);

echo $s1 . "\n";
echo $s2 . "\n";