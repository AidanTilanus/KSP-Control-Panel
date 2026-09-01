from gpiozero import Button, LED

stage_button = None
stage_led = None

safety_switch = None

def setup_controls():
    global stage_button, stage_led, safety_switch
    
    #stage_button = Button(23, bounce_time=0.025)
    #stage_led = LED(24)

    #safety_switch = Button(25)
    
    #SECTION - Setup simple actions
    
    #safety_switch.when_pressed  = stage_led.on
    #safety_switch.when_released = stage_led.off

def setup_actions(stage):
    #stage_button.when_pressed = stage
    pass
