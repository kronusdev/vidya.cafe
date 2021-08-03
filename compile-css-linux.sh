#!/bin/sh
sass ./drama/assets/style/dark.scss ./drama/assets/style/dark_ff66ac.css
echo "Finished dark\n"
sass ./drama/assets/style/midnight.scss ./drama/assets/style/midnight_ff66ac.css
echo "Finished midnight\n"
sass ./drama/assets/style/light.scss ./drama/assets/style/light_ff66ac.css
echo "Finished light\n"
sass ./drama/assets/style/coffee.scss ./drama/assets/style/coffee_ff66ac.css
echo "Finished coffe\n"
sass ./drama/assets/style/tron.scss ./drama/assets/style/tron_ff66ac.css
echo "Finished tron\n"
sass ./drama/assets/style/4chan.scss ./drama/assets/style/4chan_ff66ac.css
echo "Finished 4chan\n"
python3 ./compilecss.py
