# regrexitmap
Mapping the UK's regret at its decision to leave the EU

On 23rd June the British public voted with a majority of 51.9% to 48.1% to leave the EU. Many were shocked at the result, expressing [regrexit](https://twitter.com/search?q=%23REGREXIT) for the outcome.

Over four million people signed a [petition](https://petition.parliament.uk/petitions/131215) calling for a second chance at the referendum.

I was excited by the fact that both the referendum and petition data had been made available in JSON format. Wouldn't it be interesting to correlate the two and see how they compare? What's more, with the data broken down into areas, it should be easy, right?

Not so easy as it turned out. The two sources of data are partitioned into different regions. The Python code in this repository takes the data, distributes it by postcode across the regions, then calculates the proportion between the relative number of remain votes and the relative number of names on the petition.

There's also some Javascript for displaying the results on a pretty map using [LeafletJS](https://github.com/Leaflet/Leaflet).

You can see the final result at [www.regrexitmap.eu](http://www.regrexitmap.eu/)

## Usage

The ```mapreduce.py``` inside the ```process``` can be used to simplify the GeoJSON feature outlines. It simplifies the constituency outlines by removing random points in a way that retains the overall coherence of the boundaries (it will only remove sensible points, and the points will be removed from all boundaries that share the same point).

The simplification process can take a long time, but because it's stochastic, running it iteratively on a simplified file has the same effect as running it on the original file, but with increasing speed.

The ```gendata.py``` file will pull in the postcode data, referendum results and petition signature to calculate the level of regrexit for each parliamentary constituency. The file ```change.js``` it outputs can be then be used for rendering the site (by replacing the ```site/data/change.js``` file).

The ```site``` folder contains everything needed to render the site. The site is entirely server-side static -- all of the dynamic work happens on the client-side, or is outsourced to Mapbox -- so there's no fancy installation procedure. Just copy the files to some webspace.

## Sources

* Referendum results [data](https://interactive.guim.co.uk/2016/06/eureferendum/booted/data/full.json) from the [Guardian](https://interactive.guim.co.uk/2016/06/eureferendum/booted/main.html).
* Petition [data](https://petition.parliament.uk/petitions/131215) from the UK Government and Parliament
* Martin Chorley's constituency GeoJSON [boundary data](https://github.com/martinjc/UK-GeoJson) 
* Map rendering code from [LeafletJS](http://leafletjs.com/examples/quick-start.html)
* Tiled map images from [Mapbox](https://www.mapbox.com/)
* Postcode [data](https://census.edina.ac.uk/pds.html) from the UK Data Service Census Support
* Typeface design by [Philipp Hubert and Sebastian Fischer](http://hubertfischer.com/work/type-rubik)

## Copyright licences

Because this is basically just an exercise in data correlation, data is used from many different sources. They all have their own peculiar licences. The ``copyright`` folder contains the details.

## Data files

Most of the data files needed have been committed to git, but the postcode data from the UK Data Service is over the 100MB limit. To access and manage this data with GitHub, you'll need to use [git-lfs](https://git-lfs.github.com/).

