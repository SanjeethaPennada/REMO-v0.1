from PIL import Image, ImageDraw, ImageFont

def create_combined_gif(gif1_path, gif2_path, output_path):
    # Open the two GIFs
    gif1 = Image.open(gif1_path)
    gif2 = Image.open(gif2_path)

    # Get the frames for both GIFs
    gif1_frames = []
    gif2_frames = []

    try:
        while True:
            gif1_frames.append(gif1.copy())
            gif1.seek(gif1.tell() + 1)
    except EOFError:
        pass

    try:
        while True:
            gif2_frames.append(gif2.copy())
            gif2.seek(gif2.tell() + 1)
    except EOFError:
        pass

    # Ensure both GIFs have the same number of frames
    max_frames = max(len(gif1_frames), len(gif2_frames))
    while len(gif1_frames) < max_frames:
        gif1_frames.append(gif1_frames[-1])  # Repeat last frame
    while len(gif2_frames) < max_frames:
        gif2_frames.append(gif2_frames[-1])  # Repeat last frame

    # Get sizes of GIFs
    width1, height1 = gif1.size
    width2, height2 = gif2.size

    # Max height to align GIFs properly
    max_height = max(height1, height2)

    # Create a drawing object for adding titles
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()

    # Combine the frames side by side and add titles
    combined_frames = []
    for i in range(max_frames):
        frame1 = gif1_frames[i]
        frame2 = gif2_frames[i]

        # Create a blank image large enough for both GIFs
        combined_image = Image.new('RGBA', (width1 + width2, max_height + 50), (255, 255, 255, 255))

        # Paste both GIFs onto the combined image
        combined_image.paste(frame1, (0, 0))
        combined_image.paste(frame2, (width1, 0))

        # Create a drawing object to add text titles
        draw = ImageDraw.Draw(combined_image)

        # Add titles on top
        draw.text((width1 // 2 - 50, max_height + 10), "Failure Scenario", font=font, fill="black")
        draw.text((width1 + width2 // 2 - 60, max_height + 10), "Modified Scenario", font=font, fill="black")

        combined_frames.append(combined_image)

    # Save the combined frames as a GIF
    combined_frames[0].save(output_path, save_all=True, append_images=combined_frames[1:], loop=0, duration=gif1.info['duration'])

    print(f"Combined GIF saved to {output_path}")

# Example usage
gif1_path = 'failure_scenario.gif'  # Path to the first GIF
gif2_path = 'modified_scenario.gif'  # Path to the second GIF
output_path = 'combined_scenario.gif'  # Path to save the output GIF

create_combined_gif(gif1_path, gif2_path, output_path)

