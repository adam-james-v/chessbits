import cadquery as cq
import StringIO
import matplotlib.colors as colors

def show_object(result, name='web_view/assembly'):
    # WHAT ARE YOU DOING?
    # TODO: Come up with a better way to multi process things. This import is no good.
    from cadquery import exporters
    'generate a .JSON file for ThreeJS objects.'
    # Open stream
    output = StringIO.StringIO()

    # cadquery will stream a ThreeJS JSON (using old v3 schema, which is deprecated)
    exporters.exportShape(result, 'TJS', output)

    # store stream to a variable
    contents = output.getvalue()

    # Close stream
    output.close()

    # Overwrite the JSON color.
    col = [0.7412, 0.5765, 0.9765]
    old_col_str = '"colorDiffuse" : [0.6400000190734865, 0.10179081114814892, 0.126246120426746]'
    new_col_str = '"colorDiffuse" : ' + str(col)
    new_contents = contents.replace(old_col_str, new_col_str)


    file_name = name + '.json'
    # Save the string to a json file
    with open(file_name, "w") as text_file:
        text_file.write(new_contents)
    return