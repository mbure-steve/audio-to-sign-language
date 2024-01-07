# import pygame
# from moviepy.editor import VideoFileClip


def pygame_video(pygame,VideoFileClip,list_videos):
    # Initialize Pygame
    pygame.init()

    # Set the width and height of the screen (video resolution)
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Video Player")

    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()
    resources = "resources"
    # List of video filenames
    video_files = [f"{resources}/{i}"for i in list_videos]
    current_video_index = 0

    # Function to load and play the next video
   

    # Main loop
    running = True
    current_video,current_video_index = play_next_video(current_video_index,video_files,VideoFileClip)
    start_time = pygame.time.get_ticks()

    while running and current_video:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get the elapsed time in milliseconds
        elapsed_time = pygame.time.get_ticks() - start_time

        # Get the current frame from the video based on elapsed time
        frame = current_video.get_frame(elapsed_time / 1000.0)

        # Convert the frame to a Pygame surface
        # pygame_frame = pygame.image.fromstring(frame.tobytes(), (current_video.size[0], current_video.size[1]), 'RGB')
        pygame_frame = pygame.transform.scale(pygame.image.fromstring(frame.tobytes(), current_video.size, 'RGB'),
                                               (width, height))

        # Display the frame on the screen
        screen.blit(pygame_frame, (0, 0))
        pygame.display.flip()

        # Control the frame rate
        clock.tick(30)

        # Check if the video has ended
        if elapsed_time > current_video.duration * 1000:
            current_video,current_video_index = play_next_video(current_video_index,video_files,VideoFileClip)
            start_time = pygame.time.get_ticks()

    # Quit Pygame
    pygame.quit()
def play_next_video(current_video_index,video_files,VideoFileClip):
    if current_video_index < len(video_files):
        video_path = video_files[current_video_index]
        try:
            video_clip = VideoFileClip(video_path)
        except Exception as e:
            pass
        current_video_index += 1
        return video_clip,current_video_index
    else:
        return None,None