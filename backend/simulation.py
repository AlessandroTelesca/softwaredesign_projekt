from robot import Robot

class Simulation:
    """
    TODO: Docstring
    """
    robots: list[Robot] = []

    def __init__(self, robots: list[Robot] = []):
        """
        TODO: Docstring
        """
        self.robots = robots
