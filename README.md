# MapGenerator

Generate procedural geographic maps from random fields.

**Try an interactive demo [here](https://huggingface.co/spaces/PabloVD/MapGenerator).**

## Map generation

The process of map generation is as follows:

1. Generate a random field, choosing from the list of available random fields
2. Normalize the field between 0 and 1
3. Smooth the field with a gaussian filter
4. Retain only the mainland above a certain threshold

## Random fields

The available random fields are:

- `gauss`: Random gaussian field, with a given power spectrum, computed using the package [powerbox](https://powerbox.readthedocs.io/en/latest/index.html)
- `perlin`: Perlin noise, computed using the package [noise](https://pypi.org/project/noise/)
- `warped_perlin`: Perlin noise with domain warping, computed using the package [noise](https://pypi.org/project/noise/)
- `cos`: Sinusoidal noise (to be improved)
- `fbm`: Fractional Brownian Field

![An example of randomly generated islands](/images/gridmap_noise_gauss_threshold_0.6_sigma_5.0.png)