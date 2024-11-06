import gradio as gr
from source.visualization_tools import *
from PIL import Image
import io
import random

# Threshold for the sea level
threshold = 0.6
# Sigma for the gaussian smoothing
sigma = 5.

def generate_maps(kind_noise,boxsize,index,make_island,deterministic):

    params = index
    
    images = []
    if deterministic:
        seeds = range(3)
    else:
        seeds = random.sample(range(1000),3)
    for llavor in seeds:
        fig = single_map(kind_noise,boxsize,llavor,params,sigma,threshold,make_island=make_island)
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')

        img = Image.open(img_buf)
        images.append(img)

    return images

md = """
     # Map generator

     Generate maps of random maps from a gaussian field.

     After being normalized and smoothed, only the mainland above a certain threshold is retained,
     being the rest considered as sea.
     """

"""
with gr.Blocks() as demo:

    gr.Markdown(md)

    gallery = gr.Gallery(label="Generated maps", show_label=False, elem_id="gallery", columns=[3], rows=[1], object_fit="contain", height="auto")

    btn = gr.Button("Generate maps", scale=1)
    btn.click(generate_maps, None, gallery)
"""

"""
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
"""

gallery = gr.Gallery(label="Generated maps", show_label=False, elem_id="gallery", columns=[3], rows=[1], object_fit="contain", height="auto")

demo = gr.Interface(
    generate_maps,
    [
        gr.Dropdown(["gauss", "perlin"], label="Field", info="Kind of random field", value="gauss"),
        gr.Slider(100, 1000, value=500, label="Box size"),#, info="Box size"),
        gr.Slider(-5, -1, value=-3, label="Spectral index"),#, info="Spectral index"),
        # gr.Slider(100, 1000, value=500, label="Scale"),#, info="Box size"),
        # gr.Slider(1, 10, value=6, label="Octaves"),#, info="Spectral index"),
        # gr.Slider(0, 1, value=0.5, label="Persistence"),#, info="Box size"),
        # gr.Slider(0.1, 10, value=2, label="Lacunarity"),#, info="Spectral index"),
        gr.Checkbox(label="Island", info="Mark to ensure that boundaries are sea"),
        gr.Checkbox(label="Deterministic", info="Mark to employ the same random seed"),
    ],
    gallery,
    title="Map generator",
    description="Generate maps of random maps from a gaussian field"
)

if __name__ == "__main__":
    demo.launch()