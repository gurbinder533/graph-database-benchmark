nohup ./run_synthea  -c synthea.config -s 23456  -p 2000000 "New Jersey" > 1TB_NJ.log &
nohup ./run_synthea  -c synthea.config -s 23456  -p 2000000 "New York" > 1TB_NY.log &
nohup ./run_synthea  -c synthea.config -s 23456  -p 2000000 "Florida" > 1TB_FL.log &
nohup ./run_synthea  -c synthea.config -s 23456  -p 3000000 "California" > 1TB_CA.log &
