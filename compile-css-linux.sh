#!/bin/sh
sass ./files/assets/style/main2.scss ./files/assets/style/main.css
echo "Finished compilation"

rm ./files/assets/style/*[.]map
