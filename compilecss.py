def color_variant(hex_color, brightness_offset=1):
    """ takes a color like #87c95f and produces a lighter or darker variant """  
    if len(hex_color) != 6:  
        raise Exception("Passed %s into color_variant(), needs to be in 87c95f format." % hex_color)
    rgb_hex = [hex_color[x:x+2] for x in [0, 2, 4]]
    new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
    new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 255  
    # hex() produces "0x88", we want just "88"  
    return "".join([hex(i)[2:] for i in new_rgb_int])

for theme in ['midnight', 'dark', 'light', 'coffee', 'tron', '4chan']:
    with open(f"./files/assets/style/{theme}_47a3ff.css", encoding='utf-8') as t:
        text = t.read()
        for color in ['47a3ff','805ad5','62ca56','38a169','80ffff','2a96f3','62ca56','eb4963','ff0000','f39731','adf1d2','3e98a7','e4432d','7b9ae4','ec72de','7f8fa6', 'f8db58']:
            newtext = text.replace("47a3ff", color).replace("1f84d7", color_variant(color, -40))
            with open(f"./files/assets/style/{theme}_{color}.css", encoding='utf-8', mode='w') as nt:
                nt.write(newtext)

