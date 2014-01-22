            <?php
			//Variables for connecting to your database.
			//These variable values come from your hosting account.
			$hostname = "*************";
			$username = "****************";
			$dbname = "**********";

			//These variable values need to be changed by you before deploying
			$password = "*********";
			$usertable = "********";
        
            //Connecting to your database
            mysql_connect($hostname, $username, $password) OR DIE ("Unable to 
            connect to database! Please try again later.");
            mysql_select_db($dbname);
			
			$action = "0";
			if($_POST["control"] == "play"){
				$action="1";
			}
			else if($_POST["control"] == "pause"){
				$action="2";
			}
			else if($_POST["control"] == "next"){
				$action="3";
			}
			else if($_POST["control"] == "stop"){
				$action="4";
			}
			
			$s = $_POST["song"];
			$p = $_POST["playlist"];
			
			$voice = mysql_real_escape_string($_POST["voice"]);
			
			if($_POST["switch"] == "on"){
				$l1state="1";
			}
			else if($_POST["switch"] == "off"){
				$l1state="0";
			}
			else{
				$l1state="-1";
			}
			
			if($_POST["hue"] == ""){
				$l1hue="-1";
			}
			else{
				$l1hue=$_POST["hue"];
			}
			
			if($_POST["bri"] == ""){
				$l1bri="-1";
			}
			else{
				$l1bri=$_POST["bri"];
			}
			
			//Fetching from your database table.
			$query = "INSERT INTO goalstates (song, playlist, action, voice, lightstate1, lighthue1, lightbri1) VALUES ('$s', '$p', '$action', '$voice', '$l1state', '$l1hue', '$l1bri')";
			mysql_query($query);
			
			
			mysql_close();
			
			header( 'Location: SOME LOCATION' ) ;

            ?>
			
			