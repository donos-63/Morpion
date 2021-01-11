class GraphicalManager():
    __instance = None

    def initialize_instance(render):
        GraphicalManager.__instance = render

    def get_instance():
        if(GraphicalManager.__instance == None):
            GraphicalManager.__instance = GraphicalManager()
        
        return GraphicalManager.__instance
