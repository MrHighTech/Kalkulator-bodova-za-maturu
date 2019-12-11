<?php
	$conn = mysqli_connect("localhost", "root","");
	$sql = "CREATE DATABASE	kalkulator";
	mysqli_query($conn, $sql);	
	
	mysqli_select_db($conn, "kalkulator");
	$sql = "CREATE TABLE Uvjeti (
	id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
	Fakultet NVARCHAR(150) NOT NULL,
	Smjer NVARCHAR(150) NOT NULL,
	Matematika_razina VARCHAR(1) NOT NULL,
	Hrvatski_razina VARCHAR(1) NOT NULL,
	Engleski_razina VARCHAR(1) NOT NULL,
	Matematika_vrednovanje VARCHAR(15) NOT NULL,
	Hrvatski_vrednovanje VARCHAR(15) NOT NULL,
	Engleski_vrednovanje VARCHAR(15) NOT NULL,
	Vrednovanje_prosjek VARCHAR(15) NOT NULL)";
	mysqli_query($conn, $sql);
	header('Content-Type: text/html; charset=utf-8');
	mysqli_set_charset($conn, "utf8");

	$prvi = $_REQUEST["prvi"];
	$drugi = $_REQUEST["drugi"];
	$treci = $_REQUEST["treci"];
	$cetvrti = $_REQUEST["cetvrti"];

	$hrvatski = $_REQUEST["hrvatski"];
	$matematika = $_REQUEST["matematika"];
	$engleski = $_REQUEST["engleski"];


	if (strpos($prvi, ',')) {
		$prvi = str_replace(',', '.', $prvi);
	};
	if (strpos($drugi, ',')) {
		$drugi = str_replace(',', '.', $drugi);
	}
	if (strpos($treci, ',')) {
		$treci = str_replace(',', '.', $treci);
	}
	if (strpos($cetvrti, ',')) {
		$cetvrti = str_replace(',', '.', $cetvrti);
	}
	
	$prosjek = (floatval($prvi) + floatval($drugi) + floatval($treci) + floatval($cetvrti)) / 20;
	$sql = "SELECT * FROM Uvjeti";
	$result = mysqli_query($conn, $sql);
	$smjer = '';
	
	if (mysqli_num_rows($result) > 0) {
		$fakultet = $_REQUEST['fakulteti'];  // Storing Selected Value In Variable
		$smjer = $_REQUEST['smjerovi'];
		// output data of each row
		while($row = mysqli_fetch_assoc($result)) {
			$result1 = strcmp(strtolower($row['Fakultet']), strtolower($fakultet));
			$result2 = strcmp(strtolower($row['Smjer']), strtolower($smjer));
			if ($result1 == 1 && $result2 == 0) {
				$fak = $row['Fakultet'];  // Storing Selected Value In Variable
				$smj = $row['Smjer'];
				$matraz = $row['Matematika_razina'];
				$hrvraz = $row['Hrvatski_razina'];
				$engraz = $row['Engleski_razina'];
				$matvr = $row['Matematika_vrednovanje'];
				$hrvvr = $row['Hrvatski_vrednovanje'];
				$engvr = $row['Engleski_vrednovanje'];
				$vr_prosjek = substr($row['Vrednovanje_prosjek'], 0, 2);
			}			
		}
	}

	if (strlen($smjer)<5) {
		echo("Nisi odredio smjer");
	} else if ($prvi == "" || $drugi == "" || $treci == "" || $cetvrti == "") {
		echo ("Nisi unio sve prosjeke");
	} else if ($hrvatski == "" || $matematika == "" || $engleski == "") {
		echo("Nisi unio sve rezultate državne mature");
	} else if (floatval($prvi) > 5 || floatval($prvi) < 2 || floatval($drugi) > 5 || floatval($drugi) < 2 || floatval($treci) > 5 || floatval($treci) < 2 || floatval($cetvrti) > 5 || floatval($cetvrti) < 2) {
		echo ("Za prosjeke moraš unijeti brojeve između 2 i 5");
	} else if (floatval($hrvatski) > 100 || floatval($hrvatski) < 0 || floatval($matematika) > 100 || floatval($matematika) < 0 || floatval($engleski) > 100 || floatval($engleski) < 0) {
		echo("Rezultati državne mature moraju biti između 0 i 100");
	} else {
		echo((floatval($prosjek) * floatval($vr_prosjek) * 10) + (floatval($matvr) * floatval($matematika)) / 10 + (floatval($hrvvr) * floatval($hrvatski)) / 10 + (floatval($engvr) * floatval($engleski)) / 10);  
	}
	
	mysqli_close($conn);
	
?>