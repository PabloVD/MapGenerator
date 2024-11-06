import gradio as gr
from source.visualization_tools import *
from PIL import Image
import io

#--- Parameters ---#

# Number of bins per dimension
boxsize = 500
# Number of bins per dimension in the smoothed high resolution box
highboxsize = boxsize
# Threshold for the sea level
threshold = 0.6
# Sigma for the gaussian smoothing
sigma = 5.
# Initial random seed
llavor = 0
# Spectral index for the power spectrum (only for Gauss noise)
indexlaw = -3.
# Hurst index for Fractional Brownian Field
hurst = 0.5
# Choose kind of noise. See the source/field.py module for the options
kind_noise = "gauss"
# Ensure that the boundaries are sea if 1
make_island = 0

#--- Perlin parameters ---#
# Scale sets the size of the objects
# Set to e.g. 500 to bigger portions of land
scale = 500
# Octaves is the number of levels, and increases the granularity with higher values
# Lower values give less defined boundaries
octaves = 6
# Persistence determines how much each octave contributes to the overall shape (adjusts amplitude)
# Lower than 1 means that sucessive octaves contribute less
# Set to close to 1 to have more islands and less big structures
persistence = 0.5
# Lacunarity determines how much detail is added or removed at each octave (adjusts frequency)
# More than 1 means that each octave will increase it’s level of fine grained detail (increased frequency)
# For the octave i, the frecuency is lacunarity**i, and the amplitude is persistence**i
lacunarity = 2.0

if kind_noise == "gauss":
    params = indexlaw
elif kind_noise == "fbm":
    params = hurst
else:
    params = [scale,octaves,persistence,lacunarity,boxsize]


def generate_maps():

    images = []
        
    for llavor in range(9):
        fig = single_map(kind_noise,boxsize,llavor,params,sigma,threshold)
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')

        img = Image.open(img_buf)
        images.append(img)

    return images

with gr.Blocks() as demo:
    gr.Markdown("# Map generator")

    gallery = gr.Gallery(label="Generated maps", show_label=False, elem_id="gallery", columns=[3], rows=[3], object_fit="contain", height="auto")

    btn = gr.Button("Generate maps", scale=1)
    btn.click(generate_maps, None, gallery)

    # def fn(input):
    #     return generate_maps()

    
    # demo = gr.Interface(fn=fn, inputs="text",outputs=gallery)

if __name__ == "__main__":
    demo.launch()