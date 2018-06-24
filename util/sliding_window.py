import numpy as np
import cv2


def slide_window(word_segment, cnn, window_size=50, step_size=1, topN=3, visualize=False, sliding_window_delay=100):
    segment_width = len(word_segment[0])
    segment_height = len(word_segment)

    window_size = np.min((window_size, segment_width, segment_height))
    window_x = 0
    window_y = 0

    x_iterations = int(np.ceil((segment_width - window_size) / (step_size * 1.0))) + 1
    y_iterations = int(np.ceil((segment_height - window_size) / (step_size * 1.0))) + 1

    map_width = x_iterations
    map_height = y_iterations
    confidence_map = [np.zeros((map_height, map_width)) for _ in range(topN)]
    character_map = [[['' for _ in range(map_width)] for _ in range(map_height)] for _ in range(topN)]

    # Slide window and analyze the character
    for i in range(y_iterations):
        for j in range(x_iterations):
            window = word_segment[window_y:(window_size + window_y), window_x:(window_size + window_x)]
            results = _analyze_window(window, cnn, topN=topN, visualize=visualize,
                                      sliding_window_delay=sliding_window_delay)

            for k in range(len(results)):
                xx = window_x / step_size
                yy = window_y / step_size
                confidence_map[k][yy, xx] = results[k][0]
                character_map[k][yy][xx] = results[k][1][0]

            window_x += step_size
        window_x = 0
        window_y += step_size

    if visualize:
        cv2.destroyAllWindows()

    return confidence_map, character_map


def get_window_groups(extrema, character_map, window_size=50, step_size=1, min_group_size=1, max_pixel_distance=1,
                      max_windows=450):
    elements = len(extrema)
    if elements > max_windows:
        print "Maximum number of windows exceeded: "
        print "\tAllowed: %d -> Received %d" % (max_windows, elements)
        return []

    m = np.zeros((elements, elements))
    max_distance = pow(pow(max_pixel_distance, 2) * 2, .5)

    # Create group grid.
    for i in range(elements):
        for j in range(elements):
            coor1 = map_coordinate_to_image_coordinate(extrema[i][0], extrema[i][1],
                                                       window_size=window_size, step_size=step_size)
            coor2 = map_coordinate_to_image_coordinate(extrema[j][0], extrema[j][1],
                                                       window_size=window_size, step_size=step_size)

            # Make sure that group members have the same label
            if character_map[extrema[i][0]][extrema[i][1]] != character_map[extrema[j][0]][extrema[j][1]]:
                continue

            if _distance(coor1[0], coor1[1], coor2[0], coor2[1]) <= max_distance:
                members = np.where(m[j, :] == 1)[0]
                for member in members:
                    m[i, member] = 1
                    m[member, i] = 1
                m[i, j] = 1
                m[j, i] = 1

    # Create window group list
    window_groups = []
    for i in range(elements):
        if m.shape[1] == 0:
            break
        if m[i, :].sum() < min_group_size:
            continue

        members = np.where(m[i, :] == 1)
        group = []

        for member in members[0]:
            group.append(extrema[member])

        m[:, members[0]] = 0
        window_groups.append(group)
    return window_groups


def sort_window_groups(window_groups, min_character_distance=25):
    assigned, groups = [], []
    sorted_window_groups = sorted(window_groups, key=lambda x: _get_window_group_center(x)[1])

    for group1 in sorted_window_groups:
        if group1 in assigned:
            continue

        assigned.append(group1)
        groups.append([group1])

        for group2 in sorted_window_groups:
            if group1 == group2 or group2 in assigned:
                continue

            center1 = _get_window_group_center(group1)
            center2 = _get_window_group_center(group2)

            if _distance(0, center1[1], 0, center2[1]) < min_character_distance:
                assigned.append(group2)
                groups[-1].append(group2)

    for i in range(len(groups)):
        groups[i].sort(key=lambda x: len(x), reverse=True)

    return groups


def map_coordinate_to_image_coordinate(x, y, window_size=50, step_size=1):
    xx = x * step_size + window_size / 2.0
    yy = y * step_size + window_size / 2.0
    return xx, yy


def image_coordinate_to_map_coordinate(x, y, window_size=50, step_size=1):
    xx = (x - window_size / 2) / step_size
    yy = (y - window_size / 2) / step_size
    return xx, yy


#### HELPER FUNCTIONS ####

def _analyze_window(window, cnn, topN=3, visualize=False, sliding_window_delay=100):
    if visualize:
        cv2.imshow("Sliding Window", window)
        cv2.waitKey(sliding_window_delay)

    total, results = cnn.analyze_character(window)
    results = sorted(results.items(), reverse=True)[:topN]
    return results


def _get_window_group_center(group):
    total = [0, 0]
    for member in group:
        total[0] += member[0]
        total[1] += member[1]
    return total[0] / len(group), total[1] / len(group)


def _distance(x, y, xx, yy):
    return pow(pow(x - xx, 2) + pow(y - yy, 2), .5)
