import numpy as np

def otsu_intraclass_variance(image, threshold):
	"""
	Otsu’s intra-class variance.
	If all pixels are above or below the threshold, this will throw a warning that can safely be ignored.
	"""
	return np.nansum([
		np.mean(cls) * np.var(image,where=cls)
		#   weight   ·  intra-class variance
		for cls in [image>=threshold,image<threshold]
	])
	# NaNs only arise if the class is empty, in which case the contribution should be zero, which `nansum` accomplishes.

# Random image for demonstration:
image = np.random.randint( 2, 253, size=(50,50) )

otsu_threshold = min(
		range( np.min(image)+1, np.max(image) ),
		key = lambda th: otsu_intraclass_variance(image,th)
	)
