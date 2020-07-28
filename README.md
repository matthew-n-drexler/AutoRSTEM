# AutoRSTEM
A tool for the automated analysis of HAADF STEM images
imganalscript.py contains a simple script that will determine relevant features, connect them in a lattice, and return a list of the connections between features.
Other files contain methods for more custom methods of analysis.
fftcompression.py will determine the radius within which all diffraction points are contained.
rsicompression.py will identify features.
sandwichsmooth.py will reduce noise.
lonelattice.py will connect features based on proximity to one another, refine their position, and provide information about the connections.
pointfitting.py contains methods used by lonelattice to refine feature positions.
latticeanalysis.py takes the information provided by lonelattice.py and transforms it into a useful form for further analysis.
