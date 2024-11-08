import gradio as gr
from source.visualization_tools import single_map
from PIL import Image
import io
import random

# Threshold for the sea level
threshold = 0.6
# Sigma for the gaussian smoothing
sigma = 5.

def generate_maps(kind_noise,boxsize,index,scale,octaves,persistence,lacunarity,make_island,deterministic):

    if kind_noise=="gauss":
        params = index
    else:
        params = [scale,octaves,persistence,lacunarity,boxsize]
    
    if deterministic:
        seeds = range(3)
    else:
        seeds = random.sample(range(1000),3)

    images = []

    for llavor in seeds:
        fig = single_map(kind_noise,boxsize,llavor,params,sigma,threshold,make_island=make_island)
        img_buf = io.BytesIO()
        fig.savefig(img_buf, format='png')

        img = Image.open(img_buf)
        images.append(img)

    return images

md ="""
    # Map generator

    Generate procedural geographic maps from random fields.
    """


with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown(md)

    with gr.Accordion("General settings", open=True):
    
        with gr.Row():
            kind_noise = gr.Dropdown(["gauss", "perlin", "warped_perlin"], label="Random field", value="gauss")
            boxsize = gr.Slider(100, 1000, value=500, label="Box size")#, info="Box size"),
            make_island = gr.Checkbox(label="Island", info="Mark to ensure that boundaries are sea")
            deterministic = gr.Checkbox(label="Deterministic", info="Mark to employ the same random seed")

    with gr.Accordion("Gaussian field settings", open=False):
        index = gr.Slider(-5, -1, value=-3, label="Spectral index")#, info="Spectral index"),
        
    with gr.Accordion("Perlin field settings", open=False):
        with gr.Row():
            scale = gr.Slider(100, 1000, value=500, label="Scale")
            octaves = gr.Slider(1, 10, value=6, label="Octaves", step=1)
            persistence = gr.Slider(0, 1, value=0.5, label="Persistence")
            lacunarity = gr.Slider(0.1, 10, value=2, label="Lacunarity")
    
    
    inputs = [kind_noise,boxsize,index,scale,octaves,persistence,lacunarity,make_island,deterministic]

    btn = gr.Button("Generate maps", scale=1)

    gallery = gr.Gallery(label="Generated maps", show_label=False, elem_id="gallery", columns=[3], rows=[1], height="20vw")

    btn.click(generate_maps, inputs=inputs, outputs=gallery)


if __name__ == "__main__":
    demo.launch()