import numpy as np
from utils import Directions


class BaseAgent(object):
    def __init__(self, height, width, initial_strength, name='base_agent'):
        """
        Base class for a game agent

        Parameters
        ----------
        height: int
            Height of the game map
        width: int
            Width of the game map
        initial_strength: int
            Initial strength of the agent
        name: str
            Name of the agent
        """
        self.height = height
        self.width = width
        self.initial_strength = initial_strength
        self.name = name

    def step(self, location, strength, game_map, map_objects):
        """

        Parameters
        ----------
        location: tuple of int
            Current location of the agent in the map
        strength: int
            Current strength of the agent
        game_map: numpy.ndarray
            Map of the game as observed by the agent so far
        map_objects: dict
            Objects discovered by the agent so far


        Returns
        -------
        direction: Directions
            Which direction to move
        """
        pass


class RandomAgent(BaseAgent):
    """
    A random agent that moves in each direction randomly

    Parameters
    ----------
    height: int
        Height of the game map
    width: int
        Width of the game map
    initial_strength: int
        Initial strength of the agent
    name: str
        Name of the agent
    """

    def __init__(self, height, width, initial_strength, name='random_agent'):
        super().__init__(height=height, width=width,
                         initial_strength=initial_strength, name=name)

    def step(self, location, strength, game_map, map_objects):
        """
        Implementation of a random agent that at each step randomly moves in
        one of the four directions

        Parameters
        ----------
        location: tuple of int
            Current location of the agent in the map
        strength: int
            Current strength of the agent
        game_map: numpy.ndarray
            Map of the game as observed by the agent so far
        map_objects: dict
            Objects discovered by the agent so far

        Returns
        -------
        direction: Directions
            Which direction to move
        """
        return np.random.choice(list(Directions))


class HumanAgent(BaseAgent):
    """
    A human agent that that can be controlled by the user. At each time step
    the agent will prompt for an input from the user.

    Parameters
    ----------
    height: int
        Height of the game map
    width: int
        Width of the game map
    initial_strength: int
        Initial strength of the agent
    name: str
        Name of the agent
    """

    def __init__(self, height, width, initial_strength, name='human_agent'):
        super().__init__(height=height, width=width,
                         initial_strength=initial_strength, name=name)

    def step(self, location, strength, game_map, map_objects):
        """
        Implementation of an agent that at each step asks the user
        what to do

        Parameters
        ----------
        location: tuple of int
            Current location of the agent in the map
        strength: int
            Current strength of the agent
        game_map: numpy.ndarray
            Map of the game as observed by the agent so far
        map_objects: dict
            Objects discovered by the agent so far

        Returns
        -------
        direction: Directions
            Which direction to move
        """
        dir_dict = {'N': Directions.NORTH,
                    'S': Directions.SOUTH,
                    'W': Directions.WEST,
                    'E': Directions.EAST}

        dirchar = ''
        while not dirchar in ['N', 'S', 'W', 'E']:
            dirchar = input("Please enter a direction (N/S/E/W): ").upper()

        return dir_dict[dirchar]

#Our implemented agent named "quad_agent"
class QuadAgent(BaseAgent):
    """
    Our HUERISTIC: 
        Initially the agent will choose the path with least cost, if there are no special conditions.
        It checks in the frontier whether a visited node is present or not, if so, it ignores it and chooses
        the nodes that are not visited and helps us in exploring more nodes.
        When the agent comes accross any power-ups and if it is in the frontier or adjacent node, it will move
        towards it and if it is in its diagnoal and visible nodes then it will choose the best adjacent node to reach the power-up.
        Everytime it comes across a skeleton, monster or agent, it calculates the strength of the other as well as the cost to reach that monster or agent
        and will decide whether to fight agent or boss based on a winning chance which also is calculated and comapared later with random
        probability of fight. If the probability decides to not fight then agent will keep exploring the map. If the agent comes across a skeleton
        then it will simply compare strenghts and it will fight if and only if the agent's strength is greater than the skelton's.
        
    Parameters
    ----------
    height: int
        Height of the game map
    width: int
        Width of the game map
    initial_strength: int
        Initial strength of the agent
    name: str
        Name of the agent
    """

    def __init__(self, height, width, initial_strength, name='quad_agent'):
        super().__init__(height=height, width=width,
                         initial_strength=initial_strength, name=name)

    #Some of the global variables for the class
    visited = []
    counter = 1
    visited_tail = 0
    
    
    def makedict(c_list):       #This function will map 2D list input to coordinate list
        dictionary= c_list
        #use c_list tuples as keys
        #get corresponding  p,m,s and w with their respective coordinates
        for i in dictionary.keys():
            if dictionary[i]== 0:
                dictionary[i]=1
            elif dictionary[i]==1:
                dictionary[i]=3
            elif dictionary[i]==2 :
                dictionary[i]=10
            elif dictionary[i]==3 :
                dictionary[i]=-1
            else:
                dictionary[i]=0          
        return dictionary
    
    def dora_explora(t_frontier,power_objects,location,size, cost_dict, treasure_route):
        #cur is the the node suggested by the function
        cur = (-1,-1)
        cor_f = []
        front_cordinates = [(-1,0),(0,1),(1,0),(0,-1)]
        #Condition to perform backtrack
        if len(t_frontier) == 0:
            QuadAgent.counter += 1
            t_cur = QuadAgent.visited[len(QuadAgent.visited) - QuadAgent.counter]
            #To find the best possible node to backtrack to
            for i in range(len(front_cordinates)):
                cor_f.append((front_cordinates[i][0] + location[0], front_cordinates[i][1] + location[1]));

            if t_cur in cor_f:
                cur = t_cur
            else:
                for i in range(len(QuadAgent.visited)):
                    QuadAgent.counter += 1
                    t_cur = QuadAgent.visited[len(QuadAgent.visited) - QuadAgent.counter]
                    if t_cur in cor_f:
                        cur = t_cur
                        break;
                        
        #This condition is to select best node when power-ups are in the visible nodes
        elif len(power_objects) != 0:
            if len(treasure_route) > 0: #Monsters
                for k,v in treasure_route.items():                    
                    cur = k
                    QuadAgent.counter = 1
            else:  #If power-up is in frontier
                for k,v in power_objects.items():
                    if k in t_frontier.keys():
                        cur = k
                        QuadAgent.counter = 1
                if cur == (-1,-1): #If until now no condition is satisfied
                    for k,v in power_objects.items():
                        node_heu = []
                        nodes = []
                        close_dora = []
                        medi_route = {}
                        #Calculating manhattan distance to reach the power-up with best least cost path
                        for k1,v1 in t_frontier.items():
                            nodes.append(k1)
                            cost = ( abs(k1[0]-k[0]) + abs(k1[1]-k[1]) )
                            node_heu.append(cost)
                        sort_dist = np.argsort(node_heu)
                        if len(t_frontier) == 1:
                            close_dora.append(nodes[sort_dist[0]])
                            medi_route[close_dora[0]] = cost_dict[close_dora[0]]
                        elif len(t_frontier) > 1:
                            close_dora.append(nodes[sort_dist[1]])
                            if sort_dist[0] != sort_dist[1]:
                                medi_route[close_dora[0]] = cost_dict[close_dora[0]]
                            else:
                                if cost_dict[close_dora[0]] < cost_dict[close_dora[1]]:
                                    medi_route[close_dora[0]] = cost_dict[close_dora[0]]
                                else:
                                    medi_route[close_dora[1]] = cost_dict[close_dora[1]]
                        
                    for k2,v2 in medi_route.items():
                        cur = k2;
                    QuadAgent.counter = 1
            #Appending the suggested node to visited list        
            QuadAgent.visited.append(cur)            
            
        else:
            key = []
            sort=[t_frontier[k] for k in sorted(t_frontier,key=t_frontier.__getitem__)]
                    
            for k,v in t_frontier.items():
                        if v==sort[0]:
                            key.append(k)

            if len(key) == 1:
                cur = key[0]
                QuadAgent.counter = 1
            #If multiple keys are present with the same cost terrain                
            else:
                for i in key:
                    x, y = i
                    if x == 1 or x == (size-1) or y == 1 or y == (size-1):
                        cur = i
                    elif x == 0 or x == size or y == 0 or y == size:
                        cur = i
                    else:
                        cur = key[0]
                QuadAgent.counter = 1
            QuadAgent.visited.append(cur)
        
        #returning the suggested node
        return cur
        

    def step(self, location, strength, game_map, map_objects):
        """
        Implementation of an agent that at each step asks the user
        what to do

        Parameters
        ----------
        location: tuple of int
            Current location of the agent in the map
        strength: int
            Current strength of the agent
        game_map: numpy.ndarray
            Map of the game as observed by the agent so far
        map_objects: dict
            Objects discovered by the agent so far

        Returns
        -------
        direction: Directions
            Which direction to move
        """
        t_frontier = {}
        t_visible = {}
        c_list = {}
        visited = QuadAgent.visited
        size = len(game_map) -1
        #Maintaining feasible visited nodes
        if len(visited) == 0:
            visited.append(location)
            QuadAgent.visited_tail = size + size 
        
        x,y = location
        for i in range(size+1):
            for j in range(size+1):
                c_list[(i,j)] = game_map[i][j].value
        
        #Calculating the frontiers           
        for i in game_map:
            x,y = location
            a=x+1,y
            t_frontier[(tuple(a))]=0  
            t_visible[(tuple(a))]=0  
            a=x-1,y
            t_frontier[(tuple(a))]=0 
            t_visible[(tuple(a))]=0
            a=x,y+1
            t_frontier[(tuple(a))]=0  
            t_visible[(tuple(a))]=0
            a=x,y-1
            t_frontier[(tuple(a))]=0 
            t_visible[(tuple(a))]=0

            #t_visible: adding diagonal elements
            a=x+1,y+1
            t_visible[(tuple(a))]=0  
            a=x-1,y+1
            t_visible[(tuple(a))]=0
            a=x-1,y-1
            t_visible[(tuple(a))]=0
            a=x+1,y-1
            t_visible[(tuple(a))]=0
        
        cost_dict = QuadAgent.makedict(c_list)
            
        temp_f = t_frontier.copy()
        #Limiting to the game map's size
        for i in temp_f.keys():
            if i[0] > size or i[0] < 0 or i[1] > size or i[1] < 0:
                del t_frontier[i]
            else:
                if cost_dict[i] == -1:
                    del t_frontier[i]
        
        #Ignoring the visited nodes
        for key in list(t_frontier.keys()):
            if key in visited:
                del t_frontier[key]
                
        temp_v = t_visible.copy()
        for j in temp_v.keys():
            if j[0] > size or j[0] < 0 or j[1] > size or j[1] < 0:
                del t_visible[j]
        
        #Adding cost to the frontiers and visible nodes
        for i in c_list.keys():
            if i in t_visible.keys():
                t_visible[i]=c_list[i]
                
        for i in c_list.keys():
            if i in t_frontier.keys():
                t_frontier[i]=cost_dict[i]
                if t_frontier[i]==-1:
                    t_frontier.pop(i, None)
        
        #Only keeping track of the objects that are currently visible in power_objects            
        power_objects = map_objects.copy()
        for k, v in  map_objects.items():          
            if k not in t_visible.keys():
                del power_objects[k]
                
        close = []
        treasure_route = {}
        temp_power = power_objects.copy()
        tile_cost = 0
        #Looping for skeletons and boss when found
        for k, v in  temp_power.items():
            if v.label == 'skeleton' or v.label == 'boss' or v.label == 'agent':
                recent = (-1,-1)
                if k in t_frontier.keys():
                    monster_strength = v.strength + cost_dict[k]    #Calculating the strength of the monster, if in adjacent tile
                    treasure_route[k] = cost_dict[k];
                else:
                    node_heu = []
                    nodes = []
                    
                    #Calculating the best path to reach the monster
                    for k1,v1 in t_frontier.items():
                        nodes.append(k1)
                        cost = ( abs(k1[0]-k[0]) + abs(k1[1]-k[1]) )
                        node_heu.append(cost)
                    sort_dist = np.argsort(node_heu)
                    if len(t_frontier) == 1:
                        close.append(nodes[sort_dist[0]])
                        treasure_route[close[0]] = cost_dict[close[0]]
                        recent = close[0]   #This variable keeps track of the adjacent tile to the monster, just in case if our strength is less then we remove it
                    elif len(t_frontier) > 1:
                        close.append(nodes[sort_dist[1]])
                        if sort_dist[0] != sort_dist[1]:
                            treasure_route[close[0]] = cost_dict[close[0]]
                            recent = close[0]
                        else:
                            if cost_dict[close[0]] < cost_dict[close[1]]:
                                tile_cost = cost_dict[close[0]]
                                treasure_route[close[0]] = cost_dict[close[0]]
                                recent = close[0]
                            else:
                                tile_cost = cost_dict[close[1]]
                                treasure_route[close[1]] = cost_dict[close[1]]
                                recent = close[1]
                            
                    monster_strength = v.strength + cost_dict[k] + tile_cost  #Calculating the strength of the monster, if in diagonal tile
                                                
                if v.label == "boss" or v.label == "agent":
                    #Calculating the probability of winning
                    prob = strength/(monster_strength + strength)
                    #Comparing the probability with random                    
                    if np.random.random() > prob:
                        if k in power_objects.keys():
                            del power_objects[k]
                        if k in t_frontier.keys():
                            del t_frontier[k]
                        if k in treasure_route.keys():
                            del treasure_route[k]
                        if recent in treasure_route.keys():
                            del treasure_route[recent]
                else:
                    #If strength is less then we remove the monster from our vision
                    if strength < monster_strength:
                        if k in power_objects.keys():
                            del power_objects[k]
                        if k in t_frontier.keys():
                            del t_frontier[k]
                        if k in treasure_route.keys():
                            del treasure_route[k]
                        if recent in treasure_route.keys():
                            del treasure_route[recent]
                    
        
        #Clearing the best to near tiles on every step
        close.clear()
        
        if len(visited) > QuadAgent.visited_tail:
            visited.pop(0)

        #Calculating direction(NEWS) from the suggested node
        next_corr = QuadAgent.dora_explora(t_frontier, power_objects, location, size, cost_dict, treasure_route)
        x = location[0] - next_corr[0]
        y = location[1] - next_corr[1]        
        direction = ''
        if x == 1 and y == 0:
            direction = 'N'
        elif x == -1 and y == 0:
            direction = 'S'
        elif x == 0 and y == 1:
            direction = 'W'
        elif x == 0 and y == -1:
            direction = 'E'
        dir_dict = {'N': Directions.NORTH,
                    'S': Directions.SOUTH,
                    'W': Directions.WEST,
                    'E': Directions.EAST}
        return dir_dict[direction]