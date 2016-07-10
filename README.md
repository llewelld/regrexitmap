# regrexitmap
Mapping the UK's regret at its decision to leave the EU

On 23rd June the British public voted with a majority of 51.9% to 48.1% to leave the EU. Many were shocked at the result, expressing [regrexit](https://twitter.com/search?q=%23REGREXIT) for the outcome.

Over four million people signed a [petition](https://petition.parliament.uk/petitions/131215) calling for a second chance at the referendum.

I was excited by the fact that both the referendum and petition data had been made available in JSON format. Wouldn't it be interesting to correlate the two and see how they compare? What's more, with the data broken down into areas, it should be easy, right?

Not so easy as it turned out. The two sources of data are partitioned into different regions. The Python code in this repository takes the data, distributes it by postcode across the regions, then calculates the proportion between the relative number of remain votes and the relative number of names on the petition.

There's also some Javascript for displaying the results on a pretty map using [LeafletJS](https://github.com/Leaflet/Leaflet).

You can see the final result at [www.regrexitmap.eu](http://www.regrexitmap.eu/)

## Copyright licences

Because this is basically just an exercise in data correlation, data is used from many different sources. They all have their own peculiar licences. The ```copyright`` folder contains the details.

## Data files

Most of the data files needed have been committed to git, but the postcode data from the UK Data Service is over the 100MB limit. To access and manage this data with GitHub, you'll need to use [git-lfs](https://git-lfs.github.com/).

