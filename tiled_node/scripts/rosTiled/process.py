import rclpy, numpy as np, tiledland as tll
from rclpy.node import Node
from rclpy.context import Context
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Point
from nav_msgs.msg import OccupancyGrid

class Process() :
    # Constructor:
    def __init__(self):
        self._rosNode= None
        self._rosNodeMulti= None
        self._gridmap= OccupancyGrid()
        self._scene= tll.Scene()

    # ROS Wraping:
    def rosInit(self, process_name, multirobot= False):
        # Ros initialization: 
        rclpy.init()
        executor= rclpy.get_global_executor()

        # local node :
        contextLocal= Context()
        contextLocal.init()
        self._rosNode = Node( process_name, context=contextLocal )
        executor.add_node( self._rosNode )
        
        # Multi node :
        if multirobot :
            contextMulti = Context()
            contextMulti.init(domain_id= 140)
            self._rosNodeMulti = Node( f"parasit_{ rosName }", context=contextMulti )
            executor.add_node( self._rosNodeMulti )
        
        # default events handling :
        self._rosNode.create_timer( 1.2, self.routine )

        return self

    def rosSpin(self):
        # Infinite loop:
        executor= rclpy.get_global_executor()
        executor.spin()

        # Clean stop:
        self._rosNode.destroy_node()
        self._rosNode= None
        if self._rosNodeMulti : 
            self._rosNodeMulti.destroy_node()

    def rosLogInfo(self, msg):
        self._rosNode.get_logger().info(msg)
        return self

    # ROS gridmap subscription:
    def rosOccupGrid_to_gridmap( self, gridmapMsg ):
        # Reading the data
        gridmapMsg
        width= gridmapMsg.info.width
        height= gridmapMsg.info.height
        resolution= round(gridmapMsg.info.resolution, 4)
        position= gridmapMsg.info.origin.position
        if round(position.z, 8) != 0.0 :
            self.rosLogInfo( f"not coherent Z translation : {position.z}" )
        pos_x, pos_y= position.x, position.y
        rotate= gridmapMsg.info.origin.orientation
        if round(rotate.x, 8) != 0.0 or round(rotate.y, 8) != 0.0 : 
            self.rosLogInfo( f"not coherent X or Y rotation : {rotate.x, rotate.y}" )
        if round(rotate.z, 8) != 0.0 : 
            self.rosLogInfo( f"Rotation in Z not taked into account... : {rotate.z}" )
        
        grid= np.array(gridmapMsg.data, dtype=np.int8).reshape((height, width) )
        
        reverseGrid= [
            grid[i] for i in range( len(grid)-1, -1, -1 )
        ]
        transform= {
            -1: tll.Grid.STATE_UNKWON,
            0: tll.Grid.STATE_FREE,
            100: tll.Grid.STATE_OCCUPIED
        }
        self._gridmap= tll.Grid().initializeTransform( reverseGrid, transform, tll.Point(pos_x, pos_y), resolution )
        return self
    
    def rosOccupGrid_to_scene( self, gridmapMsg, tileExpectedSize= 1.2 ):
        self.rosOccupGrid_to_gridmap( gridmapMsg )
        self._scene.fromGridConvexes( self._gridmap, tileExpectedSize, matters=[tll.Grid.STATE_FREE] )
        return self

    
    def subscribeToGridMap( self, topicName, callback ):
        self._rosNode.create_subscription( OccupancyGrid, topicName, callback, 10 )
        return self
    
    # ROS tiled markers publishing:
    def activateMarkerPublisher( self, topicName ):
        self._pub_marker= self._rosNode.create_publisher( Marker, topicName, 10 )
        # Initialize msg squeletoms
        self._tileMarker= Marker()
        self._tileMarker.type= Marker.LINE_STRIP
        self._tileMarker.ns = "tiles"
        self._tileMarker.scale.x = 0.1
        self._tileMarker.color.a = 1.0

        self._nodeMarker= Marker()
        self._nodeMarker.type= Marker.SPHERE_LIST
        self._nodeMarker.ns = "nodes"
        self._nodeMarker.scale.x = 0.1
        self._nodeMarker.scale.y = 0.1
        self._nodeMarker.scale.y = 0.1
        self._nodeMarker.color.a = 1.0

    def setTileMarkerHeader(self, header):
        self._tileMarker.header= header
        return self

    def markeTile(self, tile):
        self._tileMarker.id= tile.id()
        tileColor= self._tileMarker.color 
        if tile.matter() == 0 :
            tileColor.r, tileColor.b, tileColor.g= (0.0, 0.0, 1.0)
        elif tile.matter() == 1 :
            tileColor.r, tileColor.b, tileColor.g= (1.0, 0.0, 0.0)
        else :
            tileColor.r, tileColor.b, tileColor.g= (0.0, 1.0, 0.0)
        
        self._tileMarker.points= []
        points= tile.body().points()
        for p in points + [points[0]] :
            rosPoint= Point()
            rosPoint.x, rosPoint.y, rosPoint.z=  p.x(), p.y(), 0.0
            self._tileMarker.points.append(rosPoint)
        
        self._pub_marker.publish(self._tileMarker)

    def setGraphMarkerHeader(self, header):
        self._nodeMarker.header= header
        return self
    
    def markeSceneGraph(self):
        freeNodePoints= []
        for tile in self._scene.tiles() :
            px, py= tile.position().asTuple()
            rosPoint= Point()
            rosPoint.x, rosPoint.y, rosPoint.z=  px, py, 0.0
            if tile.matter() == 0 :
                freeNodePoints.append(rosPoint)

        self._nodeMarker.id= 0
        self._nodeMarker.color.r = 0.0
        self._nodeMarker.color.g = 1.0
        self._nodeMarker.color.b = 0.0
        self._nodeMarker.points= freeNodePoints
        
        self._pub_marker.publish(self._nodeMarker)
        return self
    
    # ros routine callback :
    def routine(self):
        self.rosLogInfo("Ba-Boum...")
    
    # TiledLand Wraping:
    def drawScene(self, filename= "tiledmap.svg", width=1200, height=800 ):
        a= tll.createArtistSVG( "tiledmap.svg", width, height )
        a.fit( self._scene )
        self._scene.draw(a)
        self._scene.drawNetwork(a)
        a.flip()
        return self
