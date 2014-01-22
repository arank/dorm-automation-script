			<html>			
				<head>
					<title>Open room Protocol</title>
					<link type="text/css" rel="stylesheet" href="bootstrap/css/bootstrap.css"/>
					<meta name="viewport" content="width=device-width, user-scalable=false;">
					<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.4/jquery.min.js" type="text/javascript"></script>
					<script src="chosen.jquery.js" type="text/javascript"></script>
				</head>
				<body>
				<div class="row-responsive">
					<p>The control function for Aran's Room</p>	
					<form action="roomupdate.php" method="post" class="well form-search">
					<br>Songs<br>
						<select name='song' class="chosen-select">
							<option value=''></option>
							<?php
								//Variables for connecting to your database.
								//These variable values come from your hosting account.
								$hostname = "************";
								$username = "**********";
								$dbname = "*************";

								//These variable values need to be changed by you before deploying
								$password = "**********";
							
								//Connecting to your database
								mysql_connect($hostname, $username, $password) OR DIE ("Unable to 
								connect to database! Please try again later.");
								mysql_select_db($dbname);
								
								$query = "SELECT * FROM musiclibrary";
								$result = mysql_query($query);
								while($row = mysql_fetch_assoc($result)){
									echo("<option value=\"");
									echo addslashes($row["song"]);
									echo("\">");
									echo $row["song"];
									echo("</option>");
								}
								mysql_close();	
							?>	
						</select><br>
						Playlists<br>
						<select name='playlist' class="chosen-select">
							<option value=''></option>
							<?php
								//Variables for connecting to your database.
								//These variable values come from your hosting account.
								$hostname = "************";
								$username = "***********";
								$dbname = "***********";

								//These variable values need to be changed by you before deploying
								$password = "***************";
							
								//Connecting to your database
								mysql_connect($hostname, $username, $password) OR DIE ("Unable to 
								connect to database! Please try again later.");
								mysql_select_db($dbname);
								
								$query = "SELECT * FROM playlists";
								$result = mysql_query($query);
								while($row = mysql_fetch_assoc($result)){
									echo("<option value=\"");
									echo addslashes($row["list"]);
									echo("\">");
									echo $row["list"];
									echo("</option>");
								}
								mysql_close();	
							?>	
						</select><br>
						<input type="radio" name="control" value="pause">Pause<br>
						<input type="radio" name="control" value="play">Play<br>
						<input type="radio" name="control" value="next">Next<br>
						<input type="radio" name="control" value="stop">Stop<br>
						</input>
						<br>
						<br>
						<input type="submit">
						<br>
						These are the light Controls<br>
						<input type="radio" name="switch" value="on">On<br>
						<input type="radio" name="switch" value="off">Off<br>
						</input>
						Hue:<input type="text" name="hue"><br>
						Brightness:<input type="text" name="bri"><br>
						<br>
						<br>
						<br>
						These are the Voice Controls<br>
						Say something:<input type="text" name="voice"><br>
					</form>
				</div>
				<?php
					//Variables for connecting to your database.
					//These variable values come from your hosting account.
					$hostname = "*****************";
					$username = "************";
					$dbname = "***********";

					//These variable values need to be changed by you before deploying
					$password = "*************";
				
					//Connecting to your database
					mysql_connect($hostname, $username, $password) OR DIE ("Unable to 
					connect to database! Please try again later.");
					mysql_select_db($dbname);
					
					$query = "SELECT * FROM paststates ORDER BY time DESC LIMIT 0, 1";
					$result = mysql_query($query);
					while($row = mysql_fetch_assoc($result)){
						if ($row["song"]){
							echo $row["song"];
							echo("<br>");
							if ($row["action"]==0){
								echo ("paused");
							}else{
								echo ("playing");
							}
							echo("<br>");
						}
						if ($row["playlist"]){
							echo $row["playlist"];
							echo("<br>");
						}
						if ($row["lightstate1"]==0){
							echo ("lights off");
							echo("<br>");
						}
						else
						{
							echo ("lights on");
							echo("<br>");
							echo $row["lighthue1"];
							echo("<br>");
							echo $row["lightbri1"];
							echo("<br>");
						}
					}
					mysql_close();	
				?>	
			</body>
			<script type="text/javascript">
						$(".chosen-select").chosen();
			</script>
		</html>