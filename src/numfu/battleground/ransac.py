# a function that performs RANSAC on a set of 3d points
def ransac(points, num_iterations, threshold, num_points_to_sample, min_num_points_in_model):
    best_model = None
    best_consensus_set = None
    best_error = np.inf
    for i in range(num_iterations):
        # randomly sample points
        indices = np.random.choice(points.shape[0], num_points_to_sample)
        consensus_set = points[indices,:]
        maybe_model = fit_plane(consensus_set)
        # find points that agree with model
        distances = compute_error(points, maybe_model)
        consensus_indices = np.where(distances < threshold)[0]
        consensus_set = points[consensus_indices]
        if consensus_set.shape[0] >= min_num_points_in_model:
            maybe_model = fit_plane(consensus_set)
            # compute error of all points to model
            distances = compute_error(points, maybe_model)
            total_error = np.sum(distances)
            if total_error < best_error:
                best_error = total_error
                best_model = maybe_model
                best_consensus_set = consensus_set
    return best_model, best_consensus_set

