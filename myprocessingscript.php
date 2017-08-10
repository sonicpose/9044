<html>
    
    <head>
        <link rel="stylesheet" href="9044.css">
    </head>
    
    <body>
        
        <h1>9044 YouTube Downloader</h1>
        
        <div>
            <img src="DownloadGIF.gif">
        </div>
        
        <?php
        if(isset($_POST['field1'])) {
            $data = $_POST['field1'] . "\n" ;
            $ret = file_put_contents('C:/xampp/htdocs/data.txt', $data, FILE_APPEND | LOCK_EX);
            if($ret === false) {
                die('An error occured when receiving the URL. Please try again');
            }
            else {
                echo "URL Received! Starting download...";
            }
        }
            else {
                die('no post data to process');
            }
        ?>
 
    </body>

</html>