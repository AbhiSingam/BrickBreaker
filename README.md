# DASStruction

DASStruction is a termial-based replica of the popular arcade game brickbreaker.  
It involves using a ball to break to break an arrangement of bricks with the use of a movable paddle to direct the ball and prevent it from falling off the screen (which results in the loss of a life, explaines later).

---

## Types of bricks

There are a total of 6 kinds of bricks:
 - **Weak bricks**:  
 Weak bricks can be broken with a single hit from the ball
 - **Regular bricks**:  
 Regular bricks can be broken with two hits from the ball
 - **Strong bricks**:  
 Strong bricks can be briken with three hits from the ball
 - **Unbreakable bricks**:  
 Unbreakable bricks cannot be broken
 - **Explosive bricks**:  
 Upon being hit, explosive bricks will be destroyed and will also destroy all other bricks around them, including unbreakable bricks. You can use a chain of explosive bricks to create a chain explosion and destroy large amounts of bricks.
 - **Rainbow Bricks**:
 These bricks have a random strength which is decided upon hitting it for the first time.

---

## Game Controls
 - 'a' : Moves paddle left
 - 'd' : Moves paddle right
 - 'w' : Launches ball from initial position
 - 'x' : Ends game
 - 'n' : Next level

---

## Score
You gain 10 points from damaging a weak, regular, or strong brick.  
You do not get points for hitting unbreakable bricks or exploding explosive bricks.

---

## Levels
There are 3 levels in the game, the final one being a boss level. In the the first two standard levels, the condition to beat the level is to break all the bricks. In the boss level, a UFO (represented by a yellow bar) will move with the paddle periodically dropping bombs. To beat the boss level, you must hit the boss with the ball and deplete it's health.

---

## Lives
You have 3 lives at the start of the game and you lose one every time you let the ball fall below the paddle or being hit by a bomb in the boss level. In case you lose all three lives, you lose the game.

---

## Game-Board generation
The board is randomly generated every time you run the game and is made to be symmetrical. It is also ensure that there is one chain of explosive bricks with at least 6 bricks in the chain.

---

## Running the game:
To run the game, run the following commands:
```
pip3 install -r requirements.txt
```
```
python3 main.py
```
---

## Collisions:
- **With walls and roof**:  
When the ball collides with the walls of the board, its velocity is reflected along the wall it collides with. Note: The ball CANNOT collide with the bottom wall of the board.
- **With bricks**:  
When the ball collides with a brick, its velocity is reflected according to the side of the brick it collides with.
- **With paddle**:  
The velocity of the ball is changed depending on where the ball hit the paddle. So if hits further to the right of the paddle, it'll have more velocity to the right and the same goes for the left.  
To ensure sufficiently good rendering of the ball, the ball's velocity along the x direction is capped at 3 (i.e. it cannot be less than -3 or more than 3)

---

## OOPS Concepts:
When making this game, the following OOPS concepts were applied:
- **Abstraction**:  
All the functionality in main.py is implemented via intuitive commands like ball.move() and board.render().
- **Encapsulation**:  
Each game element has it's own class and methods to make the operation and functioning of those game elements simpler.
- **Inheritance**:  
Inheritance is applied in the making of explosive bricks and powerups. It allows for the creation of similar game elements to be done in a simpler manner.
- **Polymorphism**:  
Polymorphism is diplayed in the .hit() and .destroy() methonds of the exploding bricks and the .fall() method of powerups. This allows for the code in brick colloision to be done in a simpler manner as now the class method handles the differences in effect and such features do not need to be implemented separately.

---

## Powerups:
Powerups are dropped at random when any brick is destroyed. The various kinds of powerups include:
- **Laser Paddle**: The paddle shoots lasers from the sides. Each laser travels vertically and will damage any brick it comes in contact with. Lasers cannot break unbreakable bricks.
- **Fireball**: The ball will cause the first brick it hits to explode, similar to exploding bricks.