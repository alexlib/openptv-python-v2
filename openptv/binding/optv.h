/**
 * optv.h - Main header file for OpenPTV C library bindings
 *
 * This file serves as a wrapper that includes all the necessary headers
 * from the OpenPTV C library for use with the Cython bindings.
 */

#ifndef OPTV_H
#define OPTV_H

/* Include standard headers */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/* Define the basic types needed for the bindings */
typedef struct {
    double x;
    double y;
    double z;
} point3d_t;

typedef struct {
    double x;
    double y;
} point2d_t;

/* Function declarations for the bindings */
int track_particles(point3d_t *particles, int num_particles, 
                   double max_link_distance, void *trajectories);

int find_correspondences(point2d_t *points1, point2d_t *points2,
                        int num_points1, int num_points2,
                        void *correspondences);

/* 
 * Note: We're not including the OpenPTV headers here because we're using
 * our own implementation directly in this file.
 */

#endif /* OPTV_H */
