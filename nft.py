#!/usr/bin/env python
# coding: utf-8

# Import required libraries
from PIL import Image
import pandas as pd
import numpy as np
import time
import os
import random
from progressbar import progressbar
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# Import configuration file
from config import CONFIG


# Parse the configuration file and make sure it's valid
def parse_config():
    
    # Input traits must be placed in the assets folder. Change this value if you want to name it something else.
    assets_path = 'assets'

    # Loop through all layers defined in CONFIG
    for layer in CONFIG:

        # Go into assets/ to look for layer folders
        layer_path = os.path.join(assets_path, layer['directory'])
        
        # Get trait array in sorted order
        traits = sorted([trait for trait in os.listdir(layer_path) if trait[0] != '.'])

        # If layer is not required, add a None to the start of the traits array
        if not layer['required']:
            traits = [None] + traits
        
        # Generate final rarity weights
        if layer['rarity_weights'] is None:
            rarities = [1 for x in traits]
        elif layer['rarity_weights'] == 'random':
            rarities = [random.random() for x in traits]
        elif type(layer['rarity_weights'] == 'list'):
            assert len(traits) == len(layer['rarity_weights']), "Make sure you have the current number of rarity weights"
            rarities = layer['rarity_weights']
        else:
            raise ValueError("Rarity weights is invalid")
        
        rarities = get_weighted_rarities(rarities)
        
        # Re-assign final values to main CONFIG
        layer['rarity_weights'] = rarities
        layer['cum_rarity_weights'] = np.cumsum(rarities)
        layer['traits'] = traits


# Weight rarities and return a numpy array that sums up to 1
def get_weighted_rarities(arr):
    return np.array(arr)/ sum(arr)

# Updated function to handle video layers and add images on top
def combine_video_and_images(video_path, image_paths, output_filename=None):
    # Load the background video (assuming only one video as the background)
    video_clip = VideoFileClip(os.path.join('assets', video_path))

    # Load images and overlay them on the video
    image_clips = []
    for image_path in image_paths:
        img = Image.open(os.path.join('assets', image_path))

        # Convert the PIL image to a MoviePy image clip and set the duration
        img_clip = ImageClip(np.array(img), duration=video_clip.duration)

        # Position the image on the video (modify as needed)
        img_clip = img_clip.set_position(('center', 'center')).resize(video_clip.size, Image.Resampling.LANCZOS)

        image_clips.append(img_clip)

    # Composite the video and image layers
    final_clip = CompositeVideoClip([video_clip] + image_clips)

    # Write the result to a file
    if output_filename:
        final_clip.write_videofile(output_filename, codec='libx264')
    else:
        output_dir = os.path.join('output', 'video_with_images')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        final_clip.write_videofile(os.path.join(output_dir, str(int(time.time())) + '.mp4'), codec='libx264')

# New function to handle video layers
def combine_video_layers(video_paths, output_filename=None):
    clips = [VideoFileClip(os.path.join('assets', path)) for path in video_paths if path.endswith('.mp4')]
    
    # Combine video clips into one
    final_clip = CompositeVideoClip(clips)
    
    if output_filename:
        final_clip.write_videofile(output_filename, codec='libx264')
    else:
        output_dir = os.path.join('output', 'single_videos')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        final_clip.write_videofile(os.path.join(output_dir, str(int(time.time())) + '.mp4'), codec='libx264')

# Updated function to handle both images and video layers
def generate_single_media(filepaths, output_filename=None):
    # Separate image and video layers
    image_paths = [path for path in filepaths if path.endswith('.png')]
    video_paths = [path for path in filepaths if path.endswith('.mp4')]

    # Handle video layers first (as background)
    if video_paths:
        video_bg = VideoFileClip(os.path.join('assets', video_paths[0]))
        final_clip = video_bg  # This will be the base for compositing

        # Handle image layers on top of the video background
        if image_paths:
            for image_path in image_paths:
                img = Image.open(os.path.join('assets', image_path))
                # Convert PIL image to a MoviePy image clip
                img_clip = ImageClip(np.array(img)).set_duration(video_bg.duration)
                final_clip = CompositeVideoClip([final_clip, img_clip])

        # Save the combined video
        if output_filename and output_filename.endswith('.mp4'):
            final_clip.write_videofile(output_filename, codec='libx264')
        else:
            output_dir = os.path.join('output', 'single_videos')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            final_clip.write_videofile(os.path.join(output_dir, str(int(time.time())) + '.mp4'), codec='libx264')

    # If no video, handle image layers alone
    elif image_paths:
        bg = Image.open(os.path.join('assets', image_paths[0]))
        for filepath in image_paths[1:]:
            img = Image.open(os.path.join('assets', filepath))
            bg.paste(img, (0, 0), img)

        # Save the image as .png
        if output_filename and output_filename.endswith('.png'):
            bg.save(output_filename)
        else:
            output_dir = os.path.join('output', 'single_images')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            bg.save(os.path.join(output_dir, str(int(time.time())) + '.png'))


# Generate a single image with all possible traits
# generate_single_image(['Background/Background 01 White Memgen Ryu.png, Background 02 Red Race On Base Diecaster.png, Background 03 Pink Landwolf.png, Background 04 Purple Touch Grass.png, Background 05 Based Blue Memgen.png, Background 06 Sunny Field.png, Background 07 Snowy.png, Background 08 Green $AYB.png, Background 09 Neon Jeetolax.png, Background 10 Sunset.png, Background 11 Trippy.png, Background 12 Moon.png, Background 13 Desert.png, Background 14 Animated Jeetolax Desert.mp4, Background 15 Animated Building On Base Sunny Field.mp4, Background 16 Animated Wear The $WAG Sunny Field.mp4, Background 17 Animated Memgen Sunset.mp4, Background 18 Animated Million Bit Home Page Sunset.mp4, Background 19 Animated All Your Base Sunset.mp4, Background 20 Animated Touch Grass Sunset.mp4, Background 21 Animated $EARN Sunset.mp4, Background 22 Animated Diecaster Desert.mp4, Background 23 Animated Landwolf on Base Desert.mp4, Background 24 Animated $EARN Desert.mp4, Background 25 Animated Gems Of Base Desert.mp4, Background 26 Animated $CHEWY Desert.mp4, Background 27 MOON Animated Gems Of Base UFO.mp4, Background 28 MOON Animated All Your Base UFO.mp4, Background 29 MOON Animated $CHEWY UFO.mp4, Background 30 MOON Animated Touch Grass UFO.mp4, Background 31 MOON Animated Jeetolax UFO.mp4, Background 32 MOON Animated Memgen UFO.mp4, Background 33 MOON Animated Emnirex UFO.mp4, Background 34 Motion Snowing.mp4, Background 35 MOON Animated Diecaster UFO.mp4, Background 36 MOON Animated Landwolf UFO.mp4, Background 37 MOON Animated $EARN UFO.mp4, Background 38 MOON Animated Million Bit Homepage UFO.mp4',
#                        'Banner Flags/Banner Flag 01 - None.png, Banner Flag 02 - OnChain Summer.png, Banner Flag 03 - Launched On Base.png, Banner Flag 04 - Degen.png, Banner Flag 05 - Chad.png, Banner Flag 06 - Based.png, Banner Flag 07 - Just $WAG IT.png, Banner Flag 08 - Gems Of Base.png, Banner Flag 09 - Jeetolax.png, Banner Flag 10 - CHEWY On Base.png, Banner Flag 11 - Million Bit Homepage.png, Banner Flag 12 - All Your Base.png, Banner Flag 13 - Touch Grass.png, Banner Flag 14 - Buy & Hold Earn.png, Banner Flag 15 - Race On Base Diecaster.png, Banner Flag 16 - Landwolf On Base.png',
#                        'Body/Fur 01 - Fox Orange Memgen.png, Fur 02 - Arctic Memgen.png,Fur 03 - Avax Red Memgen.png, Fur 04 - Binance Yellow Memgen.png, Fur 05 - Based Blue Memgen.png, Fur 06 - Camo Memgen.png, Fur 07 - Pink Memgen.png, Fur 08 - Tiger Memgen.png, Fur 09 - Solana Memgen.png Fur 10 - Leopard Memgen.png, Fur 11 - Emerald Memgen.png, Fur 12 - Based Blue Sapphire Memgen.png, Fur 13 - Diamond Memgen.png, Fur 14 - Alien Memgen.png',
#                        'Nose/Nose 01 - Black Nos.png, Nose 02 - Avax Red.png, Nose 03 - Pink Nose.png, Nose 04 - Based Blue Nose.png, Nose 05 - Xmas Red Nose.png',
#                        'Bling/Bling 01 - None.png, Bling 02 - Leather Collar.png, Bling 03 - Based Blue Collar.png, Bling 04 - Based Plaster.png, Bling 05 - Dog Tag Collar.png, Bling 06 - Gold T-Bone Collar.png',
#                        'Eyes/Eyes 01 - Common.png, Eyes 02 - Stoned Orange.png, Eyes 03 - Angry.png, Eyes 04 - Stoned Dark.png, Eyes 05 - Stoned Solana.png, Eyes 06 - Eye Patch.png, Eyes 07 - Stoned Avax.png, Eyes 08 - Based.png, Eyes 09 - Stoned Based.png, Eyes 10 - Sunglasses Macho.png, Eyes 11 - Surprised.png, Eyes 12 - Basedticles.png, Eyes 13 - Sunglasses Matrix.png, Eyes 14 - Cyborg.png, Eyes 15 - Bloodshot.png, Eyes 16 - Red Lazer Beam.png, Eyes 17 - Diamonds.png',
#                        'Headwear/Headwear 01 - None.png, Headwear 02 - Red Baseball Cap $WAG.png, Headwear 03 - Golden Laurel.png, Headwear 04 - Leprechaun.png, Headwear - 05 Based Blue Baseball Cap $EARN.png, Headwear 06 - Based Blue Baseball Cap Diecaster.png, Headwear 07 - Based Blue Baseball Cap Touch Grass.png, Headwear 08 - Based Blue Baseball Cap All Your Base.png, Headwear 09 - Based Blue Baseball Cap Touch Grass.png, Headwear 10 - Based Blue Baseball Cap Landwolf.png, Headwear 11 - Based Blue Baseball Cap $WAG.png, Headwear 12 - Based Blue Baseball Cap $WFK.png, Headwear 13 - Red Baseball Cap All Your Base.png, Headwear 14 - Red Baseball Cap $WFK.png, Headwear 15 - Red Baseball Cap Million Bit Homepage.png, Headwear 16 - Red Baseball Cap Jeetolax.png, Headwear 17 - Gold Crown.png, Headwear 18 - Red Baseball Cap Gems Of Base.png, Headwear 19 - Red Baseball Cap Earn.png, Headwear 20 - Red Baseball Cap Touch Grass.png, Headwear 21 - Red Baseball Cap Landwolf.png, Headwear 22 - Red Baseball Cap Diecaster.png, Headwear 23 - Red Baseball Cap Emnirex Influence.png, Headwear 24 - Red Baseball Cap Chewy.png, Headwear 25 - Based Blue Baseball Cap $CHEWY.png, Headwear 26 - Based Blue Baseball Cap Jeetolax.png',
#                         'Mouth/Mouth 01 - Expressionless.png, Mouth 02 - Dizzy.png, Mouth 03 - Flat.png, Mouth 04 - Woof.png, Mouth 05 - Smoking Refer.png, Mouth 06 - Manga Growling.png, Mouth 07 - Smile.png, Mouth 08 - Tongue Out.png'])


# Get total number of distinct possible combinations
def get_total_combinations():
    
    total = 1
    for layer in CONFIG:
        total = total * len(layer['traits'])
    return total


# Select an index based on rarity weights
def select_index(cum_rarities, rand):
    
    cum_rarities = [0] + list(cum_rarities)
    for i in range(len(cum_rarities) - 1):
        if rand >= cum_rarities[i] and rand <= cum_rarities[i+1]:
            return i
    
    # Should not reach here if everything works okay
    return None


# Generate a set of traits given rarities
def generate_trait_set_from_config():
    
    trait_set = []
    trait_paths = []
    
    for layer in CONFIG:
        # Extract list of traits and cumulative rarity weights
        traits, cum_rarities = layer['traits'], layer['cum_rarity_weights']

        # Generate a random number
        rand_num = random.random()

        # Select an element index based on random number and cumulative rarity weights
        idx = select_index(cum_rarities, rand_num)

        # Add selected trait to trait set
        trait_set.append(traits[idx])

        # Add trait path to trait paths if the trait has been selected
        if traits[idx] is not None:
            trait_path = os.path.join(layer['directory'], traits[idx])
            trait_paths.append(trait_path)
        
    return trait_set, trait_paths


# Generate the image set. Don't change drop_dup
def generate_images(edition, count, drop_dup=True):
    
    # Initialize an empty rarity table
    rarity_table = {}
    for layer in CONFIG:
        rarity_table[layer['name']] = []

    # Define output path to output/edition {edition_num}
    op_path = os.path.join('output', 'edition ' + str(edition), 'images')

    # Will require this to name final images as 000, 001,...
    zfill_count = len(str(count - 1))
    
    # Create output directory if it doesn't exist
    if not os.path.exists(op_path):
        os.makedirs(op_path)
      
    # Create the images
    for n in progressbar(range(count)):
        
        # Set image name
        media_name = str(n).zfill(zfill_count)
        
        # Get a random set of valid traits based on rarity weights
        trait_sets, trait_paths = generate_trait_set_from_config()

        # Generate the actual image
        output_file = os.path.join(op_path, media_name+".mp4")
        generate_single_media(trait_paths, output_file)
        
        # Populate the rarity table with metadata of newly created image
        for idx, trait in enumerate(trait_sets):
            if trait is not None:
                rarity_table[CONFIG[idx]['name']].append(trait[: -1 * len('.png')])
            else:
                rarity_table[CONFIG[idx]['name']].append('none')
    
    # Create the final rarity table by removing duplicate creat
    rarity_table = pd.DataFrame(rarity_table).drop_duplicates()
    print("Generated %i images, %i are distinct" % (count, rarity_table.shape[0]))
    
    if drop_dup:
        img_tb_removed = sorted(list(set(range(count)) - set(rarity_table.index)))
        print("Removing %i duplicate media..." % (len(img_tb_removed)))
        for i in img_tb_removed:
            os.remove(os.path.join(op_path, str(i).zfill(zfill_count)))
        for idx, img in enumerate(sorted(os.listdir(op_path))):
            os.rename(os.path.join(op_path, img), os.path.join(op_path, str(idx).zfill(zfill_count)))
    
    rarity_table = rarity_table.reset_index().drop('index', axis=1)
    return rarity_table

# Main function. Point of entry
def main():

    print("Checking assets...")
    parse_config()
    print("Assets look great! We are good to go!")
    print()

    tot_comb = get_total_combinations()
    print("You can create a total of %i distinct avatars" % (tot_comb))
    print()

    print("How many avatars would you like to create? Enter a number greater than 0: ")
    while True:
        num_avatars = int(input())
        if num_avatars > 0:
            break
    
    print("What would you like to call this edition?: ")
    edition_name = input()

    print("Starting task...")
    rt = generate_images(edition_name, num_avatars)

    print("Saving metadata...")
    rt.to_csv(os.path.join('output', 'edition ' + str(edition_name), 'metadata.csv'))

    print("Task complete!")


# Run the main function
main()