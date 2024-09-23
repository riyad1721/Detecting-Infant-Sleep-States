import streamlit as st
import cv2
from video_processing import process_video

# Streamlit main function
def main():
    # st.title("Using Facial Recognition for Detecting Infant Sleep States")
    # Title with custom color
    with st.container():
        st.markdown("<h3 style='text-align: center; color: #4B0082;'>Using Facial Recognition for Detecting Infant Sleep States</h3>",
                    unsafe_allow_html=True)

    # Main section layout
    with st.container():
        st.markdown("<h4 style='text-align: left; color: #008080;'> Video Upload and Playback </h4>",
                    unsafe_allow_html=True)

        # col1, col2 = st.columns(2)

        # with col1:
        #     uploaded_file = st.file_uploader("Upload a video file (MP4 or AVI)", type=["mp4", "avi"])

        # with col2:
        # Sidebar for video upload
        st.sidebar.markdown("<h2 style='color: #008080;'>Upload a Video File</h2>", unsafe_allow_html=True)
        # uploaded_file = st.sidebar.file_uploader("Choose a video...", type=["mp4", "avi"])
        # Styling the upload section
        # Styling the upload section
        st.sidebar.markdown("""
            <div style='background-color: #E8F0FE; padding: 10px; border-radius: 5px;'>
                <h4 style='color: #4B0082;'>Choose a video file</h4>
            </div>
        """, unsafe_allow_html=True)

        # Upload file button
        uploaded_file = st.sidebar.file_uploader("Upload your video here...", type=["mp4", "avi"])


        # Play button for the video
        # play_button = st.sidebar.button("Play Video")
        if uploaded_file is not None:
            # Save the uploaded video temporarily
            with open("temp_video.mp4", "wb") as f:
                f.write(uploaded_file.read())

            # Display processing message
            st.write("Processing the video, please wait...")

            # Create a placeholder for the video display
            video_placeholder = st.empty()
            status_placeholder = st.empty()
            probability_placeholder = st.empty()

            # Process the video and display frames
            for frame, status, probability in process_video("temp_video.mp4"):
                video_placeholder.image(frame, channels="RGB", use_column_width=True)
                # status_placeholder.write(f"Detection Status: {status}")
                # Custom status display with different colors for label and status on the same line
                if probability > 80 :
                    status_placeholder.markdown(f"<span style='color: #FFA500; font-size: 25px; font-weight: bold;'>Detection Status: </span> "
                                                f"<span style='color: #000000; font-size: 20px; font-weight: bold;'>{status}</span>",
                                                unsafe_allow_html=True)
                    probability_placeholder.markdown(f"<span style='color: #FFA500; font-size: 25px; font-weight: bold;'>Prediction Probability: </span> "
                                                f"<span style='color: #000000; font-size: 20px; font-weight: bold;'>{probability}</span>",
                                                unsafe_allow_html=True)
if __name__ == "__main__":
    main()
