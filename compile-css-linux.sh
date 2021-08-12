#!/bin/sh
sass ./files/assets/style/dark.scss ./files/assets/style/dark_47a3ff.css
echo "Finished dark"
sass ./files/assets/style/light.scss ./files/assets/style/light_47a3ff.css
echo "Finished light"
sass ./files/assets/style/blur.scss ./files/assets/style/blur_47a3ff.css
echo "Finished blur"
sass ./files/assets/style/hackernews.scss ./files/assets/style/hackernews_47a3ff.css
echo "Finished HN"
sass ./files/assets/style/coffee.scss ./files/assets/style/coffee_47a3ff.css
echo "Finished coffe"
sass ./files/assets/style/tron.scss ./files/assets/style/tron_47a3ff.css
echo "Finished tron"
sass ./files/assets/style/4chan.scss ./files/assets/style/4chan_47a3ff.css
echo "Finished 4chan"
sass ./files/assets/style/midnight.scss ./files/assets/style/midnight_47a3ff.css
echo "Finished midnight"

python3 ./compilecss.py
rm ./files/assets/style/*[.]map
