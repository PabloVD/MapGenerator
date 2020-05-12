# IslandGenerator

Generate maps of random islands from a gaussian field.

After being normalized and smoothed, only the mainland above a certain threshold is retained,
being the rest considered as sea.

The gaussian field is generated employing a cosmological package, powerbox, from a power spectrum as input.

![An example of randomly generated islands](/images/archipielago_9seeds_indexlaw_-3.0_threshold_0.6_sigma_5.0.png)