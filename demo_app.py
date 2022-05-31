from enum import auto
import streamlit as st
from demo import run_inference, draw_debug, draw_debug_image
import copy
import time
import argparse
import os
from PIL import Image
import cv2 as cv
import numpy as np
import tensorflow as tf
import tempfile
from streamlit_image_comparison import image_comparison

def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

if __name__ == '__main__':


    genre = st.radio(
     "Choose input:",
     ('image', 'video')
    )

    if genre == 'image':
        st.write('You selected image.')

        # Select a file
        img_file_buffer = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

        if img_file_buffer is not None:
            image = np.array(Image.open(img_file_buffer))



            input_size = (192,640)

            model_path = './saved_model_lite_hr_depth_k_t_encoder_depth_192x640/model_float16_quant.tflite'
            interpreter = tf.lite.Interpreter(model_path=model_path)
            interpreter.allocate_tensors()

            depth_map = run_inference(
                        interpreter,
                        input_size,
                        image)

            image1, image2 = draw_debug_image(image, depth_map)

            col1, col2 =st.columns(2)

            with col1:
                st.image(image1, use_column_width=True, output_format='auto')
            with col2:
                st.image(image2, use_column_width=True, output_format='auto')

            # render image-comparison
            image_comparison(
                img1=image1,
                img2=image2,
            )
    else:
        # Select a file
        vid = st.file_uploader("Upload a video", type=["avi", "mp4"])
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        # tfile.write(vid.read())

        vf = cv.VideoCapture(tfile.name)
        stframe = st.empty()

        if vid is not None:

            input_size = (192,640)

            model_path = './saved_model_lite_hr_depth_k_t_encoder_depth_192x640/model_float16_quant.tflite'
            interpreter = tf.lite.Interpreter(model_path=model_path)
            interpreter.allocate_tensors()

            stframe = st.empty()

            while vf.isOpened():
                ret, frame = vf.read()
                start_time = time.time()

                if not ret:
                    break
                debug_image = copy.deepcopy(frame)

                # Inference execution
                depth_map = run_inference(
                    interpreter,
                    input_size,
                    frame,
                )

                elapsed_time = time.time() - start_time

                # Draw
                debug_image, depth_image = draw_debug(
                    debug_image,
                    elapsed_time,
                    depth_map,
                )

                col1, col2 =st.columns(2)

                with col1:
                    st.image(debug_image, use_column_width=True, output_format='auto')
                with col2:
                    st.image(depth_image, use_column_width=True, output_format='auto')

                # render image-comparison
                image_comparison(
                    img1=debug_image,
                    img2=depth_image,
                )


        st.write("You selected video.")



    