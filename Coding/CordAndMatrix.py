import pickle

# Provided coordinates
coordinates = [
    (-26.039048847328033, 27.99350625664295),
    (-26.10685303608294, 27.9608460741248),
    (-26.10867869020804, 28.052654245906318),
    (-26.11888697572315, 28.140610036644834),
    (-26.12623160177116, 28.133491478383434),
    (-26.138997554073267, 28.087892104735953),
    (-26.16146886845589, 28.01245028464389),
    (-26.166328920059495, 28.053935229847298),
    (-26.181702814150665, 28.004133740939366),
    (-26.183058180599772, 28.036467120909183),
    (-26.18063943468783, 28.118213505526864),
    (-26.183188904736255, 28.115609869449287),
    (-26.188709014466102, 28.123241261827896),
    (-26.196469070140626, 28.041974599574154),
    (-26.205429048443463, 28.046259673372333),
    (-26.211516840580263, 28.100514919954254),
    (-26.24129741467129, 28.0100862125746),
    (-26.266325966638917, 27.98269252499411),
    (-26.27261645951534, 28.0286082115355),
    (-26.26585159114156, 28.059429874597356),
    (-26.132689252040052, 28.23244829264204)
]

# Provided distance matrix
distance_matrix = [
    [0, 8215, 9739, 17166, 17013, 14573, 13743, 15386, 15898, 16578, 20073, 20138, 21089, 18161, 19236, 21952, 22550, 25295, 26207, 26064, 26035],
    [8215, 0, 9170, 17999, 17371, 13178, 7964, 11406, 9378, 11348, 17722, 17627, 18590, 12840, 13886, 18159, 15736, 17866, 19633, 20232, 27268],
    [9739, 9170, 0, 8855, 8304, 4873, 7111, 6412, 9455, 8427, 10337, 10399, 11350, 9820, 10777, 12393, 15346, 18868, 18386, 17490, 18148],
    [17166, 17999, 8855, 0, 1083, 5718, 13641, 10133, 15308, 12608, 7221, 7573, 7955, 13089, 13464, 11050, 18839, 22739, 20423, 18239, 9296],
    [17013, 17371, 8304, 1083, 0, 4768, 12702, 9107, 14309, 11563, 6239, 6580, 7022, 12018, 12383, 10038, 17758, 21657, 19351, 17194, 9905],
    [14573, 13178, 4873, 5718, 4768, 0, 7934, 4552, 9614, 7095, 5532, 5639, 6558, 7864, 8475, 8162, 13772, 17624, 15992, 14389, 14447],
    [13743, 7964, 7111, 13641, 12702, 7934, 0, 4175, 2398, 3392, 10768, 10574, 11463, 4881, 5939, 10401, 8880, 12032, 12464, 12517, 22191],
    [15386, 11406, 6412, 10133, 9107, 4552, 4175, 0, 5256, 2549, 6609, 6434, 7350, 3558, 4415, 6845, 9414, 13196, 12086, 11080, 18206],
    [15898, 9378, 9455, 15308, 14309, 9614, 2398, 5256, 0, 3230, 11384, 11125, 11910, 4117, 4963, 10172, 6653, 9650, 10400, 10862, 23430],
    [16578, 11348, 8427, 12608, 11563, 7095, 3392, 2549, 3230, 0, 8162, 7897, 8681, 1589, 2673, 7131, 6990, 10700, 9990, 9487, 20346],
    [20073, 17722, 10337, 7221, 6239, 5532, 10768, 6609, 11384, 8162, 0, 385, 1028, 7808, 7690, 3861, 12722, 16539, 13583, 11143, 12587],
    [20138, 17627, 10399, 7573, 6580, 5639, 10574, 6434, 11125, 7897, 385, 0, 978, 7494, 7348, 3492, 12352, 16163, 13198, 10765, 12943],
    [21089, 18590, 11350, 7955, 7022, 6558, 11463, 7350, 11910, 8681, 1028, 978, 0, 8154, 7903, 3402, 12713, 16463, 13272, 10681, 12554],
    [18161, 12840, 9820, 13089, 12018, 7864, 4881, 3558, 4117, 1589, 7808, 7494, 8154, 0, 1084, 6075, 5913, 9762, 8572, 7909, 20289],
    [19236, 13886, 10777, 13464, 12383, 8475, 5939, 4415, 4963, 2673, 7690, 7348, 7903, 1084, 0, 5455, 5378, 9276, 7676, 6846, 20265],
    [21952, 18159, 12393, 11050, 10038, 8162, 10401, 6845, 10172, 7131, 3861, 3492, 3402, 6075, 5455, 0, 9609, 13238, 9879, 7300, 15817],
    [22550, 15736, 15346, 18839, 17758, 13772, 8880, 9414, 6653, 6990, 12722, 12352, 12713, 5913, 5378, 9609, 0, 3900, 3942, 5627, 25261],
    [25295, 17866, 18868, 22739, 21657, 17624, 12032, 13196, 9650, 10700, 16539, 16163, 16463, 9762, 9276, 13238, 3900, 0, 4631, 7652, 29013],
    [26207, 19633, 18386, 20423, 19351, 15992, 12464, 12086, 10400, 9990, 13583, 13198, 13272, 8572, 7676, 9879, 3942, 4631, 0, 3164, 25606],
    [26064, 20232, 17490, 18239, 17194, 14389, 12517, 11080, 10862, 9487, 11143, 10765, 10681, 7909, 6846, 7300, 5627, 7652, 3164, 0, 22743],
    [26035, 27268, 18148, 9296, 9905, 14447, 22191, 18206, 23430, 20346, 12587, 12943, 12554, 20289, 20265, 15817, 25261, 29013, 25606, 22743, 0]
]

# Save to file
with open('coordinates.pkl', 'wb') as f:
    pickle.dump(coordinates, f)

with open('distance_matrix.pkl', 'wb') as f:
    pickle.dump(distance_matrix, f)