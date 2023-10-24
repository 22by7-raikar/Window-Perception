"""
main.py
    Simulates the UAV dynamics, cameras and visualizes output
    This entrypoint file runs within Blender's python interpreter

    How to setup Blender and Blender python interpreter?
        Install Blender (this code was tested on version 3.6)

        Ubuntu is officially supported. In case you are using Windows or Mac, these instructions may or may not work
              
        1. Find the python interpreter location associated with the Blender:
            a. Open Blender interactive console within Blender
            b. import sys
            c. print(sys.executable) 
        2. Use pip to install the dependencies from command prompt/terminal (I dont think it worked with powershell though). It will throw a warning and install to something called user site
            "python path" -m pip install imath numpy opencv-python scipy pyquaternion
            For example,
            Windows command looks like this,
                "C:\Program Files\Blender Foundation\Blender 3.6\3.6\python\bin\python.exe" -m pip install opencv-python ...
            Linux command looks like this in my setup,
                /usr/bin/python3.10 -m pip install opencv-python ...
        3. Reopen blender

    How to run the script?
        Create a folder called outputs and open main.blend file
        Goto scripting tab, associate it with main.py if not done already
        Run the script. It takes about 10 seconds to execute
        Goto animation tab and press space to see the visualization
    
    Based on Prof. Nitin's work https://umdausfire.github.io/teaching/fire298/asn3.html
"""

import bpy
import sys
import site

# PATH CONFIGURATION
user_site_packages = "/home/ankush/proj0/myenv/lib/python3.10/site-packages/"
sys.path.append(user_site_packages) #For pip installed dependencies
sys.path.append('./src')

# IMPORT PIP LIBS
import importlib
import math
import os
import random
import numpy as np
import cv2
import scipy
#import OpenEXR
    
# IMPORT DYNAMICS, CONTROL and USER CODE
import quad_dynamics as qd
import control
import tello
import frame_utils as frame
import rendering
import usercode
import yaml
from environment import create_block, create_boundary, create_window, clear_scene #, setup_window_material

# Force reload custom modules and run the latest code
importlib.reload(control)
importlib.reload(qd)
importlib.reload(tello)
importlib.reload(frame)
importlib.reload(rendering)
importlib.reload(usercode)

clear_scene()
robot_width = 0.3
robot_length = 0.3
robot_height = 0.5
bloat_width = robot_width/2
bloat_length = robot_length/2
bloat_height = robot_height/2

def main():
    # Replace the path below with the correct absolute path to cfg.yaml
    cfg_path = '/home/ankush/Desktop/abhardwaj_p3a/src/configs/cfg.yaml'
    
    try:
        if os.path.exists(cfg_path):
            with open(cfg_path, 'r') as file:
                cfg = yaml.safe_load(file)
            # Now you can work with the 'cfg' variable, which contains the parsed YAML data.
            print(cfg)
        else:
            print(f"The file '{cfg_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    clear_scene()

    env_path = cfg['env']['main_path']
    map_file = cfg['env']['map_file']
    env_file = os.path.expanduser(os.path.join(env_path, map_file))

    with open(env_file, 'r') as file:
        lines = file.readlines()

        for line in lines:
            line_parts = line.strip().split()
                # Load the texture for the window

            texture_location = cfg["textures"]["main_path"]
            texture_file = cfg["textures"]["pic"]
            texture_path = os.path.expanduser(os.path.join(texture_location, texture_file))

            # Create the window material with the texture
            # window_material = setup_window_material(texture_path)

            if len(line_parts) > 0:
            
                if line_parts[0] == "block" and len(line_parts) == 10:
                    xmin, ymin, zmin, xmax, ymax, zmax, r, g, b = map(float, line_parts[1:])
                    create_block(xmin, ymin, zmin, xmax, ymax, zmax, r, g, b)

                elif line_parts[0] == "boundary" and len(line_parts) == 7:
                    bxmin, bymin, bzmin, bxmax, bymax, bzmax = map(float, line_parts[1:])
                    transparency = 0.344  # Set the desired transparency value
                    create_boundary(bxmin, bymin, bzmin, bxmax, bymax, bzmax, transparency)
                 
                elif line_parts[0] == "window":
                    x, y, z, xdelta, ydelta, zdelta, qw, qx, qy, qz, xangdelta, yangdelta, zangdelta = map(float, line_parts[1:])
                    create_window(x, y, z, xdelta, ydelta, zdelta, qw, qx, qy, qz, xangdelta, yangdelta, zangdelta, texture_path) 
    
    # CONSTANTS
    fps = 20

    # STOP time for simulation
    sim_stop_time = 200

    # INIT RENDERING AND CONTROL
    controller = control.quad_control()
    user_sm = usercode.state_machine()
    rendering.init() 
    bpy.context.scene.render.fps = fps
    bpy.context.scene.frame_end = fps*sim_stop_time

    # SET TIME STEP
    dynamics_dt = 0.01
    control_dt = controller.dt
    user_dt = user_sm.dt
    frame_dt = 1./fps

    # INIT STATES
#    current_time = 0.
#    xyz = np.array([0, 0, 0]) 
#    vxyz = np.array([0.0, 0.0, 0.0])
#    quat = np.array([1.0, .0, .0, .0])
#    pqr = np.array([0.0, .0, .0])
#    current_ned_state = np.concatenate((xyz, vxyz, quat, pqr))    
#    
#    # INIT TIMER
#    dynamics_countdown = 0.
#    control_countdown = 0.
#    frame_countdown = 0.
#    user_countdown = 0.
#    
#    # INIT LOG
#    stateArray = current_ned_state
#    timeArray = 0
#    controlArray = np.array([0., 0, 0, 0])

#    # SCHEDULER SUPER LOOP
#    # --------------------------------------------------------------------------------------------
#    while current_time < sim_stop_time:
#        if frame_countdown<=0.:
#            rendering.stepBlender(current_ned_state)
#            frame_countdown = frame_dt

#        if user_countdown<=0.:
#            xyz_ned = current_ned_state[0:3]
#            xyz_blender = [xyz_ned[0], -xyz_ned[1], -xyz_ned[2]]

#            vxyz_ned = current_ned_state[3:6]
#            vxyz_blender = [vxyz_ned[0], -vxyz_ned[1], -vxyz_ned[2]]

#            xyz_bl_des, vel_bl_des, acc_bl_des, yaw_bl_setpoint = user_sm.step(current_time, xyz_blender, vxyz_blender)

#            yaw_ned = -yaw_bl_setpoint
#            WP_ned = np.array([xyz_bl_des[0], -xyz_bl_des[1], -xyz_bl_des[2], yaw_ned])
#            vel_ned = np.array([vel_bl_des[0], -vel_bl_des[1], -vel_bl_des[2]])
#            acc_ned = np.array([acc_bl_des[0], -acc_bl_des[1], -acc_bl_des[2]])
#            

#            user_countdown = user_dt

#        if control_countdown<=0.:
#            U = controller.step(current_ned_state, WP_ned, vel_ned, acc_ned)
#            control_countdown = control_dt

#        # Dynamics runs at base rate. 
#        #   TODO replace it with ODE4 fixed step solver
#        current_ned_state = current_ned_state + dynamics_dt*qd.model_derivative(current_time,
#                                                            current_ned_state,
#                                                            U,
#                                                            tello)
#        
#        # UPDATE COUNTDOWNS AND CURRENT TIME
#        dynamics_countdown -= dynamics_dt
#        control_countdown -= dynamics_dt
#        frame_countdown -= dynamics_dt
#        user_countdown -=dynamics_dt
#        current_time += dynamics_dt

#        # LOGGING
#        stateArray = np.vstack((stateArray, current_ned_state))
#        controlArray = np.vstack((controlArray, U))
#        timeArray = np.append(timeArray, current_time)
#    # ----------------------------------------------------------------------------------------------
#    user_sm.terminate()

#    # SAVE LOGGED SIGNALS TO MAT FILE FOR POST PROCESSING IN MATLAB
#    loggedDict = {'time': timeArray,
#                  'state': stateArray,
#                  'control': controlArray}  
#                  
#    scipy.io.savemat('~/Desktop/abhardwaj_p3a/log/states.mat', loggedDict)
    
if __name__=="__main__":
    main()
    
    
    
     