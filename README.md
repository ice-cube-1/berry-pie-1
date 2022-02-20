<h1>Berry-pie-1</h1>
<h2>This is a repository for an entry into the astro-pi competition.</h2>
<p>There are 4 folders, two as actual projects, one as a script to train / test a binary AI using a coral edge tpu, and one to plot data on a map in a webpage from a CSV file.<p>
<h3>mapOfPiData</h3>
<p>This needs a data folder with images corresponding to the image names in the CSV file, or a generated CSV file by main.py in terrain. It is used <b>after</b> all of the others.</p>
<h3>terrain</h3>
<p>This needs a "data" folder to run correctly.</p>
<h3>wildfire</h3>
<p>This is mostly untested. It needs a working AI (produced by wildfireAiTrainAndTest) called wildfire-vs-nonwildfire.tflite, as well as an empty data folder. Without these, it will run with errors.</p>
<h3>wildfireAiTrainAndTest</h3>
<p>Again, this is mostly untested. The train script needs a data folder, with two folders inside of it, one called "wildfire" and the other called "nonwildfire". These both need equal amounts of images (preferably over 300) of both categories. Within the data folder a txt file with the same name and data as the one under wildfire is also needed. The model outputted will be next to the mobilenet....tflite one, and can then be copied into the test directory. This will also need the txt file mentioned above, but this time not within a layer of directory, as well as a folder called data, with two subfolders that have the same names. These need less (c.50) images in each, although they must be different to the ones under "train". When running, two CSV files should be produced, one for each category. If these look as if most of the images are being classified correctly, the AI can be used in the wildfire folder.</br></br></br>ice-cube-1</p>
