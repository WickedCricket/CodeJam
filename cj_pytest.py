import sys
import time

def loading_screen():
        tool_name = "This is a test"
        animation = "|/-\\"

        for i in range(20):
            time.sleep(0.1)
            sys.stdout.write("\r" + tool_name + ": " + animation[i % len(animation)])
            sys.stdout.flush()
            
        print("\nTest completed!!")
