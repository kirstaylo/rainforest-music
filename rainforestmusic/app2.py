"""
App
"""
from window import Window

# build the window
Amazone = Window("The Amazone", "1280x800", "#506b52")
# add the title
Amazone.build_title("Welcome to the Amazone", 'Candara', 25, "#eeeeee", 2)
# add the video section
Amazone.build_video("scenes/scene1.jpg", (800,600))
# add the controls section
Amazone.build_controls(0.7, "Sample", 'Candara', 10, 2)
# add a sound
# Amazone.add_sound("woods_spirit", 'Candara', 10, 2)

Amazone.run()