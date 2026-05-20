# map construction definition

define floorplan model
(
  # sombre, sensible, artistic
  color "gray30"

  # most maps will need a bounding box
  boundary 1

  gui_nose 0
  gui_grid 0

  gui_outline 0
  gripper_return 0
  fiducial_return 0
  laser_return 1
)

define office_map floorplan
(
  size [18.000 18.000 0.800]
  pose [10 10 0 0]
  bitmap "bitmaps/office.png"
  gui_move 0 
)

define cave_map floorplan
(
  size [30.000 24.000 0.800]
  pose [14 11 0 0]
  bitmap "bitmaps/cave.png"
  gui_move 0 
)

define willow_map floorplan
(
  size [120.000 120.000 0.800]
  pose [62 62 0 0]
  bitmap "bitmaps/willow.png"
  gui_move 0
)

define small_block model
(
  size [0.5 0.5 0.5]
  gui_nose 0
)

