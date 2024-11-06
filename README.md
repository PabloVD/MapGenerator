# MapGenerator

Generate maps of random maps from a gaussian field.

After being normalized and smoothed, only the mainland above a certain threshold is retained,
being the rest considered as sea.

The gaussian field is generated employing a cosmological package, [powerbox](https://powerbox.readthedocs.io/en/latest/index.html), from a power spectrum as input.

![An example of randomly generated islands](/images/gridmap_noise_gauss_threshold_0.6_sigma_5.0.png)