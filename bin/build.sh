# Setup local environment:
cd `dirname $0`/../..

colcon build --packages-select tiled_node tiled_test
