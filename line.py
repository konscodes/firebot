'''Line messenger app module.
- connect to Line API
- handle Join events
    - prompt for pass code
    - call fire db for pass code check
    - call fire db to associate group id with the pass code if matched
- send a push message'''

class Line:
    def __init__(self) -> None:
        print('[Line] Connecting to Line')
        print('[Line] Adding Join handler')
        print('[Line] Adding message handler')
    
    def send_push(self):
        print('[Line] Sending push')

