import board
import time
import neopixel
import number

# Main program logic follows:
if __name__ == '__main__':


    frames_per_second = 60
    ms_per_frame = float(1000) / float(frames_per_second)

    print(f"Milliseconds per frame {ms_per_frame:.3f}")
    
#    one = number.FadeNumber(38, 35, color=(255,0,0), bright_step=0.01, max_brightness=0.65, min_brightness=0.05)
    one = number.ChaseNumber(38, 35, color=(0,255,0), brightness=0.15)
    one.clear()

    try:
        while True:
            start = time.monotonic()
            one.show()
            one.step()
            step_time = time.monotonic() - start
            if(step_time < ms_per_frame):
                #
                # Wait for the start of the next frame
                sleep_time = ms_per_frame - step_time
                time.sleep(sleep_time/1000.0)
            else:
                print(f"Step time was {step_time:.3f}ms")
    except KeyboardInterrupt:
        one.clear()
