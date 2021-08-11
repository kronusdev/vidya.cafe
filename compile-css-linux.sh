#!/bin/sh
sass ./files/assets/style/dark.scss ./files/assets/style/dark_47a3ff.css
echo "Finished dark\n"
sass ./files/assets/style/midnight.scss ./files/assets/style/midnight_47a3ff.css
echo "Finished midnight\n"
sass ./files/assets/style/light.scss ./files/assets/style/light_47a3ff.css
echo "Finished light\n"
sass ./files/assets/style/coffee.scss ./files/assets/style/coffee_47a3ff.css
echo "Finished coffe\n"
sass ./files/assets/style/tron.scss ./files/assets/style/tron_47a3ff.css
echo "Finished tron\n"
sass ./files/assets/style/4chan.scss ./files/assets/style/4chan_47a3ff.css
echo "Finished 4chan\n"
python3 ./compilecss.py
rm ./files/assets/style/*[.]map
