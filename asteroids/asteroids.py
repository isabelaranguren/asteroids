"""
Asteroid Game
Shoot space rocks in this demo program created with
Python and the Arcade library.
"""
import math 
from abc import ABC
import os
import arcade
import secrets


# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2

class Point:
    """ This class represents and manipulates x,y coordinates. """
    def __init__(self):
        """ Creates a new point at the given coordinates. """
        self.x = 0.00
        self.y = 0.00
    
class Velocity:
    """ Class stores velocity for objects with dx and dy. """
    def __init__(self):
        self.dx = 0
        self.dy = 0

class FlyingObject(ABC):
    """ Base class """
    def __init__(self, img):
        self.center  = Point()
        self.velocity = Velocity()
        self.alive = True
        self.texture = arcade.load_texture(img)
        self.width = self.texture.width
        self.height = self.texture.height
        self.radius = SHIP_RADIUS
        self.angle = 0
        self.speed = 0
        self.direction = 0
    
    def advance(self):
        self.wrap()
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy   
        
    def is_alive(self):
        return self.alive
    
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height,
                                      self.texture, self.angle, 255)
    def wrap(self):
        # If the ship goes off-screen, 
        # move it to the other side of the window
        if self.center.x > SCREEN_WIDTH:
            self.center.x -= SCREEN_WIDTH
        elif self.center.x < 0:
            self.center.x += SCREEN_WIDTH
        elif self.center.y > SCREEN_HEIGHT:
            self.center.y -= SCREEN_HEIGHT
        elif self.center.y < 0:
            self.center.y += SCREEN_HEIGHT   
            
class Ship(FlyingObject):
    """  
    Class that represents a Ship 
    """
    def __init__(self):
        """ 
        Set up the space ship. 
        """
        super().__init__("images/playerShip1_orange.png")
        self.angle = 1
        self.center.x = (SCREEN_WIDTH / 2)
        self.center.y = (SCREEN_HEIGHT / 2)
        self.radius = SHIP_RADIUS
    
    def left(self):
        self.angle += SHIP_TURN_AMOUNT
    
    def right(self):
        self.angle -= SHIP_TURN_AMOUNT
    
    def thrust(self):
        self.velocity.dx -= math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy += math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
    
    def neg_Thrust(self):
        self.velocity.dx += math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy -= math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
    
    
class Bullet(FlyingObject):
    """  
    Class that represents a bullet that 
    derives from a FlyingObject
    """

    def __init__(self, angle, x, y):
        super().__init__("images/laserBlue01.png")
        self.radius = BULLET_RADIUS
        self.life = BULLET_LIFE
        self.angle = angle
        self.center.x = x
        self.center.y = y
    
    def fire(self):
        """
        Moves the bullets towards its destination
        """
        self.velocity.dx -= math.sin(math.radians(self.angle)) * BULLET_SPEED
        self.velocity.dy += math.cos(math.radians(self.angle)) * BULLET_SPEED
   
    def advance(self):
        super().advance()
        self.life = self.life - 1
        if (self.life <= 0):
            self.alive = False

class Asteroid(FlyingObject):
    """ 
    Represents a rock and derives from a FlyingObject
    """
    def __init__(self,img):
        super().__init__(img)  
        self.radius = 0.0
        
class SmallRock(Asteroid):
    """ 
    Represents a small rock
    """
    def __init__(self):
        super().__init__("images/meteorGrey_small1.png")
        self.radius = SMALL_ROCK_RADIUS
        self.speed = BIG_ROCK_SPEED
    
    def advance(self):
        super().advance()
        self.angle += SMALL_ROCK_SPIN
        
    def break_apart(self, asteroids):
        self.alive = False
    
class MediumRock(Asteroid):
    """ 
    Represents a medium rock
    """
    def __init__(self):
        super().__init__("images/meteorGrey_med1.png")
        self.radius = MEDIUM_ROCK_RADIUS
        self.speed = BIG_ROCK_SPEED
        self.velocity.dx = math.cos(math.radians(self.direction)) * self.speed
        self.velocity.dy = math.sin(math.radians(self.direction)) * self.speed
    
    def advance(self):
        super().advance()
        self.angle += MEDIUM_ROCK_SPIN
    
    def break_apart(self, asteroids):
        """ 
        Splits asteroids into chunks
        """
        small = SmallRock()
        small.center.x = self.center.x
        small.center.y = self.center.y
        small.velocity.dy = self.velocity.dy + 1.5
        small.velocity.dx = self.velocity.dx + 1.5
        
        small2 = SmallRock()
        small2.center.x = self.center.x
        small2.center.y = self.center.y
        small2.velocity.dy = self.velocity.dy - 1.5
        small2.velocity.dx = self.velocity.dx - 1.5
        
        asteroids.append(small)
        asteroids.append(small2)
        self.alive = False
        
class LargeRock(Asteroid):
    """
    Represents a large asteroid
    """
    def __init__(self):
        super().__init__("images/meteorGrey_big1.png")
        self.center.x = secrets.SystemRandom().randint(1, 50)
        self.center.y = secrets.SystemRandom().randint(1, 150)
        self.direction = secrets.SystemRandom().randint(1, 50)
        self.speed = BIG_ROCK_SPEED
        self.radius = BIG_ROCK_RADIUS
        self.velocity.dx = math.cos(math.radians(self.direction)) * self.speed
        self.velocity.dy = math.sin(math.radians(self.direction)) * self.speed
        
    def advance(self):
        super().advance()
        self.angle += BIG_ROCK_SPIN
        
    def break_apart(self, asteroids):
        """ 
        Split an asteroid into chunks. 
        """
        
        # If bullets hits, asteroid breaks apart 
        # and becomes two small asteroids.
        
        med = MediumRock()
        med.center.x = self.center.x
        med.center.y = self.center.y
        med.velocity.dy = self.velocity.dy + 2
        
        med2 = MediumRock()
        med2.center.x = self.center.x
        med2.center.y = self.center.y
        med2.velocity.dy = self.velocity.dy - 2
        
        small = SmallRock()
        small.center.x = self.center.x 
        small.center.y = self.center.y
        small.velocity.dy = self.velocity.dy + 5
        
        asteroids.append(med)
        asteroids.append(med2)
        asteroids.append(small)
        self.alive = False

class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        
        self.held_keys = set()
        
        self.asteroids = []
        
        for i in range(INITIAL_ROCK_COUNT):
            bigAst = LargeRock()
            self.asteroids.append(bigAst)
        
        self.ship = Ship()
        
        # a list to hold the bullets fired by the spaceship
        # (that are active (on the screen))
        self.bullets = []
         
        # Set up the player
        self.score = 0
        self.player_sprite = None
        
        self.laser_sound = arcade.load_sound("sounds/laser.wav")

       
    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()

        for asteroid in self.asteroids:
            asteroid.draw()
        
        for bullet in self.bullets:
            bullet.draw()
        
        self.ship.draw()
        
        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 70, arcade.color.WHITE, 13)

        output = f"Asteroid Count: {len(self.asteroids)}"
        arcade.draw_text(output, 10, 50, arcade.color.WHITE, 13)
        
        
        
    def remove_notAlive(self):
        # Removes objects after being hit by a bullet
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)
        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)
       
    def check_collision(self):
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if ((bullet.alive) and (asteroid.alive)):
                    distance_x = abs(asteroid.center.x - bullet.center.x)
                    distance_y = abs(asteroid.center.y - bullet.center.y)
                    max_dist = asteroid.radius + bullet.radius
                    if ((distance_x < max_dist) and (distance_y < max_dist)):
                        # Collision
                        bullet.alive = False
                        self.score += 1
                        asteroid.break_apart(self.asteroids)
                        asteroid.alive = False   
            
        for asteroid in self.asteroids:
            if ((self.ship.alive) and (asteroid.alive)):
                distance_x = abs(asteroid.center.x - self.ship.center.x)
                distance_y = abs(asteroid.center.y - self.ship.center.y) 
                max_dist = asteroid.radius + self.ship.radius 
                if ((distance_x < max_dist) and (distance_y < max_dist)):
                    self.ship.alive = False
                    asteroid.alive = False
    
 
    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
    
        self.check_keys()
        
        for asteroid in self.asteroids:
            asteroid.advance()
        
        for bullet in self.bullets:
            bullet.advance()
            
        self.remove_notAlive()
        self.check_collision()
        
        self.ship.advance()
        

        
    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.right()

        if arcade.key.UP in self.held_keys:
            self.ship.thrust()

        if arcade.key.DOWN in self.held_keys:
            self.ship.neg_Thrust()

        if arcade.key.SPACE in self.held_keys:
            pass
 
    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need t o add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                bullet = Bullet(self.ship.angle, self.ship.center.x, self.ship.center.y)
                self.bullets.append(bullet)
                bullet.fire()
                arcade.play_sound(self.laser_sound)
            
            # Move the Ship with UP arrow 
            if self.ship.alive:
                self.held_keys.add(key)
                if key == arcade.key.UP:
                    self.ship.thrust()
            
            # Move the Ship with UP arrow 
            if self.ship.alive:
                self.held_keys.add(key)
                if key == arcade.key.DOWN:
                    self.ship.neg_Thrust()
           
            # Rotate the Ship with LEFT arrow
            if self.ship.alive:
                self.held_keys.add(key)
                if key == arcade.key.LEFT:
                    self.ship.left()
            
            # Rotate the Ship with RIGHT arrow
            if self.ship.alive:
                self.held_keys.add(key)
                if key == arcade.key.RIGHT:
                    self.ship.right()
    

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)
    
    
# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()

        
    
