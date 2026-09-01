def stage(control, safety_switch):
    if safety_switch.is_pressed:
        control.activate_next_stage()
