#ifndef __VISUALIZE_H
#define __VISUALIZE_H
/**
* @brief Initialize the visualization
* @param mode: true for pipe mode, false for log mode
*/
void init_visualize(bool mode);

/**
* @brief Visualize the data
* @param see the header of visualize.py
*/

void perframe_visualize
    (double p1x, double p1y, double v1x, double v1y, int a1x, int a1y,
     double p2x, double p2y, double v2x, double v2y, int a2x, int a2y);

#endif // !__VISUALIZE_H
