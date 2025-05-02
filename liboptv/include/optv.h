/**
 * Main header file for the liboptv C library.
 * 
 * This library provides core functionality for Particle Tracking Velocimetry
 * analysis, including tracking, calibration, and correspondence algorithms.
 */

#ifndef OPTV_H
#define OPTV_H

#ifdef __cplusplus
extern "C" {
#endif

/* Basic data structures */

/**
 * Structure representing a 3D point.
 */
typedef struct {
    double x;
    double y;
    double z;
} point3d_t;

/**
 * Structure representing a 2D point.
 */
typedef struct {
    double x;
    double y;
} point2d_t;

/* Function prototypes */

/**
 * Track particles across frames.
 * 
 * @param particles Array of particle positions
 * @param num_particles Number of particles
 * @param max_link_distance Maximum distance for linking particles
 * @param trajectories Output array for trajectories
 * @return Number of trajectories found
 */
int track_particles(point3d_t *particles, int num_particles, 
                   double max_link_distance, void *trajectories);

/**
 * Find correspondences between camera views.
 * 
 * @param points1 Points from first camera
 * @param points2 Points from second camera
 * @param num_points1 Number of points in first set
 * @param num_points2 Number of points in second set
 * @param correspondences Output array for correspondences
 * @return Number of correspondences found
 */
int find_correspondences(point2d_t *points1, point2d_t *points2,
                        int num_points1, int num_points2,
                        void *correspondences);

#ifdef __cplusplus
}
#endif

#endif /* OPTV_H */
