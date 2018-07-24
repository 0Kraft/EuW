<?php
                
                $jsonlog = exec('curl -s --data-binary \'{"jsonrpc": "2.0", "method": "get_log", "id": 0}\' -H \'Accept:\' 127.0.0.1:8080');
               
                if($jsonlog!="")
                {
                
                        $parse = json_decode($jsonlog, true);
                        
                        
                        
                        for ($i=0; $i<12; $i++)
                        {
                            $color=0;
                            $color=$color+$i*20;
                            echo '<b>-</b> <span style="color:rgb('.$color.','.$color.','.$color.'">'. $parse["result"][$i] .'</span><br>';
                       
                        }
                
                }else{
                    
                    echo 'no connection';
                    
                }
                
                

                ?>